from django.urls import path
from pokewordle import views

app_name = 'pokewordle'
urlpatterns = [
    path('', views.StartGameView.as_view(), name='start_game'),
    path('play_game/<int:game_id>', views.PlayGameView.as_view(), name='play_game'),
]