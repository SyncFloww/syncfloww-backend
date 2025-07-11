import django
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.conf import settings

django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

class UserAccountTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass123')
        self.client = APIClient()

    def test_signup(self):
        url = reverse('accounts:signup')
        data = {
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signin(self):
        url = reverse('accounts:login')
        data = {
            'email': 'testuser@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_email_verification(self):
        # This test assumes email verification endpoint exists
        url = reverse('accounts:verify-email')
        # Simulate verification token or key
        data = {'key': 'dummy-verification-key'}
        response = self.client.post(url, data)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])

    def test_password_reset(self):
        url = reverse('accounts:password-reset')
        data = {'email': 'testuser@example.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
