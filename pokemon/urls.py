from django.urls import path
from pokemon import views

app_name = 'pokemon'
urlpatterns = [
    path('', views.HomePageView.as_view() , name='home_page'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('pokemon_list/', views.PokemonListView.as_view(), name='pokemon_list'),
    path('pokemon_detail/<int:pk>/', views.PokemonDetailView.as_view(), name='pokemon_detail'),
    path('ability_detail/<int:pk>', views.AbilityDetailView.as_view(), name='ability_detail'),
    path('register/', views.RegistroUsuarioView.as_view(), name='register')
]