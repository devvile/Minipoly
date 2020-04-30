from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    name = models.CharField(max_length=150)
    host = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

