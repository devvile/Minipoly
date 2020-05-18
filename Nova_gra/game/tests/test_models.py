from game.models import Game
from player.models import Player
from django.test import TestCase
from django.contrib.auth.models import User

class TestModels(TestCase):

    def setUp(self):
        Game.objects.create(name='gra1',host='dottore')
        Game.objects.create(name='gra2', host='dottore')
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user2 = User.objects.create_user(username='testuser2', password='12345')
        self.user3 = User.objects.create_user(username='testuser3', password='12345')
        self.player= Player.objects.create(name=self.user,parent='testuser',nick='testuser')
        self.player2 = Player.objects.create(name=self.user2, parent='testuser2', nick='testuser2')
        self.player3 = Player.objects.create(name=self.user3, parent='testuser3', nick='testuser3')

    def test_how_many_players_ready(self):
        game1 = Game.objects.get(name='gra1')
        game2 = Game.objects.get(name='gra2')
        game1.who_is_ready.add(self.player)
        game2.who_is_ready.add(self.player)
        game1.who_is_ready.add(self.player2)

        self.assertEquals(game1.how_many_players_ready,2)
        self.assertEquals(game2.how_many_players_ready, 1)

    def test_how_many_players_playing(self):
        game1 = Game.objects.get(name='gra1')
        game2 = Game.objects.get(name='gra2')
        game1.who_is_playing.add(self.player)
        game2.who_is_playing.add(self.player)
        game1.who_is_playing.add(self.player2)

        self.assertEquals(game1.how_many_players_playing,2)
        self.assertEquals(game2.how_many_players_playing, 1)

    def test_third_player(self):
        game1 = Game.objects.get(name='gra1')
        game1.who_is_playing.add(self.player)
        game1.who_is_playing.add(self.player2)
        game1.who_is_playing.add(self.player3)

        self.assertEquals(game1.third_player,self.player3)
