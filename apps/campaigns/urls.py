from django.urls import path
from .views import EmailCampaignListCreateView, EmailCampaignRetrieveUpdateDestroyView

urlpatterns = [
    path('', EmailCampaignListCreateView.as_view(), name='email-campaign-list'),
    path('<int:pk>/', EmailCampaignRetrieveUpdateDestroyView.as_view(), name='email-campaign-detail'),
]
