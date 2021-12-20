from django.urls import path
from rest_framework.routers import DefaultRouter


from .views import PostModelViewSet, LikeModelViewSet, LikesCountApiView


router = DefaultRouter()
router.register(r'posts', PostModelViewSet, basename='post')
router.register(r'like', LikeModelViewSet, basename='like')


urlpatterns = [
    path('analytics/', LikesCountApiView.as_view(), name='analytics')
] + router.urls
