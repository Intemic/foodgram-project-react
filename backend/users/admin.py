from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = (
        'username',
        'password',
        'email',
        'first_name',
        'last_name',
        'date_joined', 
    )
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
