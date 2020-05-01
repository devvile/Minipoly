from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from game.models import Game, Notification
from game.forms import CreateGame

@login_required
def home(request, name):
    usr = request.user.username
    games = Game.objects.all()
    noti =  Notification.objects.get(name=name)
    text = noti.note
    form = CreateGame
    return render(request,'player/home.html', {'usr': usr, 'games': games, 'form' : form, 'message': text})