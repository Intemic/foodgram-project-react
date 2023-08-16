# Generated by Django 3.2.3 on 2023-08-16 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favorite',
            options={'verbose_name': 'Избранное', 'verbose_name_plural': 'Избранное'},
        ),
        migrations.AlterModelOptions(
            name='follow',
            options={'verbose_name': 'Подписки', 'verbose_name_plural': 'Подписки'},
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={'verbose_name': 'Ингредиент', 'verbose_name_plural': 'Ингредиенты'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-pub_date', 'name'], 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AlterModelOptions(
            name='recipeingredient',
            options={'verbose_name': 'Рецепт, Ингредиент', 'verbose_name_plural': 'Рецепт, Ингредиенты'},
        ),
        migrations.AlterModelOptions(
            name='recipetag',
            options={'verbose_name': 'Рецепт, Тэг', 'verbose_name_plural': 'Рецепт, Тэги'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'Тэг', 'verbose_name_plural': 'Тэги'},
        ),
    ]
