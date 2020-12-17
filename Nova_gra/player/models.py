from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player_name')
    parent = models.CharField(max_length =10)
    nick = models.CharField(max_length=10)
    in_game = models.CharField(max_length=200,default="",null=True)
    ready = models.BooleanField(default=False)
    moved = models.BooleanField(default=False, null=True, blank=True)
    money = models.IntegerField(default=150)
    position = models.IntegerField(default=0, null=True, blank=True)
    properties = models.CharField(max_length=400, null=True, default="")
    description = models.TextField(max_length=300, null=True)


    def set_ready(self):
        self.ready = True

    def set_not_ready(self):
        self.ready = False

    def __str__(self):
        return self.nick
