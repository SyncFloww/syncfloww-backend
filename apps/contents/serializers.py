from rest_framework import serializers
from .models import Content
from social.serializers import SocialAccountSerializer

class ContentSerializer(serializers.ModelSerializer):
    social_accounts = SocialAccountSerializer(many=True, read_only=True)
    social_account_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=SocialAccount.objects.all(),
        source='social_accounts',
        write_only=True
    )

    class Meta:
        model = Content
        fields = [
            'id', 'title', 'text', 'media', 'content_type', 'status',
            'scheduled_time', 'published_time', 'created_at', 'updated_at',
            'social_accounts', 'social_account_ids'
        ]
        read_only_fields = ['id', 'published_time', 'created_at', 'updated_at', 'social_accounts']
