from django.shortcuts import render, redirect

from player.models import Player
from game.models import Game

def welcome(request):
    if request.user.is_authenticated:
        usr = request.user
        bool_answer = Player.objects.filter(parent=usr.username).exists()
        if not bool_answer:
            Player.objects.create(name = usr, parent=usr.username, nick= usr.username)
        return redirect('home', name='welcome')
    else:
        return render(request, 'game/welcome.html')

def home_first(request):
    return redirect('home', name='welcome')