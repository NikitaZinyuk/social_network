from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveAPIView

from .serializers import UserActivitySerializer


User= get_user_model()


class UserActivityRetrieveApiView(RetrieveAPIView):

    serializer_class = UserActivitySerializer
    queryset = User.objects.all()