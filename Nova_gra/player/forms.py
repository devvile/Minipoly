from django import forms
from game.models import Player

class ChangeNick(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['nick']