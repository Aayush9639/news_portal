from django.urls import path
from . import views

urlpatterns = [
    path('api/recommendations/', views.get_recommendations_api, name='api_recommendations'),
    path('api/track-view/<int:article_id>/', views.track_article_view, name='track_article_view'),
    path('api/similar-articles/<int:article_id>/', views.get_similar_articles, name='similar_articles'),
]
