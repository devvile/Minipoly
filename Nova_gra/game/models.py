from django.db import models
from player.models import Player

class Game(models.Model):
    name = models.CharField(max_length=150)
    host = models.CharField(max_length=10)
    is_played = models.BooleanField(default = False)
    max_players = models.IntegerField(default=4)
    who_is_ready = models.ManyToManyField(Player, related_name="guys_ready", blank=True)
    who_is_playing = models.ManyToManyField(Player, related_name="guys_playing", blank=True)
    turn = models.IntegerField(default=1)
    turn_of_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='czyja_tura', blank=True, null=True)

    @property
    def how_many_players_ready(self):
        return self.who_is_ready.count()

    @property
    def how_many_players_playing(self):
        return self.who_is_playing.count()

    @property
    def players_ready(self):
        return list(self.who_is_ready.all())

    @property
    def players_playing(self):
        return list(self.who_is_playing.all())

    @property
    def players_playing_str(self):
        res = [i.nick for i in self.who_is_playing.all()]
        return res

    @property
    def first_player(self):
        return self.players_playing[0]

    @property
    def second_player(self):
        return self.players_playing[1]

    @property
    def third_player(self):
        return self.players_playing[2]

    @property
    def forth_player(self):
        return self.players_playing[3]


    @property
    def next_player(self):
        x = self.players_playing.index(self.turn_of_player)
        nast= x+1
        if nast > (self.how_many_players_playing - 1):
            self.turn +=1
            self.save()
            return self.players_playing[0]
        else:
            return self.players_playing[x+1]

    def __str__(self):
        return self.name



class Notification(models.Model):
    name = models.CharField(max_length=150)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class FieldType(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Field(models.Model):
    name = models.CharField(max_length=150)
    owner = models.ForeignKey(Player, on_delete= models.CASCADE,related_name='fieldOwner',null= True, default=None)
    price = models.IntegerField(default=100)
    grade = models.IntegerField(default=1)

    def __str__(self):
        return self.name


