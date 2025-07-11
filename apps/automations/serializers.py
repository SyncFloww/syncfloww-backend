from rest_framework import serializers
from .models import LLMProvider, AIModel, AIAgent, AgentTask

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
