# Update Subscription Plans to Indian Rupees

Run this in Django shell:

```bash
cd d:\projects\news_portal\news_portal
d:\projects\news_portal\venv\Scripts\python.exe manage.py shell
```

Then paste this code:

```python
from subscriptions.models import SubscriptionPlan

# Update existing plans or create new ones with INR prices
plans = [
    {
        'name': '7 Days Trial',
        'plan_type': 'free',
        'price': 0,
        'description': 'Get 7 days free access to all articles',
        'features': 'Access to all articles, Daily news updates, Ad-free reading'
    },
    {
        'name': 'Monthly Plan',
        'plan_type': 'basic',
        'price': 499,  # ₹499/month
        'description': 'Unlimited access for full month',
        'features': 'Unlimited article access, Ad-free reading, Exclusive content, Email newsletter, Save articles'
    },
    {
        'name': 'Yearly Plan',
        'plan_type': 'premium',
        'price': 4999,  # ₹4,999/year (saves ₹500 compared to 12 months)
        'description': 'Best value - full year access',
        'features': 'Unlimited article access, Ad-free reading, Exclusive content, Email newsletter, Save articles, Priority support'
    }
]

# Delete old USD plans and create new INR plans
SubscriptionPlan.objects.all().delete()

for plan in plans:
    SubscriptionPlan.objects.create(**plan, is_active=True)

print("✓ Subscription plans updated to Indian Rupees!")
exit()
```

This will update all plans to Indian Rupees pricing.
