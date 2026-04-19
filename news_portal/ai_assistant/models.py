from django.db import models
from django.conf import settings
from articles.models import Article


class UserPreference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_preference')
    preferred_categories = models.ManyToManyField('articles.Category', blank=True)
    read_articles = models.ManyToManyField(Article, blank=True, related_name='read_by_users')
    preferred_keywords = models.TextField(default="", help_text="Comma separated keywords")
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} Preferences"


class ArticleInteraction(models.Model):
    INTERACTION_TYPES = [
        ('view', 'View'),
        ('read', 'Read'),
        ('save', 'Save'),
        ('share', 'Share'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    interaction_time = models.DateTimeField(auto_now_add=True)
    duration_seconds = models.IntegerField(default=0, help_text="Time spent reading in seconds")
    
    class Meta:
        unique_together = ('user', 'article', 'interaction_type')
        indexes = [
            models.Index(fields=['user', 'interaction_time']),
            models.Index(fields=['article', 'interaction_type']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.article.title} ({self.interaction_type})"
