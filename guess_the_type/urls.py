from django.urls import path
from . import views

app_name = 'guess_the_type'

urlpatterns = [
    path('', views.TypeGuessGameView.as_view(), name='guess_type_game'),
]