## Коротко о проекте:

Проект представляет из себя продуктового помощника.
Он предоставляет следующие возможности: 
```
- создать, просмотривать, редактировать рецепты.
- подписываться на понравившихся авторов
- заносить рецепты в избранное
- просматривать страницу пользователя с рецептами
- формировать список покупок с необходимыми ингредиентами
```

проект построен на архитектуре REST API

Адрес сайта: https://yfoodgram.hopto.org/

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Intemic/foodgram-project-react.git
```

```
cd foodgram-project-react
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

Ознакомиться с документацией проекта можно по адресу:

```
http://127.0.0.1:8000/api/doc/
```

### Запуск проекта в контейнере:

Перейти в директорию:

```
 cd foodgram
```

Скачать последние обзазы с Docker Hub :

```
sudo docker compose -f docker-compose.production.yml pull
```

Удалить старые образы:

```
sudo docker compose -f docker-compose.production.yml down 
```

Удалить старые образы:

```
sudo docker compose -f docker-compose.production.yml down 
```

Запустить контейнеры:

```
sudo docker compose -f docker-compose.production.yml up -d
```

Выполнить миграции:

```
 sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
```

Собрать статику:

```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic --no-input
```

Скопировать статику

```
sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/backend_static/. /backend_static/static/ 
```

### Загрузить тестовые данные:

```
python3 manage.py loaddata ../data/db.json
```

### Для реализации использовались следующие технологии:

```
- Django REST framework
- djoser
- Pillow
```

### Примеры запросов к API :

**GET** /api/recipes/
```
{
  "count": 123,
  "next": "http://foodgram.example.org/api/recipes/?page=4",
  "previous": "http://foodgram.example.org/api/recipes/?page=2",
  "results": [
    {
      "id": 0,
      "tags": [
        {
          "id": 0,
          "name": "Завтрак",
          "color": "#E26C2D",
          "slug": "breakfast"
        }
      ],
      "author": {
        "email": "user@example.com",
        "id": 0,
        "username": "string",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "is_subscribed": false
      },
      "ingredients": [
        {
          "id": 0,
          "name": "Картофель отварной",
          "measurement_unit": "г",
          "amount": 1
        }
      ],
      "is_favorited": true,
      "is_in_shopping_cart": true,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "text": "string",
      "cooking_time": 1
    }
  ]
}
```

**GET** /api/users/
```
{
  "count": 123,
  "next": "http://foodgram.example.org/api/users/?page=4",
  "previous": "http://foodgram.example.org/api/users/?page=2",
  "results": [
    {
      "email": "user@example.com",
      "id": 0,
      "username": "string",
      "first_name": "Вася",
      "last_name": "Пупкин",
      "is_subscribed": false
    }
  ]
}
```

**GET** /api/users/subscriptions/
```

{
  "count": 123,
  "next": "http://foodgram.example.org/api/users/subscriptions/?page=4",
  "previous": "http://foodgram.example.org/api/users/subscriptions/?page=2",
  "results": [
    {
      "email": "user@example.com",
      "id": 0,
      "username": "string",
      "first_name": "Вася",
      "last_name": "Пупкин",
      "is_subscribed": true,
      "recipes": [
        {
          "id": 0,
          "name": "string",
          "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
          "cooking_time": 1
        }
      ],
      "recipes_count": 0
    }
  ]
}

```

... 
```
для более полной информации обратитесь к документации
```

Администратор: anton
Пароль: django_anton
