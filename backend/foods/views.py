from rest_framework import filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import Ingredient, Recipe, Tag
from .filters import RecipeFilter
from .pagination import PageLimitPagination
from .serializers import IngredientSerializer, RecipeSerializer, RecipeCreateSerializer, TagSerializer


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = TagSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RecipeSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    filterset_fields = (
        'is_favorited',
        'author',
        'is_in_shopping_cart',
        'tags',
    )
    pagination_class = PageLimitPagination

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method in ('POST', 'PATCH'):
            return RecipeCreateSerializer
        return super().get_serializer_class()
