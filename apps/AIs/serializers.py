from rest_framework import serializers
from .models import AIConfiguration, LLMProvider, AIModel, AIAgent, AgentTask

class AIConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIConfiguration
        fields = [
            'id', 'name', 'model_name', 'temperature', 
            'max_length', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class LLMProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = LLMProvider
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class AIModelSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(source='provider.name', read_only=True)
    
    class Meta:
        model = AIModel
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class AIAgentSerializer(serializers.ModelSerializer):
    model_name = serializers.CharField(source='model.name', read_only=True)
    provider_name = serializers.CharField(source='model.provider.name', read_only=True)
    
    class Meta:
        model = AIAgent
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class AgentTaskSerializer(serializers.ModelSerializer):
    agent_name = serializers.CharField(source='agent.name', read_only=True)
    
    class Meta:
        model = AgentTask
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'completed_at')
