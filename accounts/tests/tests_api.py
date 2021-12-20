from datetime import datetime
import json

from django.test import TestCase
from django.urls import reverse
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model

from accounts.models import Activity

User = get_user_model()


class LoginTests(APITestCase):
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
        self.client = APIClient()
        self.client.login(username=self.username1, password=self.password)
        self.client.get('/api/v1/posts/')
        self.client.logout()
        self.client.login(username=self.username2, password=self.password)
        self.client.logout()

    def test_get_user_activity(self):
        response = self.client.get(reverse('accounts:user_activity', args=(1,)))
        unexpected_result = {
            'last_login': None,
            'last_request_at': None
        }
        self.assertNotEqual(Activity.objects.get(user=self.user1), None)
        result = json.loads(response.content)
        self.assertNotEqual(result, unexpected_result)
        time_pattern = "%Y-%m-%dT%H:%M:%S.%fZ"
        login_date = datetime.strptime(result['last_login'], time_pattern).date()
        last_request_date = datetime.strptime(result['last_request_at'], time_pattern).date()
        self.assertEqual(datetime.now().date(), last_request_date)
        self.assertEqual(datetime.now().date(), login_date)