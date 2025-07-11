from rest_framework import serializers
from .models import EmailCampaign

class EmailCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailCampaign
        fields = [
            'id', 'name', 'subject', 'content', 'status',
            'scheduled_time', 'sent_time', 'recipient_list',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'sent_time', 'created_at', 'updated_at']
