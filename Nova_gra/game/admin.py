from django.contrib import admin

from .models import Game, Notification, Field, FieldType

from player.models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ( 'id','name','nick','in_game')

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ( 'id','name', 'host', 'players_ready', "is_played")


@admin.register(Notification)
class NoteAdmin(admin.ModelAdmin):
    list_display = ( 'id','name', 'note')

admin.site.register(Field)
admin.site.register(FieldType)



