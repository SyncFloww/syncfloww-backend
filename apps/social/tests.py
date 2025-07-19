<<<<<<< HEAD
from django.test import TestCase

# Create your tests here.
=======
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import SocialAccount
from unittest.mock import patch

User = get_user_model()

class SocialAccountTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.social_account = SocialAccount.objects.create(
            user=self.user,
            platform='facebook',
            access_token='dummy_token',
            is_active=True
        )

    def test_list_social_accounts(self):
        url = reverse('socialaccount-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_social_account(self):
        url = reverse('socialaccount-list-create')
        data = {
            'platform': 'facebook',
            'access_token': 'new_dummy_token',
            'is_active': True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_social_account(self):
        url = reverse('socialaccount-detail', args=[self.social_account.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_social_account(self):
        url = reverse('socialaccount-detail', args=[self.social_account.id])
        data = {
            'access_token': 'updated_token'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.social_account.refresh_from_db()
        self.assertEqual(self.social_account.access_token, 'updated_token')

    def test_delete_social_account(self):
        url = reverse('socialaccount-detail', args=[self.social_account.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(SocialAccount.objects.filter(id=self.social_account.id).exists())

    @patch('apps.social.auth_providers.get_auth_provider')
    def test_social_account_connect_initiate_oauth_flow(self, mock_get_auth_provider):
        mock_provider = mock_get_auth_provider.return_value
        mock_provider.get_auth_url.return_value = 'http://fake-auth-url'
        url = reverse('socialaccount-connect')
        data = {
            'platform': 'facebook',
            'brand_id': 1,
            'auth_code': None,
            'redirect_uri': 'http://localhost/callback'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('auth_url', response.data)

    @patch('apps.social.auth_providers.get_auth_provider')
    @patch('apps.social.views.handle_social_auth_ai.delay')
    def test_social_account_connect_handle_oauth_callback(self, mock_handle_social_auth_ai, mock_get_auth_provider):
        mock_handle_social_auth_ai.return_value.id = 'task123'
        url = reverse('socialaccount-connect')
        data = {
            'platform': 'facebook',
            'brand_id': 1,
            'auth_code': 'fake_code',
            'redirect_uri': 'http://localhost/callback'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIn('task_id', response.data)
>>>>>>> f3f460e4d9735213c1a8a8cc1b9cec37ca680d72
