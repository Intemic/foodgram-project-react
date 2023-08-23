import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from .models import Ingredient, Recipe, RecipeIngredient, RecipeTag, Tag 
from core.constants import FIELD_LENGTH


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


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
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

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
        max_length=FIELD_LENGTH['NAME']
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

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
     
        recipe = Recipe.objects.create(**validated_data)
        for ing in ingredients:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=Ingredient.objects.get(id=ing['id']),
                amount=ing['amount']
            )

        recipe.tags.set(tags)    

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

        for ing in ingredients:
            RecipeIngredient.objects.get_or_create(
                recipe=instance,
                ingredient=Ingredient.objects.get(id=ing['id']),
                amount=ing['amount']
            )

        instance.tags.set(tags)
        return instance

    def to_representation(self, instance):
        return RecipeSerializer(instance).data
