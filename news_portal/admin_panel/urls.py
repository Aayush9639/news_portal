from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('articles/', review_articles, name='review_articles'),
    path('approve/<int:id>/', approve_article, name='approve_article'),
    path('reject/<int:id>/', reject_article, name='reject_article'),
    path('users/', manage_users, name='manage_users'),
    path('edit/<int:id>/', edit_article_admin, name='edit_article_admin'),
    path('delete/<int:id>/', delete_article_admin, name='delete_article_admin'),
    path('edit_user/<int:id>/', edit_user, name='edit_user'),
    path('delete_user/<int:id>/', delete_user, name='delete_user'),
    path('ads/', review_ads, name='review_ads'),
    path('approve_ad/<int:id>/', approve_ad, name='approve_ad'),
    path('reject_ad/<int:id>/', reject_ad, name='reject_ad'),
    
    # Subscription management URLs
    path('subscriptions/plans/', manage_subscription_plans, name='manage_plans'),
    path('subscriptions/plans/add/', add_subscription_plan, name='add_plan'),
    path('subscriptions/plans/edit/<int:id>/', edit_subscription_plan, name='edit_plan'),
    path('subscriptions/plans/delete/<int:id>/', delete_subscription_plan, name='delete_plan'),
    path('subscriptions/users/', manage_user_subscriptions, name='manage_subscriptions'),
    path('subscriptions/payments/', manage_payments, name='manage_payments'),
]