from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet

from .models import Ingredient, Favorite, Recipe, Tag
from .filters import RecipeFilter
from  core.pagination import PageLimitPagination
from .serializers import IngredientSerializer, FollowSerializer, RecipeSerializer, RecipeCreateSerializer, TagSerializer


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

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return RecipeCreateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


# class FavoriteViewSet(CreateDestroyViewSet):
#     queryset = Favorite.objects.all()
#     serializer_class = FavoriteSerializer

#     def get_queryset(self):
#         favorite = get_object_or_404(Favorite, recipe=self.kwargs.get('recipe_id'))
#         return favorite
    
#     def perform_create(self, serializer):
#         if serializer.instance.author == self.request.user:

#         recipe = get_object_or_404(Recipe, pk=self.kwargs.get('recipe_id'))
#         if self.request.user == recipe.author:
#             raise

#         serializer.save(author=self.request.user, recipe=recipe)

#     def perform_destroy(self, instance):
#         recipe = get_object_or_404(Recipe, pk=self.kwargs.get('recipe_id'))

#         return super().perform_destroy(instance)
