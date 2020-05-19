from django.test import TestCase
from game.forms import CreateGame
from game.models import Game

class TestForms(TestCase):

    def test_create_game_form_valid_data(self):
        form = CreateGame(data= {
            'name':"SPOKO GIERKA"
        })

        self.assertTrue(form.is_valid())


    def test_create_game_form_no_data(self):
        form = CreateGame(data={
            'name': ""
        })

        self.assertFalse(form.is_valid())

    def test_create_game_form_too_long_input(self):
        form = CreateGame(data={
            'name': "TEKSTTEKSTTEKSTTEKSTTEKSTTEKSTTEKSTTEKSTTEKST TEKSTTEKSTTEKSTTEKSTTEKSTTEKSTTEKSTTEKSTTEKSTTEKSTTEKSTTE KSTTEKSTTEKSTTEKSTTEKSTTEKSTTEKSTTEKSTTEKSTTEKSTTEKSTTEKSTTEKSTT EKSTTEKSTTEKSTTEKSTTEKSTTEKSTTEKST"
        })

        self.assertFalse(form.is_valid())

    def test_create_game_form_special_charact(self):
        form = CreateGame(data={
            'name': "#!#!KEYS#$%^&*(<"
        })

        self.assertTrue(form.is_valid())
