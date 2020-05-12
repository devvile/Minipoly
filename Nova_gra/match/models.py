from django.db import models
from player.models import Player

class Match(models.Model):
    name = models.CharField(max_length=30)
    first_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='pierwszy', blank=True, null=True)
    second_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='drugi', blank=True, null=True)
    third_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='trzeci', blank=True, null=True)
    forth_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='czwarty', blank=True, null=True)
    Turn = models.IntegerField(default=1)
    how_many_players_play = models.IntegerField(default=2)
    is_played = models.BooleanField(default=False)
    who_is_playing = models.ManyToManyField(Player, related_name="players_playing", blank=True)

    def __str__(self):
        return self.name

