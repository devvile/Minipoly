from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from game.models import Game
from game.forms import CreateGame

@login_required
def home(request):
    usr = request.user.username
    games = Game.objects.all()
    form = CreateGame
    return render(request,'player/home.html', {'usr': usr, 'games': games, 'form' : form, })