from datetime import datetime

from django.db import IntegrityError
from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Post, Like


User = get_user_model()


class PostsModelsTest(TestCase):

    create_like_function = Like.objects.create
    create_post_function = Post.objects.create
    date_now = datetime.now().date()

    def setUp(self):
        self.user1 = User.objects.create(
            username='username',
            email='email@email.com'
        )
        self.user2 = User.objects.create(
            username='username1',
            email='email1@email.com'
        )
        self.user3 = User.objects.create(
            username='username2',
            email='email2@email.com'
        )
        self.post1 = self.create_post_function(
            author=self.user1,
            title='post1',
            content='post1'
        )
        self.post2 = self.create_post_function(
            author=self.user1,
            title='post2',
            content='post2'
        )
        self.post3 = self.create_post_function(
            author=self.user2,
            title='post3',
            content='post3'
        )

    def test_user_can_like_post_only_once(self):
        like1 = self.create_like_function(post=self.post1, user=self.user1)
        self.assertNotEqual(like1, None)

        with self.assertRaises(IntegrityError):
            like2 = self.create_like_function(post=self.post1, user=self.user1)

    def test_user_can_like_after_unlike(self):
        like1 = self.create_like_function(post=self.post1, user=self.user1)
        like1.delete()
        like2 = self.create_like_function(post=self.post1, user=self.user1)
        self.assertNotEqual(like2, None)

    def test_post_str(self):
        self.assertEqual(str(self.post1), self.post1.title)

    def test_post_likes_count(self):
        self.create_like_function(post=self.post1, user=self.user1)
        self.create_like_function(post=self.post1, user=self.user2)
        self.assertEqual(self.post1.likes.count(), 2)

    def test_user_liked_posts_count(self):
        self.create_like_function(user=self.user1, post=self.post1)
        self.assertEqual(self.user1.liked_posts.count(), 1)

    def test_autonow_add_to_like(self):
        self.assertEqual(
            self
            .create_like_function(user=self.user1, post=self.post1)
            .liked_at, self.date_now)

    def test_autonow_add_to_post(self):
        """Checks only date without time"""
        self.assertEqual(
            self.post1.created_at.date(), self.date_now
        )