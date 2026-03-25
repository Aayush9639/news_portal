from django.urls import path
from .views import advertiser_dashboard

urlpatterns = [
    path('advertiser-dashboard/', advertiser_dashboard, name='advertiser_dashboard'),
]