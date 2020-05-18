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
        usr = self.user
        self.client.login(username='testuser', password='12345')
        self.player = Player.objects.create(name=usr, parent = usr.username, nick = 'nie')


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





# Gracz, który założył pokój/grę może usunąć go, jeżeli nie ma w nim innych graczy lub gdy gra nie jest aktywna.

# W pokoju może być maksymalnie 4 graczy.

# Każdy może zobaczyć listę wszystkich pokojów, ale wejść można do niepełnego.

# Twórca pokoju musi podać jego nazwę na etapie tworzenia pokoju.


