
from django.urls import path
from .views import home, account

urlpatterns = [
    path('home/<str:name>', home, name = 'home'),
    path('account/<str:acc>', account, name="player_account")
]