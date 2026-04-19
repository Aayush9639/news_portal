#!/usr/bin/env python
"""Update subscription plans to Indian Rupees"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_portal.settings')
django.setup()

from subscriptions.models import SubscriptionPlan

# Delete old plans
SubscriptionPlan.objects.all().delete()

# Create new INR plans
plans = [
    {
        'name': '7 Days Trial',
        'plan_type': 'free',
        'price': 0,
        'description': 'Get 7 days free access to all articles',
        'features': 'Access to all articles, Daily news updates, Ad-free reading',
        'is_active': True
    },
    {
        'name': 'Monthly Plan',
        'plan_type': 'basic',
        'price': 499,
        'description': 'Unlimited access for full month',
        'features': 'Unlimited article access, Ad-free reading, Exclusive content, Email newsletter, Save articles',
        'is_active': True
    },
    {
        'name': 'Yearly Plan',
        'plan_type': 'premium',
        'price': 4999,
        'description': 'Best value - full year access',
        'features': 'Unlimited article access, Ad-free reading, Exclusive content, Email newsletter, Save articles, Priority support',
        'is_active': True
    }
]

for plan_data in plans:
    plan = SubscriptionPlan.objects.create(**plan_data)
    print(f"✓ Created: {plan.name} - ₹{plan.price}")

print("\n✓ All subscription plans updated to Indian Rupees!")
