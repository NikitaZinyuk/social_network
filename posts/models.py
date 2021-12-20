from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        max_length=100,
    )
    content = models.TextField(
        verbose_name='Content',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    draft = models.BooleanField(
        default=False,
    )
    likes = models.ManyToManyField(
        User,
        through='Like',
        related_name='liked_posts'
    )

    def __str__(self):
        return self.title


class Like(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='like_dates',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='like_dates',
        null=True
    )
    liked_at = models.DateField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = [['post', 'user']]
