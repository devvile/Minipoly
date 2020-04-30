from django import forms
from .models import Game

class CreateGame(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name']