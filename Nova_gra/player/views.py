from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    usr = request.user.username
    return render(request,'player/home.html', {'usr': usr})