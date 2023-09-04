from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from core.constants import FIELD_LENGTH

User = get_user_model()


class Name(models.Model):
    """Базовый класс, наименование."""
    name = models.CharField(
        verbose_name='Название',
        max_length=FIELD_LENGTH['NAME'],
        help_text='Название',
        db_index=True,
        unique=True
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.name[:50]


class Ingredient(models.Model):
    """Ингридиенты."""
    name = models.CharField(
        verbose_name='Название',
        max_length=FIELD_LENGTH['NAME'],
        help_text='Название',
    )
    measurement_unit = models.CharField(
        verbose_name='ЕИ',
        max_length=FIELD_LENGTH['UNITS'],
        help_text='Единицы измерения'
    )

    class Meta(Name.Meta):
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name[:50]


class Tag(Name):
    """Тэг."""
    color = models.CharField(
        max_length=7,
    )
    slug = models.SlugField(
        max_length=FIELD_LENGTH['SLUG'],
        unique=True
    )

    class Meta(Name.Meta):
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Recipe(Name):
    """Рецепт."""
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipes',
        help_text='Автор публикации'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
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
                'Введите значение больше или равно 1 мин'
            )
        ],
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиент',
        help_text='Ингредиент',
        through='RecipeIngredient'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        help_text='Тег',
        through='RecipeTag'
    )

    class Meta(Name.Meta):
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date', 'name']


class RecipeTag(models.Model):
    """Связка рецепт - тэг."""
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='rec_tags'
    )
    tag = models.ForeignKey(
        Tag,
        verbose_name='Тэг',
        on_delete=models.CASCADE,
        related_name='rec_tags'
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=['recipe', 'tag'], name='unique tag')
        ]
        verbose_name = 'Рецепт, Тэг'
        verbose_name_plural = 'Рецепт, Тэги'


class RecipeIngredient(models.Model):
    """Связка рецепт - ингредиент."""
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='rec_ingrs',
        db_index=True
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
        related_name='rec_ingrs'
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        help_text='Количество в рецепте',
        validators=[
            MinValueValidator(
                1,
                'Введите значение больше или равно 1'
            )
        ],
    )

    class Meta:
        default_related_name = 'recipe_ing'
        constraints = [
            UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique ingredient'
            )
        ]
        verbose_name = 'Рецепт, Ингредиент'
        verbose_name_plural = 'Рецепт, Ингредиенты'


class Favorite(models.Model):
    """Фавориты."""
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'recipe'], name='unique recipe')
        ]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class ShopList(models.Model):
    """Список покупок."""
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='shoplists'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='shoplists'
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'recipe'], name='unique shoplist')
        ]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списоки покупок'
        ordering = ['user', 'recipe']
