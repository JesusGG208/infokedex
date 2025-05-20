import random
from django.http import JsonResponse
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django.db.models import Q
from pokemon.models import Pokemon


class HomePageView(TemplateView):
    template_name = 'all_templates/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pokemon = list(Pokemon.objects.all())
        random.shuffle(pokemon)
        context['pokemon'] = pokemon[:10]
        return context

class SearchView(View):
    def get(self, request):
        q = request.GET.get('q', '')
        pokemon = Pokemon.objects.filter(Q(name__icontains=q) | Q(pokedex_id__icontains=q))[:10]
        return JsonResponse(
            [{'name': p.name, 'pokedex_id': p.pokedex_id, 'sprite': p.sprite_default} for p in pokemon],
            safe=False
        )

class PokemonListView(ListView):
    model = Pokemon
    template_name = 'all_templates/pokemon_list.html'
    context_object_name = 'pokemon'

class PokemonDetailView(DetailView):
    model = Pokemon
    template_name = 'all_templates/pokemon_detail.html'



