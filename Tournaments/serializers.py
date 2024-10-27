# serializers.py
from rest_framework import serializers
from .models import *

from rest_framework import serializers
from .models import Tournament, Game
from users.models import User

class TournamentSerializer(serializers.ModelSerializer):
    game_name = serializers.CharField(write_only=True)  # Field for passing the game name
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)  # User creating the tournament

    class Meta:
        model = Tournament
        fields = [
            'id','tournament_name', 'email_address', 'contact_number',
            'event_date', 'event_start_time', 'last_registration_date',
            'tournament_fee', 'banner_image', 'game_name', 'is_draft', 'created_by'
        ]
    
    def create(self, validated_data):
        # Extract game_name and remove it from validated_data
        game_name = validated_data.pop('game_name')
        
        # Attempt to fetch the Game instance
        try:
            game = Game.objects.get(name=game_name)
        except Game.DoesNotExist:
            raise serializers.ValidationError({
                'game_name': f"A game with the name '{game_name}' does not exist. Please provide a valid game name."
            })

        # Assign the found game instance to the 'game' field in validated_data
        validated_data['game'] = game

        # Check if created_by is provided
        if 'created_by' not in validated_data:
            raise serializers.ValidationError({'created_by': 'This field is required.'})

        # Call the super class create method with updated validated_data
        return super().create(validated_data)

class DraftTournamentSerializer(serializers.ModelSerializer):
    game_name = serializers.CharField(write_only=True)  # Field for passing the game name

    class Meta:
        model = Tournament
        fields = [
            'id','tournament_name', 'email_address', 'contact_number',
            'event_date', 'event_start_time', 'last_registration_date',
            'tournament_fee', 'banner_image', 'game_name', 'is_draft'
        ]
    
    def create(self, validated_data):
        # Extract game_name and remove it from validated_data
        game_name = validated_data.pop('game_name')
        
        # Attempt to fetch the Game instance
        try:
            game = Game.objects.get(name=game_name)
        except Game.DoesNotExist:
            raise serializers.ValidationError({
                'game_name': f"A game with the name '{game_name}' does not exist. Please provide a valid game name."
            })

        # Assign the found game instance to the 'game' field in validated_data
        validated_data['game'] = game

        # Set is_draft to True for draft tournaments
        validated_data['is_draft'] = True

        # Call the super class create method with updated validated_data
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Extract game_name if provided
        game_name = validated_data.pop('game_name', None)

        # Attempt to fetch the Game instance if game_name is provided
        if game_name:
            try:
                game = Game.objects.get(name=game_name)
                validated_data['game'] = game
            except Game.DoesNotExist:
                raise serializers.ValidationError({
                    'game_name': f"A game with the name '{game_name}' does not exist. Please provide a valid game name."
                })

        # Update the instance with the validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance



class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'name','image']  # Include other fields if necessary

class getTournamentSerializer(serializers.ModelSerializer):
    game_name = serializers.CharField(source='game.name', read_only=True)  # Include game name

    class Meta:
        model = Tournament
        # Updated fields list with new fields
        fields = [
            'tournament_name', 'email_address', 'contact_number', 
            'event_date', 'event_start_time', 'last_registration_date', 
            'tournament_fee', 'banner_image', 'game_name'
        ]
class ParticipantSerializer(serializers.ModelSerializer):
    tournament_name = serializers.CharField(source='tournament.tournament_name', read_only=True)
    deck_name = serializers.CharField(source='deck.name', read_only=True)
    class Meta:
        model = Participant
        fields = ['id', 'user', 'tournament_name', 'deck_name', 'registration_date', 'payment_status', 'total_score']

class TournamentSerializernew(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True, read_only=True)  # Include participants

    class Meta:
        model = Tournament
        fields = [
            'id', 
            'tournament_name', 
            'email_address', 
            'contact_number',
            'event_date', 
            'event_start_time', 
            'last_registration_date',
            'tournament_fee', 
            'banner_image', 
            'is_draft',
            'participants'  # Add this line
        ]
class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = '__all__'

class FeaturedTournamentSerializer(serializers.ModelSerializer):
    tournament = TournamentSerializer()

    class Meta:
        model = FeaturedTournament
        fields = ['id', 'tournament', 'is_featured', 'featured_date']

class createFeaturedTournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeaturedTournament
        fields = ['id', 'is_featured', 'featured_date']

class BannerImageSerializer(serializers.ModelSerializer):
    tournament = TournamentSerializer()

    class Meta:
        model = BannerImage
        fields = ['id', 'tournament', 'image', 'uploaded_at']

class newBannerImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerImage
        fields = ['tournament', 'image']  # Include tournament ID and image field
    
    def validate_tournament(self, value):
        if not value:
            raise serializers.ValidationError("Tournament is required.")
        return value

    def validate_image(self, value):
        if not value:
            raise serializers.ValidationError("Image file is required.")
        return value