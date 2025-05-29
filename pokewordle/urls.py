from django.urls import path
from pokewordle import views

app_name = 'pokewordle'

urlpatterns = [
    path('', views.StartPokewordleGame.as_view(), name='start'),
    path('play/<int:pk>/', views.PlayPokewordleGame.as_view(), name='play'),
]
