from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FollowViewSet, UserViewSet

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')
router_v1.register(
    r'users/(?P<user_id>\d+)/subscribe',
    FollowViewSet,
    basename='subscribes'
)

urlpatterns = [
    path('', include(router_v1.urls)),
]
