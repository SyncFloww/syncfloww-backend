import os
import sys
from django.contrib.auth import get_user_model
from django.urls import reverse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'syncflow.settings.development')

import django
django.setup()

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

User = get_user_model()

class CoreTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_brands_list(self):
        url = '/api/brands/'  # Correct endpoint path based on main urls.py
        response = self.client.get(url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT])
