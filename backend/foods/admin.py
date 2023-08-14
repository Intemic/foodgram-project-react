from django.contrib import admin

from .models import Ingredient, Recipe, Favorite, Follow, Tag


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
    fk_name = 'ingredient'
    list_display = (
        'id',
        'name',
        'author',
        'get_ingredient',
        'get_tag'
    )
    list_filter = ('author', 'name', 'tag',)
    empty_value_display = '-пусто-'

    @admin.display(description='Ингридиенты')
    def get_ingredient(self, obj):
        return [ingredient for ingredient in obj.ingredient.all()]

    @admin.display(description='Тэги')
    def get_tag(self, obj):
        return [tag for tag in obj.tag.all()]
