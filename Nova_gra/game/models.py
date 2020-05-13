from django.db import models
from player.models import Player

class Game(models.Model):
    name = models.CharField(max_length=150)
    host = models.CharField(max_length=10)
    is_played = models.BooleanField(default = False)
    players_ready = models.IntegerField(default =0)
    max_players = models.IntegerField(default=4)
    who_is_ready = models.ManyToManyField(Player, related_name="guys_ready", blank=True)
    first_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='pierwszy', blank=True, null=True)
    second_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='drugi', blank=True, null=True)
    third_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='trzeci', blank=True, null=True)
    forth_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='czwarty', blank=True, null=True)
    who_is_playing = models.ManyToManyField(Player, related_name="guys_playing", blank=True)



    def __str__(self):
        return self.name



class Notification(models.Model):
    name = models.CharField(max_length=150)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
