from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Activity(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    last_request_at = models.DateTimeField(
        auto_now=True,
    )
