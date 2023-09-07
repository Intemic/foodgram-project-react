FIELD_LENGTH = {
    'NAME': 200,
    'SLUG': 200,
    'UNITS': 200,
    'USER_NAME': 150,
    'PASSWORD': 150,
    'FIRST_NAME': 150,
    'LAST_NAME': 150,
    'LENGTH_OUTPUT_NAME': 50,
    'COLOR': 7,
    'MIN_COOK_TIME': 1,
    'MAX_COOK_TIME': 32000,
}

USERNAME_PATTERN = r'^[\w.@+-]+'
# будем считать что название должн состоять как минимум из 3 букв
NAME_PATTERN = r'^[^\s\d]{1}\w{2,}'

PAGE_SIZE = 6
