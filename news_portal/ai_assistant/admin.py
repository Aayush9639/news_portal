from django.contrib import admin
from .models import UserPreference, ArticleInteraction


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'updated_at')
    filter_horizontal = ('preferred_categories', 'read_articles')
    search_fields = ('user__username',)


@admin.register(ArticleInteraction)
class ArticleInteractionAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'interaction_type', 'interaction_time', 'duration_seconds')
    list_filter = ('interaction_type', 'interaction_time')
    search_fields = ('user__username', 'article__title')
    readonly_fields = ('interaction_time',)
