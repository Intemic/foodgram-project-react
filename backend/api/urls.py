from django.urls import include, path
from rest_framework.routers import DefaultRouter

from foods.views import IngredientViewSet, RecipeViewSet, TagViewSet

router_v1 = DefaultRouter()
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')
router_v1.register('recipes', RecipeViewSet, basename='recipes')

users_url = [
    path('', include('users.urls'))
]

auth_urls = [
    path('auth/', include('djoser.urls.authtoken'))
]

urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include(auth_urls)),
    path('', include(users_url))
]
