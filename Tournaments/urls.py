# urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('create-tournament/', TournamentCreateView.as_view(), name='create-tournament'),
    path('getalltournaments/', TournamentListView.as_view(), name='tournament-list'),
    path('allgames/', GameListView.as_view(), name='game-list'),  # Add this line
    path('tournaments/<int:tournament_id>/register/', RegisterForTournamentView.as_view(), name='register_for_tournament'),
    path('scores/create/', ScoreCreateView.as_view(), name='create_score'),
    path('featured-tournaments/', featured_tournament_list, name='featured_tournament_list'),

    # URL for retrieving a specific featured tournament by id
    path('featured-tournaments/<int:pk>/', featured_tournament_detail, name='featured_tournament_detail'),

    # URL for listing all banner images
    path('banner-images/', banner_image_list, name='banner_image_list'),

    # URL for retrieving a specific banner image by id
    path('banner-images/<int:pk>/', banner_image_detail, name='banner_image_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
