import re

from core.constants import USERNAME_PATTERN
from django.core.exceptions import ValidationError


def username_validator(value):
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