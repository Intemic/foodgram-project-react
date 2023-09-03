from django.urls import include, path
from rest_framework.routers import DefaultRouter
from djoser.views import UserViewSet as DjoserViewSet

from .views import UserViewSet

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path(
        'users/set_password/',
        DjoserViewSet.as_view({'post': 'set_password'})
    ),
    path('', include(router_v1.urls)),
]
