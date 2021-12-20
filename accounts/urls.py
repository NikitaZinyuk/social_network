from django.urls import path


from .views import UserActivityApiView


urlpatterns = [
    path('user_activity/<int:pk>/', UserActivityApiView.as_view(),
         name='user_activity')
]

app_name = 'accounts'
