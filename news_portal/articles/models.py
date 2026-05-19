from django.db import models
from django.conf import settings

# Indian States
INDIAN_STATES = [
    ('andhra_pradesh', 'Andhra Pradesh'),
    ('arunachal_pradesh', 'Arunachal Pradesh'),
    ('assam', 'Assam'),
    ('bihar', 'Bihar'),
    ('chhattisgarh', 'Chhattisgarh'),
    ('goa', 'Goa'),
    ('gujarat', 'Gujarat'),
    ('haryana', 'Haryana'),
    ('himachal_pradesh', 'Himachal Pradesh'),
    ('jharkhand', 'Jharkhand'),
    ('karnataka', 'Karnataka'),
    ('kerala', 'Kerala'),
    ('madhya_pradesh', 'Madhya Pradesh'),
    ('maharashtra', 'Maharashtra'),
    ('manipur', 'Manipur'),
    ('meghalaya', 'Meghalaya'),
    ('mizoram', 'Mizoram'),
    ('nagaland', 'Nagaland'),
    ('odisha', 'Odisha'),
    ('punjab', 'Punjab'),
    ('rajasthan', 'Rajasthan'),
    ('sikkim', 'Sikkim'),
    ('tamil_nadu', 'Tamil Nadu'),
    ('telangana', 'Telangana'),
    ('tripura', 'Tripura'),
    ('uttar_pradesh', 'Uttar Pradesh'),
    ('uttarakhand', 'Uttarakhand'),
    ('west_bengal', 'West Bengal'),
]

# Major Indian Cities
INDIAN_CITIES = [
    ('mumbai', 'Mumbai'),
    ('delhi', 'Delhi'),
    ('bangalore', 'Bangalore'),
    ('hyderabad', 'Hyderabad'),
    ('chennai', 'Chennai'),
    ('kolkata', 'Kolkata'),
    ('pune', 'Pune'),
    ('jaipur', 'Jaipur'),
    ('lucknow', 'Lucknow'),
    ('kanpur', 'Kanpur'),
    ('ahmedabad', 'Ahmedabad'),
    ('surat', 'Surat'),
    ('vadodara', 'Vadodara'),
    ('indore', 'Indore'),
    ('nagpur', 'Nagpur'),
    ('bhopal', 'Bhopal'),
    ('cochin', 'Cochin'),
    ('thiruvananthapuram', 'Thiruvananthapuram'),
    ('coimbatore', 'Coimbatore'),
    ('vizag', 'Vizag'),
    ('vijayawada', 'Vijayawada'),
    ('patna', 'Patna'),
    ('guwahati', 'Guwahati'),
    ('chandigarh', 'Chandigarh'),
    ('shimla', 'Shimla'),
]

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Article(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    
    # Location fields
    state = models.CharField(max_length=50, choices=INDIAN_STATES, default='maharashtra')
    city = models.CharField(max_length=100, choices=INDIAN_CITIES, default='mumbai')

    journalist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    publish_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.article.title}"