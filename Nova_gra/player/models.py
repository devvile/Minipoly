from django.db import models
from django.contrib.auth.models import User
from game.models import Game

class Player(models.Model):
    name = models.ForeignKey(User,on_delete=models.CASCADE,related_name='player_name')
    parent= models.CharField(max_length = 10)
    nick = models.CharField(max_length=10 )
    hosted_rooms =models.ManyToManyField(Game,related_name='hosted',null=True,blank=True)
    def __str__(self):
        return self.nick
