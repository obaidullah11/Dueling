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
    path('create/featured-tournament/', create_featured_tournament, name='create_featured_tournament'),
    path('create/banner-image/', create_banner_image, name='create_banner_image'),
    # URL for retrieving a specific featured tournament by id
    path('featured-tournaments/<int:pk>/', featured_tournament_detail, name='featured_tournament_detail'),

    # URL for listing all banner images
    path('banner-images/', banner_image_list, name='banner_image_list'),

    # URL for retrieving a specific banner image by id
    path('banner-images/<int:pk>/', banner_image_detail, name='banner_image_detail'),
    path('tournaments/draft/create/<int:user_id>/', TournamentViewSet.as_view({'post': 'save_draft'}), name='save_draft'),
    path('tournaments/active/', TournamentViewSet.as_view({'get': 'active'}), name='active_tournaments'),
    path('tournaments/drafts/<int:user_id>/', TournamentViewSet.as_view({'get': 'drafts'}), name='drafts_by_user'),
    path('tournaments/<int:pk>/', TournamentViewSet.as_view({'get': 'retrieve', 'put': 'update'}), name='tournament_detail'),
    path('tournaments/<int:pk>/convert_to_actual/', TournamentViewSet.as_view({'post': 'convert_to_actual'}), name='convert_draft_to_actual'),
    path('tournaments/<int:pk>/update_draft/', TournamentViewSet.as_view({'put': 'update_draft'}), name='update_draft'),
    path('tournaments/<int:tournament_id>/disqualify_user/<int:user_id>/', TournamentViewSet.as_view({'post': 'disqualify_user'})),
    path('participants/arrive-at-venue/', ParticipantViewSet.as_view({'patch': 'arrive_at_venue'}), name='arrive-at-venue'),
    path('tournaments/<int:pk>/eligible-participants/', TournamentViewSet.as_view({'get': 'eligible_participants'}), name='eligible-participants'),




    path('user/register/<int:user_id>/', register_for_tournament, name='register-for-tournament'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
