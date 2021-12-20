from django.contrib.auth import get_user_model
from rest_framework import serializers

from posts.models import Post, Like


User = get_user_model()


class PostsSerializer(serializers.ModelSerializer):

    likes_amount = serializers.SerializerMethodField()
    liked_by_current_user = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id',
            'author',
            'title',
            'content',
            'likes_amount',
            'liked_by_current_user'
        )
        read_only_fields = ('author',)

    def get_likes_amount(self, obj):
        return obj.likes.count()

    def get_liked_by_current_user(self, obj):
        user = self.context.get('user')
        if user and user.is_authenticated:
            return user in obj.likes.all()
        return False


class CreateLikeSerializer(serializers.ModelSerializer):

    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Like
        fields = (
            'post',
            'user'
        )
