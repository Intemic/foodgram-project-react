import csv
import os
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import models

from foods.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                          RecipeTag, Tag)
from users.models import Follow, User


def create_simple_model(file_data: csv.DictReader, model: models.Model):
    """Создание простой модели."""
    model.objects.all().delete()
    model.objects.bulk_create(
        [
            model(**row)
            for row in file_data
        ]
    )


def create_recipe_model(file_data: csv.DictReader, model: Recipe):
    """Создание модели Recipe."""
    model.objects.all().delete()
    model.objects.bulk_create(
        [
            model(
                id=row.get('id'),
                name=row.get('name'),
                author=User.objects.get(id=row.get('author_id')),
                pub_date=row.get('pub_date'),
                image=row.get('image'),
                text=row.get('text'),
                cooking_time=row.get('cooking_time')
            )
            for row in file_data
        ]
    )


def create_recipe_tag_model(file_data: csv.DictReader, model: RecipeTag):
    model.objects.all().delete()
    model.objects.bulk_create(
        [
            model(
                id=row.get('id'),
                recipe=Recipe.objects.get(id=row.get('recipe_id')),
                tag=Tag.objects.get(id=row.get('tag_id'))
            )
            for row in file_data
        ]
    )


def create_recipe_ingredient_model(
        file_data: csv.DictReader, model: RecipeIngredient):
    model.objects.all().delete()
    model.objects.bulk_create(
        [
            model(
                id=row.get('id'),
                recipe=Recipe.objects.get(id=row.get('recipe_id')),
                ingredient=Ingredient.objects.get(id=row.get('ingredient_id')),
                amount=row.get('amount')
            )
            for row in file_data
        ]
    )


def create_follow_model(
        file_data: csv.DictReader, model: Follow):
    model.objects.all().delete()
    model.objects.bulk_create(
        [
            model(
                id=row.get('id'),
                user=User.objects.get(id=row.get('user_id')),
                following=User.objects.get(id=row.get('following_id')),
            )
            for row in file_data
        ]
    )


def create_favorite_model(
        file_data: csv.DictReader, model: Favorite):
    model.objects.all().delete()
    model.objects.bulk_create(
        [
            model(
                id=row.get('id'),
                user=User.objects.get(id=row.get('user_id')),
                recipe=Recipe.objects.get(id=row.get('recipe_id')),
            )
            for row in file_data
        ]
    )


class Command(BaseCommand):
    help = 'Загрузка данных из CSV файлов'
    # link_models = (
    #     ('ingredients.csv', Ingredient, create_simple_model),
    #     # ('tags.csv', Tag, create_simple_model),
    #     # ('recipe.csv', Recipe, create_recipe_model),
    #     # ('recipetag.csv', RecipeTag, create_recipe_tag_model),
    #     # (
    #     #     'recipeingredient.csv',
    #     #     RecipeIngredient,
    #     #     create_recipe_ingredient_model
    #     # ),
    #     # ('follow.csv', Follow, create_follow_model),
    #     # ('favorite.csv', Favorite, create_favorite_model),
    # )

    def handle(self, *args, **options):
        work_dir = Path(Path(settings.BASE_DIR).parent, 'data')
        with os.scandir(work_dir) as files:
            files = [file.name for file in files if file.is_file()
                     and file.name.endswith('.csv')]

        print('загрузка данных из файла(ов):')

        # будем грузить по порядку иначе будут проблемы
        for file, model, func in self.link_models:
            if file in files:
                with open(Path(work_dir, file), encoding='utf-8') as h_file:
                    file_reader = csv.DictReader(h_file, delimiter=',')
                    print(f'{file} - ', end='')
                    try:
                        func(file_reader, model)
                        print('\033[32m OK \033[0;0m')
                    except Exception as err:
                        print(err)
                        print('\033[31m NO \033[0;0m')
            else:
                print(f'{file} - \033[31m NO \033[0;0m')
