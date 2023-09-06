FIELD_LENGTH = {
    'NAME': 200,
    'SLUG': 200,
    'UNITS': 200,
    'USER_NAME': 150,
    'EMAIL': 254,
    'PASSWORD': 150,
    'FIRST_NAME': 150,
    'LAST_NAME': 150,
}

USERNAME_PATTERN = r'^[\w.@+-]+'
# будем считать что название должн состоять как минимум из 3 букв
NAME_PATTERN = r'^[^\s\d]{1}\w{2,}'

PAGE_SIZE = 6
