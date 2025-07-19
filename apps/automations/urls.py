<<<<<<< HEAD
from django.urls import path

urlpatterns = []
=======
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
>>>>>>> f3f460e4d9735213c1a8a8cc1b9cec37ca680d72
