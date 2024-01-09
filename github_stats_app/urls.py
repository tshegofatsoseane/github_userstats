from django.urls import path
from .views import github_stats

urlpatterns = [
    path('stats/<str:username>/', github_stats, name='github_stats'),
    path('stats/<str:username>/html/', github_stats, name='github_stats_html'),
    path('stats/', github_stats, name='github_stats'),
]
