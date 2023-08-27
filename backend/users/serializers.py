from rest_framework import serializers
from core.constants import FIELD_LENGTH
from core.validators import username_validator
from django.core.validators import validate_email
from rest_framework.validators import UniqueValidator
from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth.password_validation import validate_password as validate_passwd
from django.core.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from .models import Follow, User


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
        # if self.context:
        #     user = self.context['request'].user

        return False


class UserCreateSerializers(serializers.ModelSerializer):
    email = serializers.CharField(
        max_length=FIELD_LENGTH['EMAIL'],
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


class FollowSerializer(serializers.ModelSerializer):
    # user = serializers.SlugRelatedField(
    #     read_only=True, slug_field='username',
    #     default=serializers.CurrentUserDefault()
    # )
    # following = serializers.SlugRelatedField(
    #     queryset=User.objects.all(),
    #     slug_field='username'
    # )

    class Meta:
        fields = (
            'user',
            'following',
        )
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following')
            )
        ]

    def validate_following(self, data):
        user = self.context['request'].user
        if user == data:
            raise serializers.ValidationError(
                {'following': 'Подписка на себя недопустима'}
            )
        return data
    
    def to_representation(self, instance):
        user_serializer = UserSerializer(instance.following)
        return super().to_representation(instance)