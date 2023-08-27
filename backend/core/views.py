from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin


class CreateDestroyViewSet(
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet
):
    pass