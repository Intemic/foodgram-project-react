from core.pagination import PageLimitPagination
from core.views import CreateDestroyViewSet
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Follow, User
from .serializers import (FollowCreateSerializer, FollowSerializer,
                          UserCreateSerializers, UserSerializers)


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializers
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    http_method_names = ['get', 'post', 'delete']
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

    @action(
        permission_classes=[IsAuthenticated],
        detail=True,
        methods=['post', 'delete']
    )
    def subscribe(self, request, pk):
        following = get_object_or_404(User, pk=pk)

        if request.method == 'POST':
            serializer = FollowCreateSerializer(
                data={'user': request.user.id, 'following': following.id})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        try:
            follow = Follow.objects.get(user=self.request.user.id, following=pk)
        except ObjectDoesNotExist:
            return Response(
                {"errors": 'Пользователь не подписан на данного автора'},
                status=status.HTTP_400_BAD_REQUEST)

        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        permission_classes=[IsAuthenticated],
        detail=False            
    )
    def subscriptions(self, request):
        users = request.user.follower.all()
        page = self.paginate_queryset(users)
        serializer = FollowSerializer(
            page,
            many=True,
            context={
                'recipes_limit': self.request.query_params.get('recipes_limit')
            }
        )
        return self.get_paginated_response(serializer.data)

    def get_serializer_class(self):
        if self.request.method in ('POST',):
            return UserCreateSerializers
        return super().get_serializer_class()
