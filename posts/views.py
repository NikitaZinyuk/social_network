from django.db.models import Count
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.generics import ListAPIView
from django_filters import rest_framework as filters

from .filters import LikeFilter
from .permissions import IsPostOwner
from .serializers import (
    PostSerializer,
    CreatePostSerializer,
    UpdatePostSerializer,
    CreateLikeSerializer
)
from .models import Post, Like


class PostModelViewSet(ModelViewSet):

    queryset = Post.objects.filter(draft=False)
    permission_classes = (IsPostOwner,)

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


class LikeModelViewSet(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    """As we need only create and delete like object, we inherit two
    mixins for these actions and GenericViewSet"""

    serializer_class = CreateLikeSerializer
    queryset = Like.objects.all()
    permission_classes = (permissions.IsAuthenticated,)


class LikeListApiView(ListAPIView):

    queryset = Like.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = LikeFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.values('liked_at').annotate(total=Count('liked_at'))
        return Response(queryset)
