from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    name = models.CharField(max_length=150)
    host = models.ForeignKey(User,on_delete=models.CASCADE)
    is_played = models.BooleanField(default = False)
    players_ready = models.IntegerField(default =0)
    max_players = models.IntegerField(default=4)

    def __str__(self):
        return self.name

