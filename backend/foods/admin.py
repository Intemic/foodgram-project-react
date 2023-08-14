from django.contrib import admin

from .models import Recipe, RecipeIngredient, RecipeTag

class TagInline(admin.TabularInline):
    model = Recipe.tag.through

class IngredientInline(admin.TabularInline):
    model = Recipe.ingredient.through


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        TagInline,
        IngredientInline,
    ]

    list_display = ('id', 'name', 'author',)
    list_filter = ('author', 'name', 'tag',) 
    empty_value_display = '-пусто-'
