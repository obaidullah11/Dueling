# serializers.py
from rest_framework import serializers
from .models import *

class TournamentSerializer(serializers.ModelSerializer):
    game_name = serializers.CharField(write_only=True)  # Field for passing the game name

    class Meta:
        model = Tournament
        fields = ['tournament_name', 'email_address', 'contact_number', 'start_date', 'end_date', 'tournament_fee', 'banner_image', 'game_name']
    
    def create(self, validated_data):
        game_name = validated_data.pop('game_name')
        try:
            game = Game.objects.get(name=game_name)
        except Game.DoesNotExist:
            raise serializers.ValidationError(f"Game with name '{game_name}' does not exist.")

        validated_data['game'] = game

        return super().create(validated_data)
    


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'name','image']  # Include other fields if necessary

class getTournamentSerializer(serializers.ModelSerializer):
    game_name = serializers.CharField(source='game.name', read_only=True)  # Include game name

    class Meta:
        model = Tournament
        fields = ['tournament_name', 'email_address', 'contact_number', 'start_date', 'end_date', 'tournament_fee', 'banner_image', 'game_name']
class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['id', 'user', 'tournament', 'deck', 'registration_date', 'payment_status', 'total_score']

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = '__all__'

class FeaturedTournamentSerializer(serializers.ModelSerializer):
    tournament = TournamentSerializer()

    class Meta:
        model = FeaturedTournament
        fields = ['id', 'tournament', 'is_featured', 'featured_date']


class BannerImageSerializer(serializers.ModelSerializer):
    tournament = TournamentSerializer()

    class Meta:
        model = BannerImage
        fields = ['id', 'tournament', 'image', 'uploaded_at']

