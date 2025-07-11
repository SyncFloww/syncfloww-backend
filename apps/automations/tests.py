import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'syncflow.settings.development')

import django
django.setup()

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

class AutomationsTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_automations_list(self):
        url = '/api/automations/'  # Adjust if needed
        response = self.client.get(url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED])
