import django_filters
from django_filters import rest_framework as filter
from rest_framework.filters import SearchFilter

from foods.models import Ingredient, Recipe


class IngredientFilter(SearchFilter):
    """Фильтр для ингредиентов."""
    search_param = 'name'

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(django_filters.FilterSet):
    """Фильтрация для рецептов."""
    is_favorited = filter.BooleanFilter(method='get_is_favorited')
    author = filter.NumberFilter(field_name='author')
    is_in_shopping_cart = filter.BooleanFilter(
        method='get_is_in_shopping_cart'
    )
    tags = filter.AllValuesMultipleFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = (
            'is_favorited',
            'author',
            'is_in_shopping_cart',
            'tags',
        )

    def get_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorites__user_id=self.request.user.pk)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(shoplists__user_id=self.request.user.pk)
        return queryset
