import re

from django.core.exceptions import ValidationError

from core.constants import NAME_PATTERN, USERNAME_PATTERN


def username_validator(value):
    """Валидация имени пользователя."""
    result = set(re.sub(USERNAME_PATTERN, '', value))
    if result:
        raise ValidationError(
            f'недопустимые символы: {"".join(result)}'
        )
    if value.lower() == 'me':
        raise ValidationError(
            'Использовать имя me запрещено'
        )
    return value


def name_validator(value):
    """Валидация названия, в требованиях не было,
    но что мешает проверить?."""
    result = set(re.sub(NAME_PATTERN, '', value))
    if result:
        raise ValidationError(
            ('Имя не может начинаться с цифры или пробела и '
             'быть меньше трех символов'
             )
        )
    return value
