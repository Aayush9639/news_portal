from django.test import TestCase
from django.contrib.auth.models import User
from articles.models import Article, Category
from .models import UserPreference, ArticleInteraction
from .services import AIRecommendationEngine


class AIRecommendationTestCase(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password123')
        self.category = Category.objects.create(name='Technology')
        self.article1 = Article.objects.create(
            title='Test Article 1',
            content='Content 1',
            category=self.category,
            status='published',
            author=self.user
        )
        self.article2 = Article.objects.create(
            title='Test Article 2',
            content='Content 2',
            category=self.category,
            status='published',
            author=self.user
        )
    
    def test_track_interaction(self):
        interaction = AIRecommendationEngine.track_interaction(
            self.user,
            self.article1,
            'view',
            30
        )
        self.assertEqual(interaction.duration_seconds, 30)
    
    def test_get_recommendations(self):
        AIRecommendationEngine.track_interaction(self.user, self.article1, 'view', 30)
        recommendations = AIRecommendationEngine.get_recommendations(self.user)
        self.assertGreater(len(recommendations), 0)
    
    def test_get_similar_articles(self):
        similar = AIRecommendationEngine.get_similar_articles(self.article1)
        self.assertGreater(len(similar), 0)
