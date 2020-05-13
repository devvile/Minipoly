from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from player.models import Player
from .forms import CreateGame
from .models import Game


# @login_required
def detail(request, id):
    game = Game.objects.get(pk=id)
    player = Player.objects.get(parent=request.user.username)
    players_ready = game.who_is_ready.all()
    players_playing = game.who_is_playing.all()
    player_in_game = player.guys_playing.filter(name=game.name)
    args = {'game': game, 'players_ready': players_ready, 'players_playing':players_playing, 'player_in_game':player_in_game}
    return render(request, 'game/detail.html', args)


@login_required
def game_join(request, id):
    game = Game.objects.get(pk=id)
    if game.players_ready == game.max_players:
        return redirect('home', name="full")
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
            return redirect("home", name="new_room")


@login_required
def delete_room(request, id):
    game = Game.objects.get(id=id)
    player = Player.objects.get(name=request.user)
    usr = player.nick
    if usr == game.host and game.players_ready == 0:
        if not game.is_played:
            game.delete()
            return redirect("home", name="game_deleted")
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
    if not game.is_played and not bool_test and not player.in_game:
        if w_pokoju < game.max_players:
            game.players_ready += 1
            game.save()
            player.in_game = True
            player.save()
            guys_ready = game.who_is_ready
            guys_ready.add(player)
            return redirect('detail', id=game.id)
        else:
            return redirect('detail', id=game.id)
    elif not game.is_played and not w_pokoju == 0:
        game.players_ready -= 1
        guys_ready = game.who_is_ready
        guys_ready.remove(player)
        game.save()
        player.in_game = False
        player.save()
        return redirect('detail', id=game.id)
    else:
        return redirect('detail', id=game.id)


@login_required
def game_start(request, id):
    game = Game.objects.get(id=id)
    w_pokoju = game.players_ready
    player = Player.objects.get(name=request.user)
    usr = player.nick
    if w_pokoju > 1 and game.host == usr:
        if not game.is_played:
            game.is_played = True
            all_players  = list(game.who_is_ready.all())
            game.first_player = all_players[0]
            game.second_player = all_players[1]
            for i in game.who_is_ready.all():
                game.who_is_playing.add(i)
                game.turn_of_player = game.first_player
                game.who_is_ready.remove(i)
            if w_pokoju >= 3:
                game.third_player=all_players[2]
            if w_pokoju ==4:
                    game.forth_player == all_players[3]
            game.players_ready = 0
            game.save()
            return redirect('detail', id=game.id)
        else:
            return redirect('detail', id=game.id)
    else:
        return redirect('detail', id=game.id)


@login_required
def game_end(request, id):
    game = Game.objects.get(id=id)
    bool_test = request.user.username == game.host
    if game.is_played and bool_test:
        guys_ready= game.who_is_ready
        guys_playing = game.who_is_playing
        for i in guys_ready.all():
            guys_ready.remove(i)
        for j in guys_playing.all():
            guys_playing.remove(j)
            j.in_game = False
            j.save()
        game.players_ready = guys_ready.all().count()
        game.is_played = False
        game.save()
        return redirect('detail', id=game.id)
    else:
        return redirect('detail', id=game.id)


@login_required
def game_leave(request, id):
    game = Game.objects.get(id=id)
    guys_playing = game.who_is_playing
    bool_test = request.user.username == game.host
    player=Player.objects.get(parent=request.user.username)
    if game.is_played:
        guys_playing = game.who_is_playing
        guys_playing.remove(player)
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
            return redirect('detail', id=game.id)
    else:
        return redirect('detail', id=game.id)


@login_required
def game_end_turn(request, id):
    game = Game.objects.get(id=id)
    return redirect('detail', id=game.id)
