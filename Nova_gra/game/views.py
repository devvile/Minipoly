from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from player.models import Player
from .forms import CreateGame
from .models import Game, Field


@login_required
def detail(request, id):
    game = Game.objects.get(pk=id)
    player = Player.objects.get(parent=request.user.username)
    fields = Field.objects.all
    args = {'game': game, 'players_ready': game.players_ready, 'players_playing':game.players_playing,
            'player_in_game':player in game.players_playing, 'fields':fields}
    return render(request, 'game/detail.html', args)


@login_required
def game_join(request, id):
    game = Game.objects.get(pk=id)
    if game.players_ready == game.max_players:
        return redirect('home')
    else:
        return redirect('detail', game.id)


@login_required
def new(request):
    if request.method == "POST":
        player = Player.objects.get(name=request.user)
        hosted = Game(host=player.nick)
        form = CreateGame(instance=hosted, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")


@login_required
def delete_room(request, id):
    game = Game.objects.get(id=id)
    player = Player.objects.get(name=request.user)
    if player.nick == game.host and game.how_many_players_ready == 0:
        if not game.is_played:
            game.delete()
            return redirect("home")
        else:
            return redirect('detail', id=game.id)
    else:
        return redirect('detail', id=game.id)


@login_required
def ready(request, id):
    game = Game.objects.get(id=id)
    player = Player.objects.get(name=request.user)
    bool_test = player in game.players_ready
    if not game.is_played and not bool_test and not player.in_game:
        if game.how_many_players_ready < game.max_players:
            player.in_game = True  # todo to mozna udoskonalic przez metode Playera
            player.save()
            game.who_is_ready.add(player)
            return redirect('detail', id=game.id)
        else:
            return redirect('detail', id=game.id)
    elif not game.is_played and not game.how_many_players_ready == 0:
        game.who_is_ready.remove(player)
        player.in_game = False
        player.save()
        return redirect('detail', id=game.id)
    else:
        return redirect('detail', id=game.id)


@login_required
def game_start(request, id):
    game = Game.objects.get(id=id)
    player = Player.objects.get(name=request.user)
    if game.how_many_players_ready > 1 and game.host == player.nick:
        if not game.is_played:
            game.is_played = True
            for i in game.who_is_ready.all():
                game.who_is_playing.add(i)
                game.turn_of_player = game.first_player
                game.who_is_ready.remove(i)
            game.save()
            return redirect('detail', id=game.id)
        else:
            return redirect('detail', id=game.id)
    else:
        return redirect('detail', id=game.id)


@login_required
def game_end(request, id):
    game = Game.objects.get(id=id)
    player = Player.objects.get(name=request.user)
    bool_test = player.nick == game.host
    if game.is_played and bool_test:
        for j in game.players_playing:
            j.in_game = False
            j.save()
        game.who_is_playing.clear()
        game.is_played = False
        game.save()
        return redirect('detail', id=game.id)
    else:
        return redirect('detail', id=game.id)


@login_required
def game_leave(request, id):
    game = Game.objects.get(id=id)
    player=Player.objects.get(parent=request.user.username)
    if game.is_played:
        guys_playing = game.who_is_playing
        game.turn_of_player = game.next_player
        guys_playing.remove(player)
        game.save()
        player.in_game = False
        player.save()
        if game.who_is_playing.count()<2:
            game.is_played = False
            game.save()
            for j in guys_playing.all():
                guys_playing.remove(j)
                j.in_game = False
                j.save()
            return redirect('detail', id=game.id)
        else:
            #zmiana tury
            return redirect('detail', id=game.id)
    else:
        return redirect('detail', id=game.id)


@login_required
def game_end_turn(request, id):
    game = Game.objects.get(id=id)
    player = Player.objects.get(parent=request.user)
    if player == game.turn_of_player:
        game.turn_of_player = game.next_player
        game.save()
        return redirect('detail', id=game.id)
    else:
        return redirect('detail',id=game.id)
