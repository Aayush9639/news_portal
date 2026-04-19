from django.db import models
from django.conf import settings

class SubscriptionPlan(models.Model):
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('basic', 'Basic'),
        ('premium', 'Premium'),
    ]
    
    name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=20, choices=PLAN_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField()
    features = models.TextField(help_text="Comma separated features")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    stripe_price_id = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.name


class UserSubscription(models.Model):
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    # Payment tracking
    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=100, blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    last_payment_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"


class Payment(models.Model):
    PAYMENT_METHOD = [
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
    ]
    
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscription = models.ForeignKey(UserSubscription, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    
    # Payment details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD, default='stripe')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    
    # Transaction IDs
    stripe_payment_intent_id = models.CharField(max_length=100, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, unique=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.payment_status}"
