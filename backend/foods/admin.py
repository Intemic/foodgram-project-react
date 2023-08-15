from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Favorite, Follow, Ingredient, Recipe, Tag


class TagInline(admin.TabularInline):
    model = Recipe.tag.through


class IngredientInline(admin.TabularInline):
    model = Recipe.ingredient.through


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug',)
    list_filter = ('name', )
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class Ingredient(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit',)
    list_filter = ('name', )
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class Favorite(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe', )
    list_filter = ('user', )
    empty_value_display = '-пусто-'


@admin.register(Follow)
class Follow(admin.ModelAdmin):
    list_display = ('id', 'user', 'following', )
    list_filter = ('user', )
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        TagInline,
        IngredientInline,
    ]
    fields = (
        (
            'name',
            'cooking_time',
        ),
        (
            'author',
        ),
        ('text',),
        (
            'image',
            'get_html_photo'
        ),
    )
    list_display = (
        'id',
        'name',
        'author',
        'get_html_photo',
        'get_ingredient',
        'get_tag',
        'get_count',
    )
    readonly_fields = ('get_html_photo',)
    list_filter = ('author', 'name', 'tag',)
    empty_value_display = '-пусто-'

    @admin.display(description='Ингридиенты')
    def get_ingredient(self, obj):
        return [ingredient for ingredient in obj.ingredient.all()]

    @admin.display(description='Тэги')
    def get_tag(self, obj):
        return [tag for tag in obj.tag.all()]

    @admin.display(description='Кол-во в избр.')
    def get_count(self, obj):
        return obj.favorites.count()

    @admin.display(description='Миниатюра')
    def get_html_photo(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{ obj.image.url }" width=100>')
