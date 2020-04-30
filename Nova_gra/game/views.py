from django.shortcuts import render, redirect
from .models import Game
from .forms import CreateGame
from django.contrib.auth.decorators import login_required

@login_required
def detail(request, id):
    game = Game.objects.get(pk=id)
    return render( request, 'game/detail.html', {'game' : game})


@login_required
def new(request):
    if request.method == "POST":
        hosted = Game(host=request.user)
        form = CreateGame(instance = hosted,data=request.POST)
        if form.is_valid():
                form.save()
                return redirect("home")


@login_required
def delete_room(request, id):
    game = Game.objects.get(id=id)
    usr = request.user
    if usr == game.host:
        if not game.is_played:
            game.delete()
            return redirect("home")
        else:
            return redirect("home")
    else:
        return redirect("home")

@login_required
def ready(request, id):
    game = Game.objects.get(id=id)
    w_pokoju = game.players_ready
    if w_pokoju < game.max_players:
        if not game.is_played:
            game.players_ready += 1
            game.save()
            return redirect("home")
        else:
            return redirect("home")
    else:
        return redirect("home")