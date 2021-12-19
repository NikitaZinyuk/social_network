from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from .views import PostModelViewSet, LikeModelViewSet, LikeListApiView


router = DefaultRouter()
router.register(r'posts', PostModelViewSet, basename='post')
router.register(r'like', LikeModelViewSet, basename='like')


urlpatterns = [
    path('token/', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path('analytics/', LikeListApiView.as_view(), name='analytics')
] + router.urls
