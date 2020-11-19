from channels.db import database_sync_to_async

from .models import Game, Field
from player.models import Player


@database_sync_to_async
def get_game(self, id):
    return Game.objects.get(pk=id)