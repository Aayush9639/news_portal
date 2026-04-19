from django.shortcuts import render, redirect
from django.db import models
from users.models import User
from django import forms
from articles.models import Article
from articles.forms import ArticleForm
from django.shortcuts import get_object_or_404
from advertisements.models import Advertisement
from subscriptions.models import SubscriptionPlan, UserSubscription, Payment
from .decorators import admin_required

@admin_required
def admin_dashboard(request):
    total_users = User.objects.count()
    total_articles = Article.objects.count()
    pending_articles = Article.objects.filter(status='pending').count()
    approved_articles = Article.objects.filter(status='approved').count()
    total_ads = Advertisement.objects.count()
    
    # Subscription statistics
    total_subscriptions = UserSubscription.objects.count()
    active_subscriptions = UserSubscription.objects.filter(is_active=True).count()
    subscription_plans = SubscriptionPlan.objects.all()
    total_revenue = Payment.objects.filter(payment_status='completed').count()
    completed_payments = Payment.objects.filter(payment_status='completed').values('amount').aggregate(
        models.Sum('amount'))['amount__sum'] or 0

    context = {
        'total_users': total_users,
        'total_articles': total_articles,
        'pending_articles': pending_articles,
        'approved_articles': approved_articles,
        'total_ads': total_ads,
        'total_subscriptions': total_subscriptions,
        'active_subscriptions': active_subscriptions,
        'subscription_plans': subscription_plans,
        'total_revenue': total_revenue,
        'completed_payments': completed_payments,
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

@admin_required
def review_ads(request):
    ads = Advertisement.objects.filter(status='pending')
    return render(request, 'admin_panel/review_ads.html', {'ads': ads})


@admin_required
def approve_ad(request, id):
    ad = Advertisement.objects.get(id=id)
    ad.status = 'approved'
    ad.save()
    return redirect('review_ads')


@admin_required
def reject_ad(request, id):
    ad = Advertisement.objects.get(id=id)
    ad.status = 'rejected'
    ad.save()
    return redirect('review_ads')


# ========== SUBSCRIPTION MANAGEMENT VIEWS ==========

class SubscriptionPlanForm(forms.ModelForm):
    class Meta:
        model = SubscriptionPlan
        fields = ['name', 'plan_type', 'price', 'description', 'features', 'is_active', 'stripe_price_id']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Monthly Plan'}),
            'plan_type': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price in ₹', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Plan description'}),
            'features': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Comma-separated features\nE.g., Unlimited articles, Ad-free reading, Save articles'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'stripe_price_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional: Stripe Price ID'}),
        }


@admin_required
def manage_subscription_plans(request):
    """List all subscription plans"""
    plans = SubscriptionPlan.objects.all().order_by('-created_at')
    context = {'plans': plans}
    return render(request, 'admin_panel/manage_plans.html', context)


@admin_required
def add_subscription_plan(request):
    """Create a new subscription plan"""
    if request.method == 'POST':
        form = SubscriptionPlanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_plans')
    else:
        form = SubscriptionPlanForm()
    
    context = {'form': form, 'title': 'Add New Subscription Plan'}
    return render(request, 'admin_panel/edit_plan.html', context)


@admin_required
def edit_subscription_plan(request, id):
    """Edit an existing subscription plan"""
    plan = get_object_or_404(SubscriptionPlan, id=id)
    
    if request.method == 'POST':
        form = SubscriptionPlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            return redirect('manage_plans')
    else:
        form = SubscriptionPlanForm(instance=plan)
    
    context = {'form': form, 'plan': plan, 'title': 'Edit Subscription Plan'}
    return render(request, 'admin_panel/edit_plan.html', context)


@admin_required
def delete_subscription_plan(request, id):
    """Delete a subscription plan"""
    plan = get_object_or_404(SubscriptionPlan, id=id)
    
    if request.method == 'POST':
        plan.delete()
        return redirect('manage_plans')
    
    context = {'plan': plan}
    return render(request, 'admin_panel/delete_plan.html', context)


@admin_required
def manage_user_subscriptions(request):
    """List all user subscriptions"""
    subscriptions = UserSubscription.objects.all().select_related('user', 'plan').order_by('-subscribed_at')
    
    # Filter by status if provided
    status = request.GET.get('status')
    if status:
        subscriptions = subscriptions.filter(payment_status=status)
    
    context = {
        'subscriptions': subscriptions,
        'status_choices': UserSubscription.PAYMENT_STATUS,
        'selected_status': status
    }
    return render(request, 'admin_panel/manage_subscriptions.html', context)


@admin_required
def manage_payments(request):
    """List all payments"""
    payments = Payment.objects.all().select_related('user', 'plan').order_by('-created_at')
    
    # Filter by status if provided
    status = request.GET.get('status')
    if status:
        payments = payments.filter(payment_status=status)
    
    # Calculate totals
    total_count = payments.count()
    completed_count = payments.filter(payment_status='completed').count()
    total_amount = payments.filter(payment_status='completed').aggregate(
        models.Sum('amount'))['amount__sum'] or 0
    
    # Calculate success rate
    success_rate = round((completed_count / total_count * 100), 1) if total_count > 0 else 0
    
    context = {
        'payments': payments,
        'status_choices': Payment.PAYMENT_STATUS,
        'selected_status': status,
        'total_amount': total_amount,
        'total_count': total_count,
        'completed_count': completed_count,
        'success_rate': success_rate,
    }
    return render(request, 'admin_panel/manage_payments.html', context)