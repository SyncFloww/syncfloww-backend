from django.urls import path
<<<<<<< HEAD

urlpatterns = []
=======
from .views import EmailCampaignListCreateView, EmailCampaignRetrieveUpdateDestroyView

urlpatterns = [
    path('', EmailCampaignListCreateView.as_view(), name='email-campaign-list'),
    path('<int:pk>/', EmailCampaignRetrieveUpdateDestroyView.as_view(), name='email-campaign-detail'),
]
>>>>>>> f3f460e4d9735213c1a8a8cc1b9cec37ca680d72
