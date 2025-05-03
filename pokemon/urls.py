from django.urls import path

from pokemon import views

app_name = 'pokemon'
urlpatterns = [
    path('/', views.HomeView.as_view(), name='home_page'),
    path('pokemon_list/', views.PokemonListView.as_view(), name='pokemon_list'),
    path('pokemon_detail/<int:pk>/', views.PokemonDetailView.as_view() , name='pokemon_detail'),
]