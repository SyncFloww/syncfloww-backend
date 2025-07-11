from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    LLMProviderViewSet,
    AIModelViewSet,
    AIAgentViewSet,
    AgentTaskViewSet
)

router = DefaultRouter()
router.register(r'llm-providers', LLMProviderViewSet)
router.register(r'ai-models', AIModelViewSet)
router.register(r'ai-agents', AIAgentViewSet)
router.register(r'agent-tasks', AgentTaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
