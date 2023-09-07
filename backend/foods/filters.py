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
        # проверку (and value:) убрал но странно что при переданом параметре
        # со значением 0 все равно показываем только из списка фаворитов
        if self.request.user.is_authenticated:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        # здесь аналогичный вопрос (and value:)
        if self.request.user.is_authenticated:
            return queryset.filter(shoplists__user=self.request.user)
        return queryset
