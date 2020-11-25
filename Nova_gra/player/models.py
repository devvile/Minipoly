from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player_name')
    parent = models.CharField(max_length =10)
    nick = models.CharField(max_length=10)
    in_game = models.BooleanField(default=False)
    money = models.IntegerField(default=150)
    position = models.IntegerField(default=0)
    properties = models.CharField(max_length=400, null=True, default="")
    description = models.TextField(max_length=300, null=True)

    def set_player_in_game(self):
        self.in_game = True

    def set_player_leave_game(self):
        self.in_game = False

    def __str__(self):
        return self.nick
