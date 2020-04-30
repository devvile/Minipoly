
from django.contrib import admin
from django.urls import path, include
from .views import welcome

urlpatterns = [
    path('admin/', admin.site.urls),
    path('player/', include('player.urls')),
    path('game/',include('game.urls')),
    path('', welcome)
]
