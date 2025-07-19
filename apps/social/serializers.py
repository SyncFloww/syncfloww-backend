from rest_framework import serializers
from .models import SocialAccount
from apps.core.models import Brand
from .constants import SOCIAL_PLATFORMS

class SocialAccountSerializer(serializers.ModelSerializer):
    platform = serializers.ChoiceField(choices=SOCIAL_PLATFORMS)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    
    class Meta:
        model = SocialAccount
        fields = [
            'id',
            'brand',
            'brand_name',
            'platform',
            'username',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'brand_name']
        
    def validate_brand(self, value):
        if value.user != self.context['request'].user:
            raise serializers.ValidationError("You don't own this brand.")
        return value

class SocialAuthURLSerializer(serializers.Serializer):
    platform = serializers.ChoiceField(choices=SOCIAL_PLATFORMS)
    brand_id = serializers.IntegerField()
    redirect_uri = serializers.URLField()

class SocialAuthCallbackSerializer(serializers.Serializer):
    code = serializers.CharField()
    state = serializers.CharField()
