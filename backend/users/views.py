from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.pagination import PageLimitPagination
from .models import Follow, User
from .serializers import (FollowCreateSerializer, FollowSerializer,
                          UserCreateSerializers, UserSerializers)


class UserViewSet(DjoserViewSet):
    serializer_class = UserSerializers
    queryset = User.objects.all()
    http_method_names = ['get', 'post', 'delete']
    pagination_class = PageLimitPagination

    @action(
        detail=True,
        methods=['post', 'delete']
    )
    def subscribe(self, request, id):
        following = get_object_or_404(User, pk=id)

        if request.method == 'POST':
            serializer = FollowCreateSerializer(
                data={'user': request.user.id, 'following': following.id},
                context={'request': self.request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        cnt, obj = Follow.objects.filter(
            user=self.request.user.id,
            following=id
        ).delete()

        if cnt:
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {"errors": 'Пользователь не подписан на данного автора'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=False
    )
    def subscriptions(self, request):
        users = User.objects.filter(following__user=request.user)
        page = self.paginate_queryset(users)
        serializer = FollowSerializer(
            page,
            many=True,
            context={
                'request': self.request
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
