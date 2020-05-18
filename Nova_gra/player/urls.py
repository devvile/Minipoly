from django.urls import path
from .views import home, account, new_nick, edit_description
from Nova_gra.views import home_first
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('home/s', home, name='home'),
    path('home', home_first, name='home_first'),
    path('account/<str:acc>=<str:notif>', account, name="player_account"),
    path('login', LoginView.as_view(template_name="player/login_form.html"), name='player_login'),
    path('logout', LogoutView.as_view(), name='player_logout'),
    path('nickchange', new_nick, name='change_nick'),
    path('<str:acc>/edit_description', edit_description, name = 'edit_description')
]
