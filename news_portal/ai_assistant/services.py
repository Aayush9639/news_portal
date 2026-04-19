from django.db.models import Q, Count
from articles.models import Article, Category
from .models import UserPreference, ArticleInteraction
from datetime import timedelta
from django.utils import timezone


class AIRecommendationEngine:
    """AI-powered recommendation engine for articles"""
    
    @staticmethod
    def get_recommendations(user, limit=5):
        """
        Get recommended articles based on user preferences and behavior
        """
        if not user.is_authenticated:
            return AIRecommendationEngine.get_trending_articles(limit)
        
        try:
            user_pref = UserPreference.objects.get(user=user)
        except UserPreference.DoesNotExist:
            user_pref = UserPreference.objects.create(user=user)
        
        # Get articles user hasn't read yet
        read_articles = user_pref.read_articles.all()
        
        # Find recommendations based on user's interaction patterns
        recent_interactions = ArticleInteraction.objects.filter(
            user=user,
            interaction_time__gte=timezone.now() - timedelta(days=30)
        ).values_list('article__category', flat=True).distinct()
        
        # Get preferred categories
        preferred_categories = user_pref.preferred_categories.all()
        
        recommendations = Article.objects.exclude(
            id__in=read_articles
        ).filter(
            Q(category__in=preferred_categories) |
            Q(category__in=recent_interactions) |
            Q(status='published')
        ).annotate(
            view_count=Count('articleinteraction')
        ).order_by('-created_at', '-view_count').distinct()[:limit]
        
        return recommendations if recommendations.exists() else AIRecommendationEngine.get_trending_articles(limit)
    
    @staticmethod
    def get_trending_articles(limit=5):
        """Get trending articles based on recent interactions"""
        trending = Article.objects.filter(
            status='published',
            created_at__gte=timezone.now() - timedelta(days=7)
        ).annotate(
            interaction_count=Count('articleinteraction')
        ).order_by('-interaction_count', '-created_at')[:limit]
        
        return trending
    
    @staticmethod
    def get_similar_articles(article, limit=3):
        """Get articles similar to the given article"""
        similar = Article.objects.filter(
            category=article.category,
            status='published'
        ).exclude(
            id=article.id
        ).order_by('-created_at')[:limit]
        
        return similar
    
    @staticmethod
    def track_interaction(user, article, interaction_type, duration=0):
        """Track user interaction with article"""
        interaction, created = ArticleInteraction.objects.get_or_create(
            user=user,
            article=article,
            interaction_type=interaction_type,
            defaults={'duration_seconds': duration}
        )
        
        if not created:
            interaction.duration_seconds += duration
            interaction.save()
        
        # Update user preferences based on category
        user_pref, _ = UserPreference.objects.get_or_create(user=user)
        if article.category not in user_pref.preferred_categories.all():
            user_pref.preferred_categories.add(article.category)
        
        if article not in user_pref.read_articles.all():
            user_pref.read_articles.add(article)
        
        return interaction
