from django.contrib import admin
from .models import Game, Notification, Player

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ( 'id','name','nick')

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ( 'id','name', 'host', 'players_ready', "is_played")


@admin.register(Notification)
class NoteAdmin(admin.ModelAdmin):
    list_display = ( 'id','name', 'note')

