from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Post(models.Model):
    """The post model. I didn't define verbose name for each field,
    because the names of the fields are understandable and django
    generates names for the form automatically if we don't define verbose
    names for those. I also didn't define verbose name for the model for
    the same reason. I didn't do it for the model of the likes below too."""
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
    """The like model. It contains relation to the post model and to the
    user model. Made to save info about which user and when liked post. This
    will help to get statistic in the future."""
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
        # unique_together is defined to make sure, that a user can like a
        # post only once
        unique_together = [['post', 'user']]
