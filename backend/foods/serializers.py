import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from core.constants import FIELD_LENGTH
from users.serializers import UserSerializers

from .models import (Favorite, Ingredient, Recipe, RecipeIngredient, ShopList,
                     Tag)

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тэга."""
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )

    def validate(self, value):
        if Tag.objects.filter(name=value).exists():
            raise serializers.ValidationError(
                'Тэг с таким именем уже существует!'
            )
        return value


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиента."""
    class Meta:
        model = Ingredient
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('name', 'measurement_unit'),
                message='Комбинация ингредиент - ЕИ не уникальна'
            )
        ]
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания пары рецепт - ингредиент."""
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор отображения пары рецепт - ингредиент."""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор отображения рецепта."""
    tags = TagSerializer(
        many=True,
    )
    ingredients = RecipeIngredientSerializer(
        source='rec_ingrs',
        many=True
    )
    author = UserSerializers()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    # без source не отображаются картинки на сервере
    image = serializers.ReadOnlyField(source='image.url')

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        return (self.context
                and self.context['request'].user.is_authenticated
                and obj.favorites.filter(
                    user=self.context['request'].user.id).exists()
                )

    def get_is_in_shopping_cart(self, obj):
        return (self.context
                and self.context['request'].user.is_authenticated
                and obj.shoplists.filter(
                    user=self.context['request'].user.id).exists()
                )


class RecipeShortSerializer(serializers.ModelSerializer):
    """Укороченный сериализатор для рецепта."""
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class Base64ImageField(serializers.ImageField):
    """Поля для изображения."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания рецепта."""
    ingredients = RecipeIngredientCreateSerializer(
        many=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    image = Base64ImageField()
    name = serializers.CharField(
        max_length=FIELD_LENGTH['NAME']
    )

    cooking_time = serializers.IntegerField(
        min_value=FIELD_LENGTH['MIN_COOK_TIME'],
        max_value=FIELD_LENGTH['MAX_COOK_TIME']
    )

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
        )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')

        recipe = Recipe.objects.create(
            author=self.context.get('request').user,
            **validated_data
        )

        RecipeCreateSerializer.save_tag_ingredient(recipe, tags, ingredients)

        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')

        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )

        RecipeCreateSerializer.save_tag_ingredient(instance, tags, ingredients)

        return super().update(instance, validated_data)

    @staticmethod
    def save_tag_ingredient(instance, tags, ingredients):
        # удалим старые данные, актуально только для обновления, но для
        # создания ничего страшного
        instance.ingredients.clear()

        RecipeIngredient.objects.bulk_create(
            [RecipeIngredient(
                recipe=instance,
                ingredient=ingredient['ingredient'],
                amount=ingredient['amount']
            ) for ingredient in ingredients]
        )

        instance.tags.set(tags)

    def validate(self, attrs):
        tags = attrs.get('tags')
        if not tags:
            raise serializers.ValidationError(
                'Укажите тэги для рецепта'
            )
        ingredients = attrs.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError(
                'Не указаны ингредиенты для рецепта'
            )

        count_ingredients = len(ingredients)
        ing_no_dubl = {
            ingredient['ingredient'].id for ingredient in ingredients
        }
        if len(ing_no_dubl) != count_ingredients:
            raise serializers.ValidationError(
                'Присутствуют не уникальные ингредиенты для рецепта'
            )

        count_tags = len(tags)
        tag_no_dubl = {tag.id for tag in tags}
        if len(tag_no_dubl) != count_tags:
            raise serializers.ValidationError(
                'Присутствуют не уникальные тэги для рецепта'
            )

        return attrs

    def to_representation(self, instance):
        return RecipeSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data


class FavoriteCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания фаворитов."""
    class Meta:
        fields = (
            'user',
            'recipe',
        )
        model = Favorite
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт уже находится в избранном'
            )
        ]

    def validate(self, attrs):
        if attrs['user'].id == attrs['recipe'].author.id:
            raise serializers.ValidationError(
                {'following': 'Недопустимо добавить свой рецепт в избранное'}
            )

        return attrs

    def to_representation(self, instance):
        return RecipeShortSerializer(instance.recipe).data


class ShopListCreateSerializer(serializers.ModelSerializer):
    """Сериализатор списка покупок."""
    class Meta:
        fields = (
            'user',
            'recipe',
        )
        model = ShopList
        validators = [
            UniqueTogetherValidator(
                queryset=ShopList.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт уже находится в избранном'
            )
        ]

    def to_representation(self, instance):
        return RecipeShortSerializer(instance.recipe).data
