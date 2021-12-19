from django.contrib.auth import get_user_model
from rest_framework import serializers

from posts.models import Post, Like


User = get_user_model()


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name'
        )


class PostSerializer(serializers.ModelSerializer):

    author = AuthorSerializer()
    likes_amount = serializers.SerializerMethodField()
    liked_by_current_user = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'author',
            'title',
            'content',
            'likes_amount',
            'liked_by_current_user'
        )

    def get_likes_amount(self, obj):
        return obj.likes.count()

    def get_liked_by_current_user(self, obj):
        user = self.context.get('user')
        if user and user.is_authenticated:
            return user in obj.likes.all()
        return False


class CreatePostSerializer(serializers.ModelSerializer):

    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = (
            'author',
            'title',
            'content',
        )


class UpdatePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            'title',
            'content',
            'draft'
        )
        extra_kwargs = {
            'title': {'required': False},
            'content': {'required': False},
            'draft': {'required': False}
        }


class CreateLikeSerializer(serializers.ModelSerializer):

    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Like
        fields = (
            'post',
            'user'
        )
