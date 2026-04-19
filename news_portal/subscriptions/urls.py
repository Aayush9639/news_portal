from django.urls import path
from . import views

urlpatterns = [
    path('plans/', views.subscription_plans, name='subscription_plans'),
    path('checkout/<int:plan_id>/', views.checkout, name='checkout'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-failed/', views.payment_failed, name='payment_failed'),
    path('success/<int:subscription_id>/', views.subscription_success, name='subscription_success'),
    path('webhook/stripe/', views.webhook, name='stripe_webhook'),
    path('subscribe/<int:plan_id>/', views.checkout, name='subscribe'),  # Legacy URL
]