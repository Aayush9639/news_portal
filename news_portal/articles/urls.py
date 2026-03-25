from django.urls import path
from . import views

urlpatterns = [
    path('journalist-dashboard/', views.journalist_dashboard, name='journalist_dashboard'),
    path('reader-dashboard/', views.reader_dashboard, name='reader_dashboard'),
    path('submit-article/', views.submit_article, name='submit_article'),
    path('', views.article_list, name='article_list'),
    path('articles/<int:id>/', views.article_detail, name='article_detail'),
    path('edit/<int:id>/', views.edit_article, name='edit_article'),
    path('delete/<int:id>/', views.delete_article, name='delete_article'),
]