from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

from core.constants import FIELD_LENGTH


User = get_user_model()


class Ingredient(models.Model):
    pass


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=FIELD_LENGTH['NAME'],
        help_text='Название'
    )
    color = models.CharField(
        max_length=7,
        default="#ffffff"
    )
    slug = models.SlugField(
        max_length=FIELD_LENGTH['SLUG'],
        unique=True
    )


class Recipe(models.Models):
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipes',
        help_text='Автор публикации'
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=FIELD_LENGTH['NAME'],
        help_text='Название'
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipes/',
        help_text='Изображение'
    )
    text = models.TextField(
        verbose_name='Описание',
        help_text='Описание рецепта'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        help_text='Время приготовления (в минутах)',
        validators=[
            MinValueValidator(
                1,
                'Введите значение больше или равно 1'
            )
        ],
    )
    ingredient = models.ManyToManyField(
        ,
        verbose_name='Ингредиент',
        help_text='Ингредиент',
        #????
    )
    tag = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        help_text='Тег',
        related_name='recipes',
    )
