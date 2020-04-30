from django.shortcuts import render, redirect


def welcome(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return render(request, 'game/welcome.html')
