# Generated by Django 3.2.3 on 2023-08-27 05:38

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранное',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название', max_length=200, verbose_name='Название')),
                ('measurement_unit', models.CharField(help_text='Единицы измерения', max_length=200, verbose_name='ЕИ')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название', max_length=200, verbose_name='Название')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('image', models.ImageField(help_text='Изображение', upload_to='recipes/', verbose_name='Изображение')),
                ('text', models.TextField(help_text='Описание рецепта', verbose_name='Описание')),
                ('cooking_time', models.PositiveIntegerField(help_text='Время приготовления (в минутах)', validators=[django.core.validators.MinValueValidator(1, 'Введите значение больше или равно 1 мин')], verbose_name='Время приготовления')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ['-pub_date', 'name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(help_text='Количество в рецепте', validators=[django.core.validators.MinValueValidator(1, 'Введите значение больше или равно 1')], verbose_name='Количество')),
            ],
            options={
                'verbose_name': 'Рецепт, Ингредиент',
                'verbose_name_plural': 'Рецепт, Ингредиенты',
            },
        ),
        migrations.CreateModel(
            name='RecipeTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Рецепт, Тэг',
                'verbose_name_plural': 'Рецепт, Тэги',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название', max_length=200, verbose_name='Название')),
                ('color', models.CharField(max_length=7)),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
            options={
                'verbose_name': 'Тэг',
                'verbose_name_plural': 'Тэги',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ShopList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shoplists', to='foods.recipe', verbose_name='Рецепт')),
            ],
            options={
                'verbose_name': 'Список покупок',
                'verbose_name_plural': 'Списоки покупок',
                'ordering': ['user', 'recipe'],
            },
        ),
    ]
