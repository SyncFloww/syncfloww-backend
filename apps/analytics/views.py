from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import AnalyticsData
from .serializers import AnalyticsDataSerializer
from apps.social.models import SocialAccount

class AnalyticsDataListView(generics.ListAPIView):
    serializer_class = AnalyticsDataSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['social_account__platform']
    ordering_fields = ['date', 'followers', 'likes', 'comments', 'shares']
    ordering = ['-date']

    def get_queryset(self):
        social_accounts = SocialAccount.objects.filter(user=self.request.user)
        return AnalyticsData.objects.filter(social_account__in=social_accounts)
