from django.urls import path
from .views import (
    AIConfigurationListCreateView,
    AIConfigurationRetrieveUpdateDestroyView,
    AIContentGenerationView,
    AIViralAnalysisView,
    AIContentCalendarView,
    AIStatsAnalysisView,
    AIFormAssistantView
)

urlpatterns = [
    path('configurations/', AIConfigurationListCreateView.as_view(), name='ai-config-list'),
    path('configurations/<int:pk>/', AIConfigurationRetrieveUpdateDestroyView.as_view(), name='ai-config-detail'),
    path('generate-content/', AIContentGenerationView.as_view(), name='ai-content-gen'),
    path('viral-analysis/', AIViralAnalysisView.as_view(), name='ai-viral-analysis'),
    path('content-calendar/', AIContentCalendarView.as_view(), name='ai-content-calendar'),
    path('stats-analysis/', AIStatsAnalysisView.as_view(), name='ai-stats-analysis'),
    path('form-assistant/', AIFormAssistantView.as_view(), name='ai-form-assistant'),
]
