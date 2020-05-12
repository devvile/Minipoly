from django.db import models
from player.models import Player

class Game(models.Model):
    name = models.CharField(max_length=150)
    host = models.CharField(max_length=10)
    is_played = models.BooleanField(default = False)
    players_ready = models.IntegerField(default =0)
    max_players = models.IntegerField(default=4)
    who_is_ready = models.ManyToManyField(Player, related_name="guys_ready", blank=True)


    def __str__(self):
        return self.name



class Notification(models.Model):
    name = models.CharField(max_length=150)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
