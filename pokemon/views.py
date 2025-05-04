from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView

from pokemon.models import Pokemon, EvolutionChain


# Create your views here.
class HomeView(TemplateView):
    template_name = "home.html"

class PokemonListView(ListView):
    model = Pokemon
    template_name = "pokemon_list.html"
    context_object_name = "pokemon"

class PokemonDetailView(DetailView):
    model = Pokemon
    template_name = "pokemon_detail.html"
    context_object_name = "pokemon"

class EvolutiveChainListView(ListView):
    model = EvolutionChain
    template_name = "ev_chain_list.html"
    context_object_name = "ev_chain"