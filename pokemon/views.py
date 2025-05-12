import random

from django.http import JsonResponse
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView

from pokemon.models import Pokemon


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pokemon = list(Pokemon.objects.all())
        random.shuffle(pokemon)
        context['pokemon'] = pokemon[:8]
        return context

class SearchView(View):
    def get(self, request):
        q = request.GET.get('q', '')
        pokemon = Pokemon.objects.filter(name__icontains=q)[:10]
        return JsonResponse(
            [{'name': p.name, 'id': p.pokedex_id} for p in pokemon],
            safe=False
        )

class PokemonListView(ListView):
    model = Pokemon
    template_name = 'pokemon_list.html'
    context_object_name = 'pokemon'

class PokemonDetailView(DetailView):
    model = Pokemon
    template_name = 'pokemon_detail.html'



