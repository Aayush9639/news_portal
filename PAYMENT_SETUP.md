# Payment Gateway Setup Guide

## 🎯 What Has Been Added

Your Django News Portal now has a complete payment gateway system with:

### ✅ Features Implemented:

1. **Stripe Payment Integration**
   - Secure payment processing
   - Real-time payment status tracking
   - Webhook support for payment confirmations

2. **Email Notifications**
   - Subscription confirmation emails
   - Payment failure notifications
   - HTML email templates

3. **Payment Pages**
   - Checkout page with Stripe card form
   - Payment success page with subscription details
   - Payment failure page with helpful troubleshooting

4. **Database Models**
   - Payment model to track all transactions
   - Enhanced UserSubscription with payment tracking
   - Payment status management

5. **Professional UI**
   - All CSS in style.css (no inline styles)
   - Responsive design
   - Modern gradient headers

---

## 🔧 Setup Instructions

### Step 1: Install Stripe Package
```bash
pip install -r requirements.txt
```

### Step 2: Get Stripe API Keys

1. Go to [Stripe Dashboard](https://dashboard.stripe.com/)
2. Sign up or log in
3. Navigate to Developers → API Keys
4. Copy your **Publishable Key** and **Secret Key**

### Step 3: Update Django Settings

Edit `news_portal/news_portal/settings.py`:

```python
STRIPE_PUBLIC_KEY = 'pk_test_your_public_key_here'  # Replace
STRIPE_SECRET_KEY = 'sk_test_your_secret_key_here'  # Replace
STRIPE_WEBHOOK_SECRET = 'whsec_test_your_webhook_secret'  # Replace (optional for now)
```

### Step 4: Create Migrations

```bash
python manage.py makemigrations subscriptions
python manage.py migrate subscriptions
```

### Step 5: Create Subscription Plans (if not already done)

```bash
python manage.py shell
```

```python
from subscriptions.models import SubscriptionPlan

# Free Plan
SubscriptionPlan.objects.create(
    name='7 Days Trial',
    plan_type='free',
    price=0,
    description='Get 7 days free access to all articles',
    features='Access to all articles, Daily news updates, Ad-free reading'
)

# Basic Plan
SubscriptionPlan.objects.create(
    name='Monthly Plan',
    plan_type='basic',
    price=9.99,
    description='Unlimited access for full month',
    features='Unlimited article access, Ad-free reading, Exclusive content, Email newsletter, Save articles'
)

# Premium Plan
SubscriptionPlan.objects.create(
    name='Yearly Plan',
    plan_type='premium',
    price=99.99,
    description='Best value - full year access',
    features='Unlimited article access, Ad-free reading, Exclusive content, Email newsletter, Save articles, Priority support'
)

exit()
```

---

## 📧 Email Configuration

Email is already configured in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = '1aayush.chaurasiya@gmail.com'
EMAIL_HOST_PASSWORD = 'okfemamksigohkvk'
DEFAULT_FROM_EMAIL = 'noreply@mynewsportal.com'
```

**Note:** These are Gmail SMTP settings. Make sure to use an [App Password](https://support.google.com/accounts/answer/185833) for security.

---

## 🔗 URL Endpoints

| URL | View | Purpose |
|-----|------|---------|
| `/subscriptions/plans/` | subscription_plans | Display all plans |
| `/subscriptions/checkout/<plan_id>/` | checkout | Payment checkout page |
| `/subscriptions/payment-success/` | payment_success | Success confirmation |
| `/subscriptions/payment-failed/` | payment_failed | Failure page |
| `/subscriptions/webhook/stripe/` | webhook | Stripe webhook receiver |

---

## 🧪 Testing Payment

### Test Card Numbers (Use with Stripe Test Mode):

- **Successful Payment:** 4242 4242 4242 4242
- **Declined Card:** 4000 0000 0000 0002
- **Requires Auth:** 4000 0025 0000 3155

Use any future expiry date and any 3-digit CVC.

---

## 📝 Templates Created

1. **checkout.html** - Payment form with Stripe card element
2. **payment_success.html** - Success confirmation page
3. **payment_failed.html** - Failure page with troubleshooting
4. **email_confirmation.html** - Subscription confirmation email
5. **email_payment_failed.html** - Payment failure notification email

---

## 💾 CSS Files

All CSS for payment pages is in: `/static/css/style.css`

### Payment CSS Classes:
- `.checkout-container` - Checkout page wrapper
- `.checkout-card` - Checkout form container
- `.card-element` - Stripe card input styling
- `.error-container` - Error page wrapper
- `.error-card` - Error message container
- `.btn-pay` - Payment button
- `.status-active` - Active subscription badge

---

## 🚀 Next Steps

1. Test with Stripe test mode using test card numbers
2. Set up Stripe webhook in dashboard
3. Deploy to production with real Stripe keys
4. Monitor transactions in Stripe dashboard

---

## ⚠️ Important Notes

- **NEVER commit real API keys to Git** - Use environment variables in production
- Test thoroughly before going live
- Review Stripe's webhook documentation for production setup
- Keep email credentials secure

---

## 📞 Support

For issues:
1. Check Stripe dashboard for payment status
2. Review Django logs for errors
3. Test email configuration separately
4. Ensure all migrations are applied

