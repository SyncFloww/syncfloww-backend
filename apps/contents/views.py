from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Content
from .serializers import ContentSerializer
from apps.ai.services import AIService
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend



ai_service = AIService()

class ContentListCreateView(generics.ListCreateAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ContentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class AIContentGenerationView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        prompt = request.data.get('prompt')
        max_length = request.data.get('max_length', 100)
        
        if not prompt:
            return Response(
                {'error': 'Prompt is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        generated_text = ai_service.generate_content(prompt, max_length=max_length)
        
        if not generated_text:
            return Response(
                {'error': 'Failed to generate content'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
        return Response({'generated_text': generated_text})


class ContentListCreateView(generics.ListCreateAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['content_type', 'status']
    search_fields = ['title', 'text']
    ordering_fields = ['scheduled_time', 'published_time', 'created_at']
    ordering = ['-scheduled_time']

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ContentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
