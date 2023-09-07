from django.contrib.auth.password_validation import \
    validate_password as validate_passwd
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from core.constants import FIELD_LENGTH
from core.validators import username_validator
from foods.models import Recipe
from users.models import Follow, User


class UserSerializers(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(

    )

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        return (self.context
                and self.context['request'].user.is_authenticated
                and obj.following.filter(
                    user=self.context['request'].user.id).exists()
                )


class UserCreateSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[
            validate_email,
            UniqueValidator(
                queryset=User.objects.all(),
                message='Пользователь с таким email уже существует'
            )
        ]
    )
    username = serializers.CharField(
        max_length=FIELD_LENGTH['USER_NAME'],
        validators=[
            username_validator,
            UniqueValidator(
                queryset=User.objects.all(),
                message='Пользователь с таким username уже существует'
            )
        ]
    )
    first_name = serializers.CharField(
        max_length=FIELD_LENGTH['FIRST_NAME']
    )
    last_name = serializers.CharField(
        max_length=FIELD_LENGTH['LAST_NAME']
    )
    password = serializers.CharField(
        style={"input_type": "password"},
        max_length=FIELD_LENGTH['PASSWORD'],
        write_only=True,
    )

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate_password(self, value):
        try:
            validate_passwd(value, self.context['request'].user)
        except ValidationError:
            raise serializers.ValidationError(
                'Некорретный пароль'
            )
        return value

    def to_representation(self, instance):
        serializer_data = UserSerializers(instance).data
        serializer_data.pop('is_subscribed')
        return serializer_data


class FollowCreateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'user',
            'following',
        )
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Пользователь уже подписан на данного автора'
            )
        ]

    def validate(self, attrs):
        if attrs['user'].id == attrs['following'].id:
            raise serializers.ValidationError(
                {'following': 'Подписка на себя недопустима'}
            )

        return attrs

    def to_representation(self, instance):
        return FollowSerializer(
            instance.following,
        ).data


class FollowSerializer(UserSerializers):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserSerializers.Meta):
        fields = UserSerializers.Meta.fields + (
            'recipes',
            'recipes_count'
        )

    def get_recipes(self, obj):
        recipes_limit = 0
        if self.context.get('request'):
            recipes_limit = int(
                self.context['request'].query_params.get('recipes_limit', 0)
            )
        if recipes_limit:
            recipes = obj.recipes.all()[:recipes_limit]
        else:
            recipes = obj.recipes.all()
        return RecipeShortSerializer(
            recipes,
            many=True
        ).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class RecipeShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
