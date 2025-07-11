from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import EmailCampaign
from .serializers import EmailCampaignSerializer

class EmailCampaignListCreateView(generics.ListCreateAPIView):
    queryset = EmailCampaign.objects.all()
    serializer_class = EmailCampaignSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['name', 'subject', 'content']
    ordering_fields = ['scheduled_time', 'sent_time', 'created_at']
    ordering = ['-scheduled_time']

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class EmailCampaignRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmailCampaign.objects.all()
    serializer_class = EmailCampaignSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
