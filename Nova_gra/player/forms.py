from django import forms
from .models import Player


class ChangeNick(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['nick']


class ChangeDescription(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['description']