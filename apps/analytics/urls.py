from django.urls import path
from .views import AnalyticsDataListView

urlpatterns = [
    path('', AnalyticsDataListView.as_view(), name='analytics-data-list'),
]
