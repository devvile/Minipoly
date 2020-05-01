from django.shortcuts import render, redirect
from game.models import Notification

def welcome(request):
    if request.user.is_authenticated:
        return redirect('home', name='welcome')
    else:
        return render(request, 'game/welcome.html')
