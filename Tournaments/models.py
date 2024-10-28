from django.db import models
from users.models import User

from django.core.exceptions import ValidationError


class Game(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='game_images/', blank=True, null=True)  # Optional image field

    def __str__(self):
        return self.name
# Create your models here.

class CustomImageField(models.ImageField):
    def __init__(self, *args, **kwargs):
        self.max_length = kwargs.pop('max_length', 150)
        super().__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        file_name = self.file.name
        if len(file_name) > self.max_length:
            raise ValidationError(f'Ensure this filename has at most {self.max_length} characters (it has {len(file_name)}).')
        return super().clean(*args, **kwargs)

class Tournament(models.Model):
    tournament_name = models.CharField(max_length=255)
    email_address = models.EmailField()
    contact_number = models.CharField(max_length=15)
    
    # New fields for event details
    event_date = models.DateField()  # The date when the event will occur
    event_start_time = models.TimeField()  # The start time of the event
    last_registration_date = models.DateField()  # Last date for participants to register
    
    tournament_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Optional
    banner_image = CustomImageField(upload_to='tournament_banners/', blank=True, null=True)  # Optional
    
    # Foreign key to the Game model
    venue = models.CharField(max_length=255, blank=True, null=True)  # Optional venue for the tournament
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='tournaments')
    is_draft = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tournaments', null=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    def __str__(self):
        return self.tournament_name
class Deck(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='decks')  # Foreign key to User
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='decks/')

    def __str__(self):
        return self.name

class Participant(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='participants', null=True, blank=True)  # Foreign key to Deck
    registration_date = models.DateField(auto_now_add=True)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    total_score = models.IntegerField(default=0) 
    is_disqualified = models.BooleanField(default=False)
    arrived_at_venue = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.tournament.tournament_name} ({self.payment_status})"
    
class Score(models.Model):
    Participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='scores')
    score_value = models.IntegerField()  # or DecimalField if you want to support decimal scores
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the score was recorded

    def __str__(self):
        return f"Score for {self.Participant.user.username} in {self.Participant.tournament.tournament_name}: {self.score_value}"
    
class FeaturedTournament(models.Model):
    tournament = models.OneToOneField(Tournament, on_delete=models.CASCADE, related_name='featured_tournament')
    is_featured = models.BooleanField(default=False)
    featured_date = models.DateField()

    def __str__(self):
        return f"Featured Tournament: {self.tournament.tournament_name} (Featured on {self.featured_date})"


class BannerImage(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='banner_images')
    image = models.ImageField(upload_to='tournament_banners/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Banner for {self.tournament.tournament_name} (Uploaded on {self.uploaded_at})"