from rest_framework import serializers
from core.constants import FIELD_LENGTH
from core.validators import username_validator
from django.core.validators import validate_email
from rest_framework.validators import UniqueValidator

from .models import User


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
    # password = serializers.CharField(
    #     max_length=FIELD_LENGTH['PASSWORD']
    # )

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )

    def to_representation(self, instance):
        serializer_data = UserSerializers(instance).data
        serializer_data.pop('is_subscribed') 
        return serializer_data
