from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from articles.models import Article
from .services import AIRecommendationEngine
from .models import ArticleInteraction


def get_recommendations_api(request):
    """API endpoint to get article recommendations"""
    limit = request.GET.get('limit', 5)
    recommendations = AIRecommendationEngine.get_recommendations(request.user, int(limit))
    
    data = {
        'articles': [
            {
                'id': article.id,
                'title': article.title,
                'category': article.category.name,
                'excerpt': article.content[:100],
                'image': article.image.url if article.image else '',
            }
            for article in recommendations
        ]
    }
    
    return JsonResponse(data)


@login_required
def track_article_view(request, article_id):
    """Track when user views an article"""
    article = get_object_or_404(Article, id=article_id)
    duration = request.POST.get('duration', 0)
    
    AIRecommendationEngine.track_interaction(
        request.user,
        article,
        'view',
        int(duration)
    )
    
    return JsonResponse({'status': 'tracked'})


def get_similar_articles(request, article_id):
    """Get articles similar to the specified article"""
    article = get_object_or_404(Article, id=article_id)
    limit = request.GET.get('limit', 3)
    
    similar = AIRecommendationEngine.get_similar_articles(article, int(limit))
    
    data = {
        'articles': [
            {
                'id': art.id,
                'title': art.title,
                'category': art.category.name,
                'excerpt': art.content[:100],
            }
            for art in similar
        ]
    }
    
    return JsonResponse(data)
