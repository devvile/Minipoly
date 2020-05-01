from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from game.models import Game, Notification, Player
from game.forms import CreateGame

@login_required
def home(request, name):
    usr = request.user.username
    games = Game.objects.all()
    noti =  Notification.objects.get(name=name)
    text = noti.note
    form = CreateGame
    return render(request,'player/home.html', {'usr': usr, 'games': games, 'form' : form, 'message': text})

@login_required
def account(request, acc):
    usr =request.user.username
    player = Player.objects.get(parent=usr)
    return render(request, 'player/player_account.html',{'player':player})

