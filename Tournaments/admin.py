from django.contrib import admin
from .models import *

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'image')  # Display name and image in the admin list view

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    # Updated list_display to show new fields
    list_display = (
        'id', 'tournament_name', 'email_address', 'contact_number', 
        'event_date', 'event_start_time', 'last_registration_date', 
        'tournament_fee', 'game'
    )
    
    # Updated list_filter to filter by event_date and game
    list_filter = ('event_date', 'game')  
    
    # Keep the search fields as they are relevant
    search_fields = ('tournament_name', 'email_address', 'contact_number')  
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('user', 'tournament', 'registration_date', 'payment_status', 'total_score')  # Fields to display in the admin list view
    search_fields = ('user__username', 'tournament__tournament_name')  # Allow searching by user or tournament name
    list_filter = ('tournament', 'payment_status')  # Allow filtering by tournament and payment status
    ordering = ('registration_date',)  # Order participants by registration date

# Register the Participant model with the custom admin interface
admin.site.register(Participant, ParticipantAdmin)

# Create a custom admin interface for the Score model
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('Participant', 'score_value', 'created_at')  # Fields to display in the admin list view
    search_fields = ('Participant__user__username',)  # Allow searching by participant username
    list_filter = ('created_at',)  # Allow filtering by created date

# Register the Score model with the custom admin interface
admin.site.register(Score, ScoreAdmin)
class DeckAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'image']  # Customize fields to display in the admin list view
    search_fields = ['name']  # Allow searching by name

# Register the Deck model
admin.site.register(Deck, DeckAdmin)
@admin.register(FeaturedTournament)
class FeaturedTournamentAdmin(admin.ModelAdmin):
    list_display = ('id', 'tournament', 'is_featured')  
    search_fields = ('tournament__tournament_name',)     

# Register BannerImage model
@admin.register(BannerImage)
class BannerImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'tournament', 'image')         
    search_fields = ('tournament__tournament_name',) 