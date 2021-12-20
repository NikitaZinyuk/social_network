from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class UserActivitySerializer(serializers.ModelSerializer):

    last_request_at = serializers.DateTimeField(source='activity.last_request_at')

    class Meta:
        model = User
        fields = ('last_request_at', 'last_login')
