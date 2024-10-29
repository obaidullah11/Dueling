# views.py
from rest_framework import generics
from rest_framework import status
from .models import Tournament
from rest_framework.views import APIView
from .serializers import *
from django.shortcuts import get_object_or_404
from .utils import api_response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Tournament
from .serializers import TournamentSerializer, DraftTournamentSerializer

@api_view(['POST'])
def create_banner_image(request):
    serializer = newBannerImageSerializer(data=request.data)
    if serializer.is_valid():
        banner_image = serializer.save()
        return Response({
            'success': True,
            'message': 'Banner image uploaded successfully.',
            'data': BannerImageSerializer(banner_image).data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'message': 'Failed to upload banner image.',
        'data': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
def create_featured_tournament(request):
    print("Received request data:", request.data)  # Print incoming request data

    tournament_id = request.data.get('tournament')
    print("Extracted tournament ID:", tournament_id)  # Print extracted tournament ID

    if tournament_id is None:
        print("Tournament ID is missing.")  # Print if tournament ID is missing
        return Response({
            'success': False,
            'message': 'Tournament ID is required.',
            'data': {}
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        tournament = Tournament.objects.get(id=tournament_id)
        print("Tournament found:", tournament)  # Print found tournament

        # Check if the tournament is already featured
        if FeaturedTournament.objects.filter(tournament=tournament).exists():
            print("This tournament is already featured.")  # Print if it already exists
            return Response({
                'success': False,
                'message': 'This tournament is already featured.',
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Tournament.DoesNotExist:
        print(f"Tournament with id {tournament_id} does not exist.")  # Print error message
        return Response({
            'success': False,
            'message': f'Tournament with id {tournament_id} does not exist.',
            'data': {}
        }, status=status.HTTP_400_BAD_REQUEST)

    # Create FeaturedTournament object
    featured_tournament = FeaturedTournament(
        tournament=tournament,
        is_featured=request.data.get('is_featured', False),
        featured_date=request.data.get('featured_date'),
    )

    try:
        featured_tournament.save()  # Save the object
        print("Featured tournament created successfully:", featured_tournament)  # Print success message
        return Response({
            'success': True,
            'message': 'Featured tournament created successfully.',
            'data': createFeaturedTournamentSerializer(featured_tournament).data
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        print("Error occurred while creating featured tournament:", str(e))  # Print error message
        return Response({
            'success': False,
            'message': 'Failed to create featured tournament.',
            'data': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


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
    


# views.py






@api_view(['POST'])
def register_for_tournament(request, user_id):
    tournament_id = request.data.get('tournament')  # Get tournament ID from the request
    deck_id = request.data.get('deck')  # Get deck ID from the request

    # Check if the tournament and deck exist
    try:
        tournament = Tournament.objects.get(id=tournament_id)
        deck = Deck.objects.get(id=deck_id)
    except (Tournament.DoesNotExist, Deck.DoesNotExist) as e:
        return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the participant already exists
    existing_participant = Participant.objects.filter(user_id=user_id, tournament=tournament).first()
    if existing_participant:
        return Response({
            "success": False,
            "message": "You are already registered for this tournament.",
            "data": ParticipantSerializer(existing_participant).data
        }, status=status.HTTP_400_BAD_REQUEST)

    # Create the participant
    participant = Participant.objects.create(
        user_id=user_id,
        tournament=tournament,
        deck=deck
    )

    # Serialize the participant to return the response
    serializer = ParticipantSerializer(participant)

    return Response({
        "success": True,
        "message": "Registration successful.",
        "data": serializer.data
    })


class TournamentViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        """API to retrieve a specific tournament."""
        tournament = self.get_tournament(pk)
        if tournament:
            serializer = TournamentSerializer(tournament)
            return Response({
                'success': True,
                'message': 'Tournament retrieved successfully.',
                'data': serializer.data
            })
        return Response({
            'success': False,
            'message': 'Tournament not found.',
            'data': None
        }, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        """API to update an existing tournament."""
        tournament = self.get_tournament(pk)
        if tournament:
            serializer = TournamentSerializer(tournament, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'success': True,
                    'message': 'Tournament updated successfully.',
                    'data': serializer.data
                })
            return Response({
                'success': False,
                'message': 'Validation error.',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'success': False,
            'message': 'Tournament not found.',
            'data': None
        }, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    

    def save_draft(self, request, user_id):
        """API to save tournament as draft with user ID from URL."""
        
        # Get the user instance from the user_id provided in the URL
        user = get_object_or_404(User, pk=user_id)

        # Proceed with the serializer
        serializer = DraftTournamentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=user)  # Use the fetched user instance
            return Response({
                'success': True,
                'message': 'Draft tournament saved successfully.',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'message': 'Validation error.',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def drafts(self, request, user_id):
        """API to get draft tournaments by user ID."""
        drafts = Tournament.objects.filter(created_by=user_id, is_draft=True)
        serializer = DraftTournamentSerializer(drafts, many=True)
        return Response({
            'success': True,
            'message': 'Draft tournaments retrieved successfully.',
            'data': serializer.data
        })

    @action(detail=False, methods=['get'])
    def active(self, request):
        """API to get all tournaments where is_draft is False along with paid participants and disqualified players."""
        active_tournaments = Tournament.objects.filter(is_draft=False)

        tournaments_data = []
        for tournament in active_tournaments:
            # Filter participants who have paid and are not disqualified
            paid_participants = Participant.objects.filter(
                tournament=tournament, payment_status='paid', is_disqualified=False
            ).select_related('user')
            
            # Filter participants who are disqualified
            disqualified_participants = Participant.objects.filter(
                tournament=tournament, is_disqualified=True
            ).select_related('user')

            tournament_data = TournamentSerializernew(tournament).data
            tournament_data['paid_participants'] = ParticipantSerializer(paid_participants, many=True).data
            tournament_data['disqualified_participants'] = ParticipantSerializer(disqualified_participants, many=True).data
            tournaments_data.append(tournament_data)

        return Response({
            'success': True,
            'message': 'Active tournaments retrieved successfully.',
            'data': tournaments_data
        }, status=status.HTTP_200_OK)
    @action(detail=False, methods=['get'])
    def all_tournaments(self, request):
        """API to get all tournaments where is_draft is False."""
        tournaments = Tournament.objects.filter(is_draft=False)
        
        # Serialize the tournament data
        tournament_data = TournamentSerializer(tournaments, many=True).data
        
        return Response({
            'success': True,
            'message': 'Tournaments retrieved successfully.',
            'data': tournament_data
        })
    @action(detail=False, methods=['post'], url_path='disqualify_user/(?P<user_id>[^/.]+)')
    def disqualify_user(self, request, tournament_id, user_id):
        """API to disqualify a user from a tournament."""
        try:
            # Find the participant
            participant = Participant.objects.get(tournament_id=tournament_id, user_id=user_id)
            participant.is_disqualified = True  # Set disqualified status
            participant.save()

            return Response({
                'success': True,
                'message': 'User disqualified successfully.',
                'data': ParticipantSerializer(participant).data
            }, status=status.HTTP_200_OK)

        except Participant.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Participant not found.'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    @action(detail=True, methods=['post'])
    def convert_to_actual(self, request, pk=None):
        """API to convert draft tournament to actual tournament."""
        tournament = self.get_tournament(pk)
        if tournament and tournament.is_draft:
            tournament.is_draft = False
            tournament.save()
            serializer = TournamentSerializer(tournament)
            return Response({
                'success': True,
                'message': 'Draft tournament converted to actual successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'success': False,
            'message': 'Tournament is not a draft or not found.',
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)
    @action(detail=True, methods=['get'])
    def eligible_participants(self, request, pk=None):
        """
        API to get all participants of a specific tournament where:
        - payment_status is 'paid'
        - is_disqualified is False
        - arrived_at_venue is True
        """
        try:
            tournament = Tournament.objects.get(pk=pk)
        except Tournament.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Tournament not found.'
            }, status=404)

        participants = Participant.objects.filter(
            tournament=tournament,
            payment_status='paid',
            is_disqualified=False,
            arrived_at_venue=True
        ).select_related('user')
        
        # Serialize participants
        participants_data = ParticipantSerializer(participants, many=True).data

        return Response({
            'success': True,
            'message': 'Eligible participants retrieved successfully.',
            'data': participants_data
        })
    @action(detail=True, methods=['put'])
    def update_draft(self, request, pk=None):
        """API to update draft tournament."""
        tournament = self.get_tournament(pk)
        if tournament and tournament.is_draft:
            serializer = DraftTournamentSerializer(tournament, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'success': True,
                    'message': 'Draft tournament updated successfully.',
                    'data': serializer.data
                })
            return Response({
                'success': False,
                'message': 'Validation error.',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'success': False,
            'message': 'Tournament is not a draft or not found.',
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)

    def get_tournament(self, pk):
        """Helper method to retrieve a tournament instance."""
        try:
            return Tournament.objects.get(pk=pk)
        except Tournament.DoesNotExist:
            return None


class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

    @action(detail=False, methods=['patch'], url_path='arrive-at-venue')
    def arrive_at_venue(self, request):
        """
        API endpoint for updating the 'arrived_at_venue' field 
        for a specific tournament without requiring authentication.
        """
        user_id = request.data.get('user_id')
        tournament_id = request.data.get('tournament_id')

        if not user_id or not tournament_id:
            return Response({'error': 'User ID and Tournament ID are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get the participant record for the provided user and tournament ID
            participant = Participant.objects.get(user_id=user_id, tournament_id=tournament_id)
            participant.arrived_at_venue = True
            participant.save()

            return Response({
                'success': True,
                'message': 'Arrived at venue status updated successfully.',
                'data': ParticipantSerializer(participant).data
            }, status=status.HTTP_200_OK)

        except Participant.DoesNotExist:
            return Response({'error': 'Participant not found for this tournament.'}, status=status.HTTP_404_NOT_FOUND)


class UpdateFeaturedTournamentView(APIView):
    def patch(self, request, tournament_id):
        try:
            tournament = Tournament.objects.get(id=tournament_id)
        except Tournament.DoesNotExist:
            return Response({'error': 'Tournament not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Toggle the featured status
        tournament.featured = not tournament.featured  # If True -> False, if False -> True
        tournament.save()

        serializer = TournamentSerializer(tournament)
        return Response({
            'success': True,
            'message': 'Featured status updated successfully.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)