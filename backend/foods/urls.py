from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, FollowViewSet, RecipeViewSet, TagViewSet

router_v1 = DefaultRouter()
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')
router_v1.register('recipes', RecipeViewSet, basename='recipes')
router_v1.register('tags', TagViewSet, basename='tags')
# router_v1.register(
#     r'recipes/(?P<recipe_id>\d+)/favorite',
#     CommentViewSet,
#     basename='comments'
# )
router_v1.register(
    r'users/(?P<user_id>\d+)/subscribe',
    FollowViewSet,
    basename='subscribes'
)


urlpatterns = [
    path('', include(router_v1.urls)),
]