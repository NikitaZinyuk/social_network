from django.db.models import Count
from rest_framework import permissions as rest_framework_permissions
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import generics
from django_filters import rest_framework as rest_framework_filters

from posts import filters
from posts import permissions
from posts.serializers import (
    PostSerializer,
    CreatePostSerializer,
    UpdatePostSerializer,
    CreateLikeSerializer
)
from posts import models


class PostModelViewSet(viewsets.ModelViewSet):

    queryset = models.Post.objects.filter(draft=False)
    permission_classes = (permissions.IsPostOwner,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreatePostSerializer
        if self.request.method in ('PUT', 'PATCH'):
            return UpdatePostSerializer
        return PostSerializer

    def get_serializer_context(self):
        context = super(PostModelViewSet, self).get_serializer_context()
        context.update({'user': self.request.user})
        return context


class LikeModelViewSet(viewsets.ModelViewSet):

    serializer_class = CreateLikeSerializer
    queryset = models.Like.objects.all()
    permission_classes = (rest_framework_permissions.IsAuthenticated,)


class LikeListApiView(generics.ListAPIView):

    queryset = models.Like.objects.all()
    filter_backends = (rest_framework_filters.DjangoFilterBackend,)
    filterset_class = filters.LikeFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.values('liked_at').annotate(total=Count('liked_at'))
        return Response(queryset)
