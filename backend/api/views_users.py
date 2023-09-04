from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .pagination import PageLimitPagination

from users.models import Follow, User
from .serializers_users import (FollowCreateSerializer, FollowSerializer,
                          UserCreateSerializers, UserSerializers)


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializers
    queryset = User.objects.all()
    http_method_names = ['get', 'post', 'delete']
    pagination_class = PageLimitPagination

    @action(
        url_path='me',
        detail=False,
    )
    def get_me(self, request):
        serializer = UserSerializers(request.user)
        return Response(serializer.data)

    @action(
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
            follow = Follow.objects.get(
                user=self.request.user.id,
                following=pk
            )
        except ObjectDoesNotExist:
            return Response(
                {"errors": 'Пользователь не подписан на данного автора'},
                status=status.HTTP_400_BAD_REQUEST)

        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
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

    def get_permissions(self):
        if self.action == 'list' or self.action == 'create':
            return (AllowAny(),)
        return super().get_permissions()
