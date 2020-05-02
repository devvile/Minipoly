from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from game.models import Game, Notification, Player
from .forms import ChangeNick
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
    form = ChangeNick
    return render(request, 'player/player_account.html',{'player':player,'form':form})

@login_required
def new_nick(request):
    usr = request.user.username
    player = Player.objects.get(parent=usr)
    if request.method == "POST":
        acc = player
        form = ChangeNick(instance = acc,data=request.POST)
        if form.is_valid():
                form.save()
                return redirect("player_account",{'player':player})
        else:
            return redirect("player_account",{'player':player})