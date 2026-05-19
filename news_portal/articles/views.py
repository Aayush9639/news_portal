from django.shortcuts import render, redirect
from .forms import ArticleForm, CommentForm
from .models import Article, Comment, INDIAN_STATES, INDIAN_CITIES
from django.contrib.auth.decorators import login_required
from users.decorators import role_required
from django.shortcuts import get_object_or_404
from ai_assistant.services import AIRecommendationEngine
from django.db.models import Q

@login_required
@role_required(['journalist'])
def journalist_dashboard(request):
    articles = Article.objects.filter(journalist=request.user)

    return render(request, 'articles/journalist_dashboard.html', {
        'articles': articles
    })

@login_required
@role_required(['reader'])
def reader_dashboard(request):
    articles = Article.objects.filter(status='approved').order_by('-created_at')[:5]
    
    # Get AI recommendations
    recommendations = AIRecommendationEngine.get_recommendations(request.user, limit=4)
    trending = AIRecommendationEngine.get_trending_articles(limit=3)

    context = {
        'articles': articles,
        'total_articles': Article.objects.filter(status='approved').count(),
        'total_categories': Article.objects.filter(status='approved').values('category').distinct().count(),
        'recommended_articles': recommendations,
        'trending_articles': trending,
    }
    return render(request, 'articles/reader_dashboard.html', context)

@login_required
@role_required(['journalist'])
def submit_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)

        if form.is_valid():
            article = form.save(commit=False)

            # IMPORTANT
            article.journalist = request.user
            article.status = 'pending'

            article.save()

            return redirect('journalist_dashboard')
    else:
        form = ArticleForm()

    return render(request, 'articles/submit_article.html', {'form': form})

@login_required
@role_required(['journalist'])
def edit_article(request, id):
    article = get_object_or_404(Article, id=id, journalist=request.user)

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('journalist_dashboard')
    else:
        form = ArticleForm(instance=article)

    return render(request, 'articles/edit_article.html', {'form': form})

@login_required
@role_required(['journalist'])
def delete_article(request, id):
    article = get_object_or_404(Article, id=id, journalist=request.user)

    if request.method == 'POST':
        article.delete()
        return redirect('journalist_dashboard')

    return render(request, 'articles/delete_article.html', {'article': article})

def article_list(request):
    articles = Article.objects.filter(status='approved').order_by('-created_at')
    
    # Filter by category if provided
    category_id = request.GET.get('category')
    if category_id:
        articles = articles.filter(category_id=category_id)
    
    # Filter by state if provided
    state = request.GET.get('state')
    if state:
        articles = articles.filter(state=state)
    
    # Filter by city if provided
    city = request.GET.get('city')
    if city:
        articles = articles.filter(city=city)
    
    return render(request, 'articles/article_list.html', {
        'articles': articles,
        'selected_category': category_id,
        'selected_state': state,
        'selected_city': city,
        'states': INDIAN_STATES,
        'cities': INDIAN_CITIES,
    })

@login_required
def article_detail(request, id):
    article = get_object_or_404(Article, id=id)

    # 🔒 ACCESS CONTROL
    if article.status != 'approved':
        if request.user.role == 'admin':
            pass  # admin can see all
        elif article.journalist == request.user:
            pass  # journalist can see own article
        else:
            return redirect('article_list')  # block others

    comments = Comment.objects.filter(article=article).order_by('-created_at')
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.article = article
            comment.save()
            return redirect('article_detail', id=id)
    else:
        form = CommentForm()

    return render(request, 'articles/article_detail.html', {
        'article': article,
        'form': form,
        'comments': comments
    })


def search_articles(request):
    """Search articles by keywords"""
    query = request.GET.get('q', '')
    articles = []
    
    if query:
        articles = Article.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(category__name__icontains=query),
            status='approved'
        ).order_by('-created_at')
    
    return render(request, 'articles/search_results.html', {
        'articles': articles,
        'query': query,
        'total_results': articles.count()
    })