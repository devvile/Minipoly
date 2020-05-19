from django.test import TestCase, Client
from django.urls import reverse, resolve
from game.models import Game, Notification
from player.models import Player
from django.contrib.auth.models import User


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user2 = User.objects.create_user(username='testuser2', password='12345')
        self.user3 = User.objects.create_user(username='testuser3', password='12345')
        self.user4 = User.objects.create_user(username='testuser4', password='12345')
        self.user5 = User.objects.create_user(username='testuser5', password='12345')
        self.client.login(username='testuser', password='12345')
        self.player = Player.objects.create(name=self.user, parent = self.user.username, nick = 'nie')
        self.player2 = Player.objects.create(name=self.user2, parent=self.user2.username, nick='niet')
        self.player3 = Player.objects.create(name=self.user3,parent=self.user3.username,nick='pizdiet')
        self.player4 = Player.objects.create(name=self.user4, parent=self.user4.username, nick='kokoz')
        self.player5 = Player.objects.create(name=self.user5, parent=self.user5.username, nick='kokon')


    def test_authorisation(self):

        self.client.logout()
        game = Game.objects.create(name='empty', host='dottore', is_played=False, max_players=4)
        self.join_url_empty = reverse('game_join', args=[game.id])
        response = self.client.get(self.join_url_empty, follow=True)

        self.assertEqual(response.request['PATH_INFO'],'/player/login')


    def test_join_empty_room(self):

        game = Game.objects.create(name='empty',host='dottore',is_played=False,max_players=4)
        self.join_url_empty = reverse('detail', args=[game.id])
        response = self.client.get(self.join_url_empty, follow=True)
        self.assertEquals(response.request['PATH_INFO'],'/game/1/')


    def test_create_many_rooms(self):
        self.new_room=reverse('new_room')
        self.client.post(self.new_room, {'name' :'mariaczi', 'host':'mario'})
        self.client.post(self.new_room, {'name': 'mariaczi2','host':'mario'})
        self.client.post(self.new_room, {'name': 'mariaczi3', 'host': 'mario'})
        suma = Game.objects.all().count()

        self.assertEquals(suma,3)

    def test_host_delete_empty_room(self):
        game = Game.objects.create(name='empty', host='nie', is_played=False, max_players=4)
        self.delete_room = reverse('delete_gam', args=[game.id])
        self.client.get(self.delete_room, follow=True)
        suma = Game.objects.all().count()

        self.assertEquals(suma,0)

    def test_non_host_delete_empty_room(self):
        game = Game.objects.create(name='empty', host='niet', is_played=False, max_players=4)
        self.delete_room = reverse('delete_gam', args=[game.id])
        self.client.get(self.delete_room, follow=True)
        suma = Game.objects.all().count()

        self.assertEquals(suma,1)

    def test_host_delete_game_is_played_room(self):
        game = Game.objects.create(name='empty', host='nie', is_played=True, max_players=4)
        self.delete_room = reverse('delete_gam', args=[game.id])
        self.client.get(self.delete_room, follow=True)
        suma = Game.objects.all().count()

        self.assertEquals(suma, 1)

    def test_host_delete_game_full_room(self):
        game = Game.objects.create(name='full', host='nie', is_played=False, max_players=4)
        game.who_is_ready.add(self.player, self.player2, self.player3)
        self.delete_room = reverse('delete_gam', args=[game.id])
        self.client.get(self.delete_room, follow=True)
        suma = Game.objects.all().count()

        self.assertEqual(game.how_many_players_ready,3)
        self.assertNotEquals(suma, 0)

    def test_get_not_ready_in_full_room(self):
        game = Game.objects.create(name='full', host='nie', is_played=False, max_players=3)
        game.who_is_ready.add(self.player, self.player2, self.player3)
        self.ready = reverse('player_ready', args=[game.id])
        self.client.get(self.ready )

        self.assertEqual(game.how_many_players_ready, 2)

    def test_get_ready_empty_room(self):

        game = Game.objects.create(name='empty',host='dottore',is_played=False,max_players=4)
        self.get_ready = reverse('player_ready', args=[game.id])
        self.client.get(self.get_ready)
        self.assertEquals(game.how_many_players_ready,1)

    def test_get_ready_in_partially_full_room(self):
        game = Game.objects.create(name='not_full', host='niet', is_played=False, max_players=3)
        game.who_is_ready.add(self.player2, self.player3)
        self.is_ready = reverse('player_ready', args=[game.id])
        self.client.get(self.is_ready)
        self.assertEqual(game.how_many_players_ready, 3)

    def test_get_ready_in_full_room(self):
        game = Game.objects.create(name='full', host='niet', is_played=False, max_players=4)
        game.who_is_ready.add(self.player4, self.player2, self.player3, self.player5)
        self.ready = reverse('player_ready', args=[game.id])
        self.client.get(self.ready)

        self.assertEqual(game.how_many_players_ready, 4)



#Przycisk jest aktywny gdy gra się nie toczy.

#Po zakończeniu gry status gry aktualizuje się automatycznie

#Gdy jest co najmniej dwóch graczy gra może zostać uruchomiona

#Gra może zostać uruchomiona gdy gracze wcześniej zgłoszą gotowość do gry

#tury

#Gdy gra się toczy nieaktywny przycisk gotowości do gry ukrywa się, pojawia się nowy służący opuszczeniu gry.
#Po opuszczeniu gry, gracz nadal jest w pokoju i jest obserwatorem


#testy player
#Gracz może zmieniać swój nick
#Nick ma od 1 do 10 znaków
#Nick może się składać z małych i dużych liter, liczb i znaków specjalnych <>!@#$%^&*~?







