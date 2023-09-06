import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from core.constants import FIELD_LENGTH
from core.validators import name_validator
from foods.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                          ShopList, Tag)
from users.serializers import UserSerializers

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeIngredientSerializer(serializers.ModelSerializer):
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
        if self.context:
            user = self.context['request'].user
            if user.is_authenticated:
                return user.favorites.filter(recipe=obj.id).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        if self.context:
            user = self.context['request'].user
            if user.is_authenticated:
                return user.shoplists.filter(recipe=obj.id).exists()
        return False


class RecipeShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientCreateSerializer(
        many=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    image = Base64ImageField()
    name = serializers.CharField(
        max_length=FIELD_LENGTH['NAME'],
        validators=[name_validator]
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

    def validate_cooking_time(self, value):
        if value < 1:
            raise serializers.ValidationError(
                'Введите значение больше или равно 1 мин!'
            )
        return value

    def validate_name(self, value):
        if Recipe.objects.filter(name=value).exists():
            raise serializers.ValidationError(
                'Рецепт с таким именем уже существует!'
            )
        return value

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')

        recipe = Recipe.objects.create(**validated_data)

        self.save_tag_ingredient(recipe, tags, ingredients)

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
        instance.save()

        self.save_tag_ingredient(instance, tags, ingredients)

        return instance

    def save_tag_ingredient(self, instance, tags, ingredients):
        # удалим старые данные, актуально только для обновления, но для
        # создания ничего страшного
        RecipeIngredient.objects.filter(recipe=instance.id).delete()

        # соберем дубликаты
        total_quantity = {}
        for ingredient in ingredients:
            if not ingredient.get('id') in total_quantity:
                total_quantity[
                    ingredient.get('id')] = int(ingredient['amount'])
            else:
                total_quantity[
                    ingredient.get('id')] += int(ingredient['amount'])

        RecipeIngredient.objects.bulk_create(
            [RecipeIngredient(
                recipe=instance,
                ingredient=Ingredient.objects.get(id=key),
                amount=int(amount)
            ) for key, amount in total_quantity.items()]
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
        # не должен же рецепт состоять только из одного ингредиента
        if len(ingredients) == 1:
            raise serializers.ValidationError(
                'Укажите больше одного ингредиента'
            )

        return attrs

    def to_representation(self, instance):
        return RecipeSerializer(instance).data


class FavoriteCreateSerializer(serializers.ModelSerializer):
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
