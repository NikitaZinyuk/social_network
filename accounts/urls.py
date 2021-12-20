from django.urls import path


from .views import UserActivityRetrieveApiView


urlpatterns = [
    path('user_activity/<int:pk>/', UserActivityRetrieveApiView.as_view(),
         name='user_activity')
]

app_name = 'accounts'
