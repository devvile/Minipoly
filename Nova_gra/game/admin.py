from django.contrib import admin

from .models import Game, Field, FieldType, Config

from player.models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'nick', 'in_game')


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'host', 'players_ready', "is_played")


admin.site.register(Field)
admin.site.register(FieldType)
admin.site.register(Config)
