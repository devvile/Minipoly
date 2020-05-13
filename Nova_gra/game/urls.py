
from django.urls import path
from .views import detail, new, delete_room, ready, game_start, game_end, game_join,game_leave,game_end_turn

urlpatterns = [
    path('<int:id>/', detail, name = 'detail'),
    path('<int:id>/join', game_join, name = 'game_join'),
    path('new', new, name='new_room'),
    path('delete/<int:id>',delete_room, name='delete_gam'),
    path('ready/<int:id>', ready, name ='player_ready'),
    path('start/<int:id>', game_start, name = 'game_start'),
    path('end/<int:id>', game_end, name = 'game_end'),
    path('<int:id>/leave',game_leave,name='game_leave'),
    path('<int:id>=end_turn', game_end_turn, name = 'game_end_turn'),
]