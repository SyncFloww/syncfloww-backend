from django.urls import path
from .views import (
    ContentListCreateView, 
    ContentRetrieveUpdateDestroyView,
    AIContentGenerationView
)

urlpatterns = [
    path('', ContentListCreateView.as_view(), name='content-list'),
    path('<int:pk>/', ContentRetrieveUpdateDestroyView.as_view(), name='content-detail'),
    path('generate/', AIContentGenerationView.as_view(), name='ai-content-generation'),
]
