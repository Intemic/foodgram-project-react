from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Favorite, Ingredient, Recipe, ShopList, Tag


class TagsInline(admin.TabularInline):
    model = Recipe.tags.through
    min_num = 1


class IngredientsInline(admin.TabularInline):
    model = Recipe.ingredients.through
    min_num = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """'Админка' для тэга."""
    list_display = ('id', 'name', 'color', 'slug',)
    list_filter = ('name', )
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class Ingredient(admin.ModelAdmin):
    """'Админка' для ингредиента."""
    list_display = ('id', 'name', 'measurement_unit',)
    list_filter = ('name', )
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class Favorite(admin.ModelAdmin):
    """'Админка' для фаворитов."""
    list_display = ('id', 'user', 'recipe', )
    list_filter = ('user', )
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """'Админка' для рецепта."""
    inlines = [
        TagsInline,
        IngredientsInline,
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
        ('get_count',),
    )
    list_display = (
        'id',
        'name',
        'author',
        'get_html_photo',
        'get_tag',
        'get_count',
    )
    readonly_fields = ('get_html_photo', 'get_count',)
    list_filter = ('author', 'name', 'tags',)
    empty_value_display = '-пусто-'

    @admin.display(description='Тэги')
    def get_tag(self, obj):
        return [tag for tag in obj.tags.all()]

    @admin.display(description='Кол-во в избр.')
    def get_count(self, obj):
        return obj.favorites.count()

    @admin.display(description='Миниатюра')
    def get_html_photo(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{ obj.image.url }" width=100>')


@admin.register(ShopList)
class ShopList(admin.ModelAdmin):
    """'Админка' для списка покупок."""
    list_display = ('id', 'user', 'recipe', )
    list_filter = ('user', )
    empty_value_display = '-пусто-'
