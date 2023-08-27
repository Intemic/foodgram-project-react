from typing import Any
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin): 
    list_display = (
        'id',
        'username',
        'password',
        'email',
        'first_name',
        'last_name',
    )
    list_filter = ('username', 'email',)
    ordering = ('username', )
    empty_value_display = '-пусто-'
