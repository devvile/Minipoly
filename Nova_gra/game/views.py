from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from player.models import Player
from match.models import Match
from .forms import CreateGame
from .models import Game


# @login_required
def detail(request, id):
    game = Game.objects.get(pk=id)
    players_ready = game.who_is_ready.all()
    args = {'game': game, 'players_ready': players_ready}
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
            match = Match.objects.create(name=game.name)
            match.is_played = True
            match.first_player = all_players[0]
            match.second_player = all_players[1]
            for i in game.who_is_ready.all():
                match.who_is_playing.add(i)
                game.who_is_ready.remove(i)
            if w_pokoju >= 3:
                match.third_player=all_players[2]
            if w_pokoju ==4:
                    match.forth_player == all_players[3]
            game.players_ready = 0
            game.save()
            match.save()
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
        for i in guys_ready.all():
            guys_ready.remove(i)
        game.players_ready = guys_ready.all().count()
        game.is_played = False
        game.save()
        return redirect('detail', id=game.id)
    else:
        return redirect('detail', id=game.id)
