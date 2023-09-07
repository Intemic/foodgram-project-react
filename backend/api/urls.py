from django.urls import include, path
from djoser.views import UserViewSet as DjoserViewSet
from rest_framework.routers import DefaultRouter

from foods.views import IngredientViewSet, RecipeViewSet, TagViewSet
from users.views import UserViewSet

router_v1 = DefaultRouter()
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')
router_v1.register('recipes', RecipeViewSet, basename='recipes')
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path(
        'users/set_password/',
        DjoserViewSet.as_view({'post': 'set_password'})
    ),
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
