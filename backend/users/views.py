from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import UserCreateSerializers, UserSerializers
from core.pagination import PageLimitPagination


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializers
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    http_method_names = ['get', 'post']
    pagination_class = PageLimitPagination

    @action(
        url_path='me',
        permission_classes=[IsAuthenticated],
        detail=False,
    )
    def get_me(self, request):
        serializer = UserSerializers(request.user)
        return Response(serializer.data)

    @action(
        permission_classes=[IsAuthenticated],
        detail=False,
        methods=['post']
    )
    def set_password(self, request):
        pass

    def get_serializer_class(self):
        if self.request.method in ('POST',):
            return UserCreateSerializers
        return super().get_serializer_class()
    
    def get_paginated_response(self, data):
        return super().get_paginated_response(data)
