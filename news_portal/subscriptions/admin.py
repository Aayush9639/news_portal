from django.contrib import admin
from .models import SubscriptionPlan, UserSubscription, Payment


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    """Admin interface for managing subscription plans"""
    list_display = ('name', 'plan_type', 'price', 'is_active', 'created_at')
    list_filter = ('plan_type', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('is_active',)
    
    fieldsets = (
        ('Plan Information', {
            'fields': ('name', 'plan_type', 'description')
        }),
        ('Pricing', {
            'fields': ('price',),
            'description': 'Enter price in Indian Rupees (₹)'
        }),
        ('Features', {
            'fields': ('features',),
            'description': 'Enter features separated by commas (e.g., Feature 1, Feature 2, Feature 3)'
        }),
        ('Stripe Integration', {
            'fields': ('stripe_price_id',),
            'classes': ('collapse',),
            'description': 'Stripe Price ID from your Stripe dashboard'
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    readonly_fields = ('created_at',)
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    """Admin interface for managing user subscriptions"""
    list_display = ('user', 'plan', 'payment_status', 'is_active', 'subscribed_at', 'expires_at')
    list_filter = ('plan', 'is_active', 'payment_status', 'subscribed_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('subscribed_at', 'stripe_customer_id', 'stripe_subscription_id')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Subscription Details', {
            'fields': ('plan', 'is_active', 'subscribed_at', 'expires_at')
        }),
        ('Payment Status', {
            'fields': ('payment_status', 'last_payment_date')
        }),
        ('Stripe Information', {
            'fields': ('stripe_customer_id', 'stripe_subscription_id'),
            'classes': ('collapse',),
            'description': 'Stripe customer and subscription IDs'
        }),
    )
    
    def has_add_permission(self, request):
        """Subscriptions should be created through checkout, not admin"""
        return False


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Admin interface for managing payments"""
    list_display = ('user', 'amount', 'currency', 'payment_status', 'payment_method', 'created_at')
    list_filter = ('payment_status', 'payment_method', 'currency', 'created_at')
    search_fields = ('user__username', 'user__email', 'transaction_id', 'stripe_payment_intent_id')
    readonly_fields = ('transaction_id', 'stripe_payment_intent_id', 'created_at', 'completed_at')
    
    fieldsets = (
        ('User & Plan Information', {
            'fields': ('user', 'subscription', 'plan')
        }),
        ('Payment Details', {
            'fields': ('amount', 'currency', 'payment_method', 'payment_status')
        }),
        ('Transaction IDs', {
            'fields': ('transaction_id', 'stripe_payment_intent_id'),
            'classes': ('collapse',),
            'description': 'Transaction and payment intent IDs'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        """Payments should be created through checkout, not admin"""
        return False
