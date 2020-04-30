from django.shortcuts import render
from .models import Game
from .forms import CreateGame

def detail(request, id):
    game = Game.objects.get(pk=id)
    return render( request, 'game/detail.html', {'game' : game})

def new(request):
    if request.method == "POST":
        form = CreateGame(request.POST)
        if form.is_valid():
                form.save()
                return redirect("home")