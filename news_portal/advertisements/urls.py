from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', advertiser_dashboard, name='advertiser_dashboard'),
    path('create/', create_ad, name='create_ad'),
    path('edit/<int:id>/', edit_ad, name='edit_ad'),
    path('delete/<int:id>/', delete_ad, name='delete_ad'),

]