from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .services import AIService

User = get_user_model()

class AIServiceTests(TestCase):
    def setUp(self):
        self.ai_service = AIService()
        
    def test_content_generation(self):
        result = self.ai_service.generate_content("Test prompt")
        self.assertTrue(len(result) > 0)
        
    def test_viral_analysis(self):
        analysis = self.ai_service.analyze_viral_potential("Sample content")
        self.assertIn('score', analysis)
        self.assertIn('feedback', analysis)

class AIAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
    def test_content_generation_api(self):
        response = self.client.post(
            '/api/v1/ai/generate-content/',
            {'prompt': 'Test prompt', 'type': 'text'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('content', response.data)
        
    def test_viral_analysis_api(self):
        response = self.client.post(
            '/api/v1/ai/viral-analysis/',
            {'content': 'Sample content for analysis'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('score', response.data)
