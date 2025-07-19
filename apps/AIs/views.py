from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import AIConfiguration
from .serializers import AIConfigurationSerializer
from .services import AIService
import json

ai_service = AIService()

class AIConfigurationListCreateView(generics.ListCreateAPIView):
    """
    View for listing and creating AI configurations.
    Allows authenticated users to view their configurations and create new ones.
    """
    serializer_class = AIConfigurationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return only the configurations belonging to the current user
        """
        return AIConfiguration.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically associate the new configuration with the current user
        """
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        """
        Add request context to serializer
        """
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

class AIConfigurationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating and deleting specific AI configurations.
    Users can only access their own configurations.
    """
    serializer_class = AIConfigurationSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        """
        Ensure users can only access their own configurations
        """
        return AIConfiguration.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        """
        Custom update logic if needed
        """
        serializer.save()

    def get_serializer_context(self):
        """
        Add request context to serializer
        """
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

class AIContentGenerationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        prompt = request.data.get('prompt')
        content_type = request.data.get('type', 'text')
        
        if not prompt:
            return Response(
                {'error': 'Prompt is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if content_type == 'image':
            image_data = ai_service.generate_image(prompt)
            if image_data:
                return Response({'image': image_data})
            return Response(
                {'error': 'Failed to generate image'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        else:
            content = ai_service.generate_content(prompt)
            return Response({'content': content})

class AIViralAnalysisView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        content = request.data.get('content')
        if not content:
            return Response(
                {'error': 'Content is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        analysis = ai_service.analyze_viral_potential(content)
        return Response(analysis)

class AIContentCalendarView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        brand_industry = request.data.get('industry', 'general')
        goals = request.data.get('goals', ['increase engagement'])
        duration = request.data.get('duration', 30)
        
        calendar = ai_service.generate_content_calendar(brand_industry, goals, duration)
        return Response(calendar)

class AIStatsAnalysisView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        stats_data = request.data.get('stats', {})
        analysis = ai_service.analyze_social_stats(stats_data)
        return Response(analysis)

class AIFormAssistantView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        form_data = request.data.get('form_data', {})
        form_type = request.data.get('form_type')
        
        # Simulate form filling guidance
        guidance = {
            'steps': [
                f"Complete {field} field with your {field.replace('_', ' ')}"
                for field in form_data.keys()
            ],
            'tips': [
                "Make sure all information is accurate",
                "Double-check before submitting"
            ]
        }
        return Response(guidance)
