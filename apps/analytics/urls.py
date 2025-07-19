from django.urls import path
<<<<<<< HEAD

urlpatterns = []
=======
from .views import AnalyticsDataListView

urlpatterns = [
    path('', AnalyticsDataListView.as_view(), name='analytics-data-list'),
]
>>>>>>> f3f460e4d9735213c1a8a8cc1b9cec37ca680d72
