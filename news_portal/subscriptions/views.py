from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import SubscriptionPlan, UserSubscription, Payment
import stripe
import uuid
from datetime import datetime, timedelta

stripe.api_key = settings.STRIPE_SECRET_KEY


def subscription_plans(request):
    plans = SubscriptionPlan.objects.filter(is_active=True)
    
    # Split features for each plan
    for plan in plans:
        plan.features_list = [f.strip() for f in plan.features.split(',') if f.strip()]
    
    user_subscription = None
    
    if request.user.is_authenticated:
        user_subscription = UserSubscription.objects.filter(user=request.user).first()
    
    return render(request, 'subscriptions/subscription_plans.html', {
        'plans': plans,
        'user_subscription': user_subscription,
    })


@login_required
def checkout(request, plan_id):
    """Checkout page for payment"""
    plan = SubscriptionPlan.objects.get(id=plan_id)
    plan.features_list = [f.strip() for f in plan.features.split(',') if f.strip()]
    
    # Get or create user subscription
    user_subscription, created = UserSubscription.objects.get_or_create(
        user=request.user,
        defaults={'plan': plan, 'payment_status': 'pending'}
    )
    
    # If plan is free, activate immediately
    if plan.price == 0:
        user_subscription.plan = plan
        user_subscription.is_active = True
        user_subscription.payment_status = 'completed'
        user_subscription.save()
        
        # Send confirmation email
        send_subscription_confirmation_email(request.user, plan)
        
        return redirect('subscription_success', subscription_id=user_subscription.id)
    
    # For paid plans, create payment intent
    try:
        stripe_customer = None
        
        # Create or retrieve Stripe customer
        if user_subscription.stripe_customer_id:
            stripe_customer = stripe.Customer.retrieve(user_subscription.stripe_customer_id)
        else:
            stripe_customer = stripe.Customer.create(
                email=request.user.email,
                name=request.user.get_full_name() or request.user.username,
                metadata={'user_id': request.user.id}
            )
            user_subscription.stripe_customer_id = stripe_customer.id
            user_subscription.save()
        
        # Create payment intent (Amount in paise for INR)
        intent = stripe.PaymentIntent.create(
            amount=int(plan.price * 100),  # Amount in paise (1 INR = 100 paise)
            currency='inr',
            customer=stripe_customer.id,
            metadata={
                'user_id': request.user.id,
                'plan_id': plan.id,
                'subscription_id': user_subscription.id
            }
        )
        
        # Store payment details
        Payment.objects.create(
            user=request.user,
            subscription=user_subscription,
            plan=plan,
            amount=plan.price,
            currency='INR',
            payment_method='stripe',
            stripe_payment_intent_id=intent.id,
            transaction_id=str(uuid.uuid4())
        )
        
        return render(request, 'subscriptions/checkout.html', {
            'plan': plan,
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
            'client_secret': intent.client_secret,
            'user_subscription': user_subscription,
        })
        
    except stripe.error.StripeError as e:
        return render(request, 'subscriptions/payment_error.html', {
            'error': str(e),
            'plan': plan,
        })


@login_required
def payment_success(request):
    """Payment success confirmation page"""
    subscription_id = request.GET.get('subscription_id')
    
    try:
        user_subscription = UserSubscription.objects.get(id=subscription_id, user=request.user)
        plan = user_subscription.plan
        plan.features_list = [f.strip() for f in plan.features.split(',') if f.strip()]
        
        # Send confirmation email
        send_subscription_confirmation_email(request.user, plan)
        
        return render(request, 'subscriptions/payment_success.html', {
            'plan': plan,
            'user_subscription': user_subscription,
        })
    except UserSubscription.DoesNotExist:
        return redirect('subscription_plans')


def payment_failed(request):
    """Payment failed page"""
    error = request.GET.get('error', 'Payment processing failed. Please try again.')
    plan_id = request.GET.get('plan_id')
    
    plan = None
    if plan_id:
        try:
            plan = SubscriptionPlan.objects.get(id=plan_id)
            plan.features_list = [f.strip() for f in plan.features.split(',') if f.strip()]
        except SubscriptionPlan.DoesNotExist:
            pass
    
    return render(request, 'subscriptions/payment_failed.html', {
        'error': error,
        'plan': plan,
    })


@login_required
def subscription_success(request, subscription_id):
    """Legacy subscription success page"""
    try:
        user_subscription = UserSubscription.objects.get(id=subscription_id, user=request.user)
        plan = user_subscription.plan
        plan.features_list = [f.strip() for f in plan.features.split(',') if f.strip()]
        
        return render(request, 'subscriptions/subscription_success.html', {
            'plan': plan,
            'user_subscription': user_subscription,
        })
    except UserSubscription.DoesNotExist:
        return redirect('subscription_plans')


@login_required
@require_POST
def webhook(request):
    """Handle Stripe webhook events"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return JsonResponse({'status': 'invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'status': 'invalid signature'}, status=400)
    
    # Handle payment_intent.succeeded
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        handle_payment_success(payment_intent)
    
    # Handle payment_intent.payment_failed
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        handle_payment_failure(payment_intent)
    
    return JsonResponse({'status': 'success'})


def handle_payment_success(payment_intent):
    """Handle successful payment"""
    try:
        payment = Payment.objects.get(stripe_payment_intent_id=payment_intent['id'])
        
        # Update payment status
        payment.payment_status = 'completed'
        payment.completed_at = datetime.now()
        payment.save()
        
        # Update subscription
        subscription = payment.subscription
        subscription.is_active = True
        subscription.payment_status = 'completed'
        subscription.last_payment_date = datetime.now()
        
        # Set expiration based on plan type
        if subscription.plan.plan_type == 'basic':
            subscription.expires_at = datetime.now() + timedelta(days=30)
        elif subscription.plan.plan_type == 'premium':
            subscription.expires_at = datetime.now() + timedelta(days=365)
        
        subscription.save()
        
        # Send confirmation email
        send_subscription_confirmation_email(payment.user, subscription.plan)
        
    except Payment.DoesNotExist:
        pass


def handle_payment_failure(payment_intent):
    """Handle failed payment"""
    try:
        payment = Payment.objects.get(stripe_payment_intent_id=payment_intent['id'])
        payment.payment_status = 'failed'
        payment.save()
        
        # Update subscription status
        subscription = payment.subscription
        subscription.payment_status = 'failed'
        subscription.save()
        
        # Send failure email
        send_payment_failure_email(payment.user, subscription.plan)
        
    except Payment.DoesNotExist:
        pass


def send_subscription_confirmation_email(user, plan):
    """Send subscription confirmation email"""
    subject = f'Subscription Confirmed - {plan.name}'
    
    html_message = render_to_string('subscriptions/email_confirmation.html', {
        'user': user,
        'plan': plan,
    })
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=True,
    )


def send_payment_failure_email(user, plan):
    """Send payment failure notification email"""
    subject = 'Payment Failed - Please Try Again'
    
    html_message = render_to_string('subscriptions/email_payment_failed.html', {
        'user': user,
        'plan': plan,
    })
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=True,
    )
