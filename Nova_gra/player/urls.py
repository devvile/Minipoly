
from django.urls import path
from .views import home

urlpatterns = [
    path('home/<str:name>', home, name = 'home')
]