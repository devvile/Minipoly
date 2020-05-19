from django.test import SimpleTestCase
from django.urls import reverse,resolve
from game.views import detail, new, game_join, delete_room, ready, game_start, game_end


class TestUrls(SimpleTestCase):


    def test_new_is_resovled(self):
        url = reverse('new_room')
        self.assertEquals(resolve(url).func,new)

    def test_detail_is_resovled(self):
            url = reverse('detail',args=[2])
            self.assertEquals(resolve(url).func, detail)

    def test_delete_room_is_resovled(self):
        url = reverse('delete_gam',args=[2])
        self.assertEquals(resolve(url).func,delete_room)

    def test_game_join_is_resovled(self):
            url = reverse('game_join',args=[2])
            self.assertEquals(resolve(url).func, game_join)

    def test_player_ready_is_resolved(self):
            url = reverse("player_ready",args=[2])
            self.assertEquals(resolve(url).func, ready)

    def test_game_start_is_resolved(self):
        url = reverse("game_start",args=[2])
        self.assertEquals(resolve(url).func,game_start)

    def test_game_end_is_resolved(self):
        url = reverse("game_end",args=[2])
        self.assertEquals(resolve(url).func,game_end)

