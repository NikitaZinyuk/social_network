from django.contrib.auth import get_user_model
from rest_framework import serializers

from posts.models import Post, Like


User = get_user_model()


class PostsSerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField(source='author.get_full_name')
    likes_amount = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id',
            'author',
            'title',
            'content',
            'likes_amount',
        )
        read_only_fields = ('author',)

    def get_likes_amount(self, obj):
        return obj.likes.count()


class LikesSerializer(serializers.ModelSerializer):

    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Like
        fields = (
            'post',
            'user',
        )
