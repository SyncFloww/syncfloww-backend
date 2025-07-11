import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))  # Add backend folder to path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'syncflow.settings.development')

import django
django.setup()

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

class AnalyticsTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_analytics_endpoint(self):
        url = '/api/analytics/'  # Replace with actual endpoint path if different
        response = self.client.get(url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED])
