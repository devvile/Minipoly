from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from game.models import Game
from .models import Player
from .forms import ChangeNick, ChangeDescription
from game.forms import CreateGame

@login_required
def home(request):
    usr = request.user.username
    player = Player.objects.get(parent=usr)
    games = Game.objects.all()
    form = CreateGame
    args = {'usr': usr, 'games': games, 'form': form, 'player':player}
    return render(request, 'player/home.html', args)

@login_required
def account(request, acc, notif):
    usr = request.user
    player = Player.objects.get(parent=usr.username)
    form = ChangeNick
    hs = Game.objects.filter(host=player.nick)
    hs_nr = hs.count()
    desc = player.description
    args = {'player': player, 'form': form, 'games': hs , 'games_nr': hs_nr, 'description': desc}
    return render(request, 'player/player_account.html', args)

@login_required
def new_nick(request):
    usr = request.user.username
    player = Player.objects.get(parent=usr)
    hs = Game.objects.filter(host=player.nick)
    hs_nr = hs.count()
    if hs_nr == 0:
        if request.method == "POST":
            acc = player
            form = ChangeNick(instance=acc, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect("player_account", player, 'nick_success')
        else:
            return redirect("player_account", player, 'nick_not_valid')
    else:
        return redirect("player_account", player)

@login_required
def edit_description(request, acc):
    form = ChangeDescription
    usr = request.user
    player = Player.objects.get(parent=usr.username)
    desc = player.description
    args = {"form":form, "description":desc}
    return render (request, 'player/player_edit_description.html', args)