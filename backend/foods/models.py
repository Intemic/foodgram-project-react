from colorfield.fields import ColorField
from core.constants import FIELD_LENGTH
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()


class BaseName(models.Model):
    """Базовый класс, наименование."""
    name = models.CharField(
        verbose_name='Название',
        max_length=FIELD_LENGTH['NAME'],
        help_text='Название',
        db_index=True,
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name[:FIELD_LENGTH['LENGTH_OUTPUT_NAME']]


class Ingredient(BaseName):
    """Ингридиенты."""
    measurement_unit = models.CharField(
        verbose_name='ЕИ',
        max_length=FIELD_LENGTH['UNITS'],
        help_text='Единицы измерения'
    )

    class Meta(BaseName.Meta):
        constraints = [
            UniqueConstraint(
                fields=['name', 'measurement_unit'], name='name unit'
            )
        ]
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Tag(BaseName):
    """Тэг."""
    color = ColorField(
        max_length=FIELD_LENGTH['COLOR'],
    )
    slug = models.SlugField(
        max_length=FIELD_LENGTH['SLUG'],
        unique=True
    )

    class Meta(BaseName.Meta):
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Recipe(BaseName):
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
                FIELD_LENGTH['MIN_COOK_TIME'],
                'Введите значение больше или равно 1 мин'
            ),
            MaxValueValidator(
                FIELD_LENGTH['MAX_COOK_TIME'],
                'Что то долговато готовить'
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

    class Meta(BaseName.Meta):
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date', 'name',)


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
        ordering = ('recipe',)


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
    amount = models.PositiveSmallIntegerField(
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
        ordering = ('recipe',)


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
        ordering = ('user', 'recipe',)


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
        ordering = ('user', 'recipe',)
