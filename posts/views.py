from django.db.models import Count
from rest_framework import permissions as rest_framework_permissions
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import mixins
from django_filters import rest_framework as rest_framework_filters

from posts import filters
from posts import permissions
from posts.serializers import (
    PostsSerializer,
    LikesSerializer,
)
from posts import models


class PostModelViewSet(viewsets.ModelViewSet):

    queryset = models.Post.objects.all()
    permission_classes = (permissions.IsAuthorOrReadOnly,)
    serializer_class = PostsSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class LikeModelViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):

    serializer_class = LikesSerializer
    queryset = models.Like.objects.all()
    permission_classes = (rest_framework_permissions.IsAuthenticated,)


class LikesCountApiView(generics.ListAPIView):

    queryset = models.Like.objects.all()
    filter_backends = (rest_framework_filters.DjangoFilterBackend,)
    filterset_class = filters.LikeFilter

    def get_analytics(self) -> dict:
        queryset = self.filter_queryset(self.get_queryset())
        return queryset.values('liked_at').annotate(
            total=Count('liked_at'))

    def list(self, request, *args, **kwargs):
        return Response(self.get_analytics())
