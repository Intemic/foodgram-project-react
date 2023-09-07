from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint

from core.constants import FIELD_LENGTH
from core.validators import username_validator


class User(AbstractUser):
    """Пользователь подходящий под ТЗ."""
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=FIELD_LENGTH['USER_NAME'],
        unique=True,
        db_index=True,
        validators=[username_validator]
    )
    # это же обязательное поле, если убрать так понимаю станет необязательным?
    email = models.EmailField(
        verbose_name='Email',
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=FIELD_LENGTH['FIRST_NAME']
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=FIELD_LENGTH['LAST_NAME']
    )
    password = models.CharField(
        max_length=FIELD_LENGTH['PASSWORD']
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self) -> str:
        return self.get_full_name()[:FIELD_LENGTH['LENGTH_OUTPUT_NAME']]


class Follow(models.Model):
    """Подписки."""
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='follower'
    )
    following = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'following'],
                name='unique following'
            )
        ]
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'
        ordering = ('user',)
