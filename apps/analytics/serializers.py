from rest_framework import serializers
from .models import AnalyticsData
from apps.social.serializers import SocialAccountSerializer

class AnalyticsDataSerializer(serializers.ModelSerializer):
    social_account = SocialAccountSerializer(read_only=True)

    class Meta:
        model = AnalyticsData
        fields = [
            'id', 'social_account', 'date', 'followers', 'following', 'likes',
            'comments', 'shares', 'impressions', 'reach', 'profile_views',
            'website_clicks', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
