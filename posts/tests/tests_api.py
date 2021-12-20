from datetime import datetime
import json

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from posts.models import Post

User = get_user_model()


class PostsAPITestCase(APITestCase):

    def setUp(self):
        self.username1 = 'username1'
        self.username2 = 'username2'
        self.password = 'noadmin21'
        self.user1 = User.objects.create(username=self.username1, is_active=True)
        self.user1.set_password(self.password)
        self.user1.save()
        self.user2 = User.objects.create(username=self.username2, is_active=True)
        self.user2.set_password(self.password)
        self.user2.save()
        self.client1 = APIClient()
        self.client1.login(
            username=self.username1, password=self.password)
        self.client2 = APIClient()
        self.client2 = self.client.login(
            username=self.username2, password=self.password)

    def test_user_create_post_api(self):
        title = 'some title'
        content = 'some content'
        response = self.client1.post(
            '/api/v1/posts/',
            {'title': title, 'content': content},
            format='json'
        )
        created_post = Post.objects.first()
        self.assertNotEqual(created_post, None)
        self.assertEqual(created_post.title, title)
        self.assertEqual(created_post.content, content)

    def test_user_like_unlike_post(self):
        title = 'some title'
        content = 'some content'
        response = self.client1.post(
            '/api/v1/posts/',
            {'title': title, 'content': content},
            format='json'
        )
        self.client1.post(
            '/api/v1/like/',
            {'post': 1},
            format='json'
        )
        response = self.client1.get(
            '/api/v1/posts/1/',
        )
        post_data = json.loads(response.content)
        self.assertEqual(post_data['likes_amount'], 1)
        self.client1.delete(
            '/api/v1/like/1/',
        )
        response = self.client1.get(
            '/api/v1/posts/1/',
        )
        new_post_data = json.loads(response.content)
        self.assertEqual(new_post_data['likes_amount'], 0)

    def test_analytics(self):
        title = 'some title'
        content = 'some content'
        self.client1.post(
            '/api/v1/posts/',
            {'title': title, 'content': content},
            format='json'
        )
        self.client1.post(
            '/api/v1/like/',
            {'post': 1},
            format='json'
        )
        response = self.client1.get(
            '/api/v1/analytics/'
        )
        date = datetime.now().date()
        response_data = json.loads(response.content)
        date_pattern = '%Y-%m-%d'
        self.assertEqual(datetime.strptime(response_data[0]['liked_at'], date_pattern).date(), date)
        self.assertEqual(response_data[0]['total'], 1)