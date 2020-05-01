from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):
    name = models.ForeignKey(User,on_delete=models.CASCADE)
    parent= models.CharField(max_length = 10)
    nick = models.CharField(max_length=10)

    def __str__(self):
        return self.nick


class Game(models.Model):
    name = models.CharField(max_length=150)
    host = models.ForeignKey(User,on_delete=models.CASCADE)
    is_played = models.BooleanField(default = False)
    players_ready = models.IntegerField(default =0)
    max_players = models.IntegerField(default=4)
    want_to_play = models.ManyToManyField(Player,related_name="players_to_play")

    def __str__(self):
        return self.name

class Notification(models.Model):
    name = models.CharField(max_length=150)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
