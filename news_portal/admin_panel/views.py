from django.shortcuts import render, redirect
from users.models import User
from django import forms
from articles.models import Article
from articles.forms import ArticleForm
from django.shortcuts import get_object_or_404
#from advertisements.models import Advertisement
from .decorators import admin_required

@admin_required
def admin_dashboard(request):
    total_users = User.objects.count()
    total_articles = Article.objects.count()
    pending_articles = Article.objects.filter(status='pending').count()
    approved_articles = Article.objects.filter(status='approved').count()
    total_ads = 0 #Advertisement.objects.count()

    context = {
        'total_users': total_users,
        'total_articles': total_articles,
        'pending_articles': pending_articles,
        'approved_articles': approved_articles,
        'total_ads': total_ads,
    }

    return render(request, 'admin_panel/dashboard.html', context)

#article approval view
@admin_required
def review_articles(request):
   articles = Article.objects.filter(status='pending')
   return render(request, 'admin_panel/review_articles.html', {'articles': articles})


@admin_required
def approve_article(request, id):
    article = Article.objects.get(id=id)
    article.status = 'approved'
    article.save()
    return redirect('review_articles')


@admin_required
def reject_article(request, id):
    article = Article.objects.get(id=id)
    article.status = 'rejected'
    article.save()
    return redirect('review_articles')

#user management view
@admin_required
def manage_users(request):
    users = User.objects.all()
    return render(request, 'admin_panel/manage_users.html', {'users': users})

@admin_required
def edit_article_admin(request, id):
    article = get_object_or_404(Article, id=id)

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('review_articles')
    else:
        form = ArticleForm(instance=article)

    return render(request, 'admin_panel/edit_article.html', {'form': form})

@admin_required
def delete_article_admin(request, id):
    article = get_object_or_404(Article, id=id)
    article.delete()
    return redirect('review_articles')

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role']


@admin_required
def edit_user(request, id):
    user = get_object_or_404(User, id=id)

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('manage_users')
    else:
        form = UserEditForm(instance=user)

    return render(request, 'admin_panel/edit_user.html', {'form': form})

@admin_required
def delete_user(request, id):
    user = get_object_or_404(User, id=id)

    if user == request.user:
        return redirect('manage_users')
    
    user.delete()
    return redirect('manage_users')