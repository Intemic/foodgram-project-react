import csv
import os
from pathlib import Path

from django.conf import settings
from django.db import models
from django.core.management.base import BaseCommand
from foods.models import Ingredient, Tag


def create_simple_model(file_data: csv.DictReader, model: models.Model):
    """Создание простой модели."""
    model.objects.all().delete()
    model.objects.bulk_create(
        [
            model(**row)
            for row in file_data
        ]
    )


class Command(BaseCommand):
    help = 'Загрузка данных из CSV файлов'
    link_models = (
        ('ingredients.csv', Ingredient, create_simple_model),
        ('tags.csv', Tag, create_simple_model),
        # ('users.csv', User, create_simple_model),
        # ('titles.csv', Title, create_title_model),
        # ('genre_title.csv', TitleGenre, create_genre_title_model),
        # ('review.csv', Review, create_review_model),
        # ('comments.csv', Comment, create_comments_model)
    )

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
                    except Exception:
                        print('\033[31m NO \033[0;0m')
            else:
                print(f'{file} - \033[31m NO \033[0;0m')
