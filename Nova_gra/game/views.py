from django.shortcuts import render, redirect
from .models import Game
from player.models import Player
from .forms import CreateGame
from django.contrib.auth.decorators import login_required


@login_required
def detail(request, id):
    game = Game.objects.get(pk=id)
    players_ready= game.who_is_ready.all()
    return render( request, 'game/detail.html', {'game' : game, 'players_ready':players_ready})


@login_required
def game_join(request, id):
    game = Game.objects.get(pk=id)
    if game.players_ready == game.max_players:
        return redirect('home',name="full")
    else:
        return redirect('detail', game.id)

@login_required
def new(request):
    if request.method == "POST":
        player= Player.objects.get(name=request.user)
        hosted = Game(host=player.nick)
        form = CreateGame(instance = hosted,data=request.POST)
        if form.is_valid():
                form.save()
                return redirect("home", name="new_room")


@login_required
def delete_room(request, id):
    game = Game.objects.get(id=id)
    player = Player.objects.get(name=request.user)
    usr = player.nick
    if usr == game.host and game.players_ready == 0:
        if not game.is_played:
            game.delete()
            return redirect("home",name="game_deleted")
        else:
            return redirect('detail', id=game.id)
    else:
        return redirect('detail', id=game.id)

@login_required
def ready(request, id):
    game = Game.objects.get(id=id)
    w_pokoju = game.players_ready
    player = Player.objects.get(name=request.user)
    usr = player.nick
    bool_test = player in game.who_is_ready.all()
    if not game.is_played and not bool_test :
        if w_pokoju < game.max_players:
            game.players_ready += 1
            game.save()
            guys_ready = game.who_is_ready
            guys_ready.add(player)
            return redirect('detail',id = game.id)
        else:
            return redirect('detail', id=game.id)
    elif not game.is_played and bool_test :
        game.players_ready -= 1
        game.save()
        guys_ready = game.who_is_ready
        guys_ready.remove(player)
        return redirect('detail', id=game.id)
    else:
        return redirect('detail',id = game.id)

@login_required
def game_start(request, id):
    game = Game.objects.get(id=id)
    w_pokoju = game.players_ready
    player= Player.objects.get(name=request.user)
    usr = player.nick
    if w_pokoju > 1 and game.host == usr:
        if not game.is_played:
            game.is_played = True
            game.save()
            return redirect('detail',id = game.id)
        else:
            return redirect('detail',id = game.id)
    else:
        return redirect('detail',id = game.id)

@login_required
def game_end(request, id):
    game = Game.objects.get(id=id)
    w_pokoju = game.players_ready
    if game.is_played:
        game.is_played = False
        game.players_ready = 0
        game.save()
        return redirect('detail',id = game.id)
    else:
        return redirect('detail',id = game.id)

