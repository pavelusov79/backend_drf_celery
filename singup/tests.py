from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class TestCaseUser(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='user1', email='user1@example.com', password='12345')

    def test_token_autogenerate(self):
        token = Token.objects.filter(user=self.user).first()
        self.assertTrue(token)

    def test_login(self):
        response = self.client.get('/api-auth/login/', {"username": self.user.username, "password": self.user.password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
