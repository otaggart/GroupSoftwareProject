from django.urls import path

from .views import leaderboard_view
from . import views

urlpatterns = [
    path("leaderboard", leaderboard_view, name="leaderboard_home"),
    path('leaderboard/submit_unity_score/', views.submit_unity_score, name='submit_unity_score')
]
