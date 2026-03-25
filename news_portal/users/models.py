from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('journalist', 'Journalist'),
        ('reader', 'Reader'),
        ('advertiser', 'Advertiser'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='reader')
    phone_number = models.CharField(max_length=15, blank=True, null=True)