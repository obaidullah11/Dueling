# views.py
from rest_framework import generics
from rest_framework import status
from .models import Tournament
from .serializers import *
from django.shortcuts import get_object_or_404
from .utils import api_response
from rest_framework.decorators import api_view
from rest_framework.response import Response


class GameListView(generics.ListAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get(self, request, *args, **kwargs):
        games = self.get_queryset()
        serializer = self.get_serializer(games, many=True)
        return api_response(success=True, message="Games retrieved successfully", data=serializer.data)
class TournamentListView(generics.ListAPIView):
    queryset = Tournament.objects.all()
    serializer_class = getTournamentSerializer

class TournamentCreateView(generics.CreateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return api_response(
                success=True,
                message="Tournament created successfully",
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return api_response(
                success=False,
                message="Failed to create tournament",
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
class TournamentListView(generics.ListAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return api_response(
            success=True,
            message="Tournaments retrieved successfully",
            data=serializer.data
        )
    
class RegisterForTournamentView(generics.CreateAPIView):
    serializer_class = ParticipantSerializer

    def create(self, request, *args, **kwargs):
        tournament_id = self.kwargs.get('tournament_id')
        tournament = get_object_or_404(Tournament, id=tournament_id)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            participant = serializer.save(user=request.user, tournament=tournament)
            return api_response(True, 'Successfully registered for the tournament.', ParticipantSerializer(participant).data)

        return api_response(False, 'Registration failed.', serializer.errors)

# API for creating a score for a participant
class ScoreCreateView(generics.CreateAPIView):
    serializer_class = ScoreSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            score = serializer.save()
            return api_response(True, 'Score created successfully.', ScoreSerializer(score).data)

        return api_response(False, 'Failed to create score.', serializer.errors)
@api_view(['GET'])
def featured_tournament_list(request):
    featured_tournaments = FeaturedTournament.objects.all()
    if featured_tournaments.exists():
        serializer = FeaturedTournamentSerializer(featured_tournaments, many=True)
        return Response({
            'success': True,
            'message': 'Featured tournaments retrieved successfully.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'success': False,
            'message': 'No featured tournaments found.',
            'data': []
        }, status=status.HTTP_200_OK)

# Function-based view for retrieving a specific featured tournament by id
@api_view(['GET'])
def featured_tournament_detail(request, pk):
    try:
        featured_tournament = FeaturedTournament.objects.get(pk=pk)
        serializer = FeaturedTournamentSerializer(featured_tournament)
        return Response({
            'success': True,
            'message': 'Featured tournament retrieved successfully.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    except FeaturedTournament.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Featured tournament not found.',
            'data': {}
        }, status=status.HTTP_404_NOT_FOUND)

# Function-based view for listing all banner images
@api_view(['GET'])
def banner_image_list(request):
    banner_images = BannerImage.objects.all()
    if banner_images.exists():
        serializer = BannerImageSerializer(banner_images, many=True)
        return Response({
            'success': True,
            'message': 'Banner images retrieved successfully.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'success': False,
            'message': 'No banner images found.',
            'data': []
        }, status=status.HTTP_200_OK)

# Function-based view for retrieving a specific banner image by id
@api_view(['GET'])
def banner_image_detail(request, pk):
    try:
        banner_image = BannerImage.objects.get(pk=pk)
        serializer = BannerImageSerializer(banner_image)
        return Response({
            'success': True,
            'message': 'Banner image retrieved successfully.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    except BannerImage.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Banner image not found.',
            'data': {}
        }, status=status.HTTP_404_NOT_FOUND)