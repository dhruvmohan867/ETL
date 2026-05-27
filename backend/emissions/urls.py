from django.urls import path
from .views import EmissionRecordListView, DashboardStatsView

urlpatterns = [
    path('', EmissionRecordListView.as_view(), name='emission-list'),
    path('dashboard/', DashboardStatsView.as_view(), name='dashboard-stats'),
]
