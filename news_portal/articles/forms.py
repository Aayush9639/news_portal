from django import forms
from .models import Article, Comment 

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'category', 'state', 'city']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Article Title'
                }),
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Write your article here...', 
                'rows': 10
                }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'state': forms.Select(attrs={'class': 'form-select'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control comment-textarea',
                'placeholder': 'Write your thoughts here...',
                'rows': 5
            })
        }