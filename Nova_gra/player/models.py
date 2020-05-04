from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):
    name = models.ForeignKey(User,on_delete=models.CASCADE,related_name='player_name')
    parent= models.CharField(max_length = 10)
    nick = models.CharField(max_length=10 )
    description = models.TextField(max_length = 300, null = True)

    def __str__(self):
        return self.nick
