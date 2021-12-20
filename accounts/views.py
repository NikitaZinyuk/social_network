from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveAPIView

from .serializers import UserActivitySerializer


User = get_user_model()


class UserActivityApiView(RetrieveAPIView):

    serializer_class = UserActivitySerializer
    queryset = User.objects.all()
