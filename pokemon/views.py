from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from pokemon.models import Pokemon


# Create your views here.
class PrincipalPageView(TemplateView):
    template_name = "principal_page.html"

class PokemonListView(ListView):
    model = Pokemon
    template_name= "pokemon_list.html"
    context_object_name = "pokemon"

