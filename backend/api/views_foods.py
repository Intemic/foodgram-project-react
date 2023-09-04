from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import IngredientFilter, RecipeFilter
from foods.models import Favorite, Ingredient, Recipe, ShopList, Tag
from .pagination import PageLimitPagination
from .permissions import AuthorOrReadOnly
from .serializers_foods import (FavoriteCreateSerializer, IngredientSerializer,
                                RecipeCreateSerializer, RecipeSerializer,
                                ShopListCreateSerializer, TagSerializer)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = TagSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = IngredientSerializer
    filter_backends = (IngredientFilter, )
    search_fields = ('^name',)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (AuthorOrReadOnly,)
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

    @action(
        detail=True,
        methods=['post', 'delete']
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)

        if request.method == 'POST':
            serializer = FavoriteCreateSerializer(
                data={'user': request.user.id, 'recipe': recipe.id})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        try:
            favorite = Favorite.objects.get(
                user=self.request.user.id,
                recipe=pk
            )
        except ObjectDoesNotExist:
            return Response(
                {"errors": 'Рецепт отсутствует в избранном'},
                status=status.HTTP_400_BAD_REQUEST)

        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post', 'delete']
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)

        if request.method == 'POST':
            serializer = ShopListCreateSerializer(
                data={'user': request.user.id, 'recipe': recipe.id})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        try:
            shoplist = ShopList.objects.get(
                user=self.request.user.id,
                recipe=pk
            )
        except ObjectDoesNotExist:
            return Response(
                {"errors": 'Рецепт отсутствует в списке покупок'},
                status=status.HTTP_400_BAD_REQUEST)

        shoplist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        permission_classes=[permissions.IsAuthenticated],
        detail=False,
    )
    def download_shopping_cart(self, request):
        ingredients = Ingredient.objects.filter(
            rec_ingrs__recipe__in=Recipe.objects.filter(
                shoplists__user=request.user
            )
        ).annotate(sum_amount=Sum('rec_ingrs__amount'))

        if len(ingredients) != 0:
            content = 'Ингредиент\tКол-во\tЕИ\n' + (
                '\n'.join([f'{ingredient.name}\t'
                           f'{ingredient.sum_amount}\t'
                           f'{ingredient.measurement_unit}'
                           for ingredient in ingredients]))

            response = HttpResponse(
                content,
                content_type='text/plain',
                headers={
                    "Content-Disposition":
                    'attachment; filename="Список покупок.txt"'
                },
            )

            return response

        return HttpResponse(status=status.HTTP_200_OK)
