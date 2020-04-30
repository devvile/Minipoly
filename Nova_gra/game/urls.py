
from django.urls import path
from .views import detail, new, delete_room, ready

urlpatterns = [
    path('<int:id>', detail, name = 'detail'),
    path('new', new, name='new_room'),
    path('delete/<int:id>',delete_room, name='delete_gam'),
    path('ready/<int:id>', ready, name ='player_ready')
]