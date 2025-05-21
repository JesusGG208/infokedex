import random
from django.http import JsonResponse
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django.db.models import Q
from pokemon.models import Pokemon, Type


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

class PokemonFilterView(View):
    def get(self, request):
        q = request.GET.get('q')
        type_ = request.GET.get('type')
        generation = request.GET.get('generation')
        evo_stage = request.GET.get('evolution_stage')

        pokemon = Pokemon.objects.all()

        # Buscador
        if q:
            pokemon = pokemon.filter(
                Q(name__icontains=q) | Q(pokedex_id__icontains=q)
            )

        # Tipo
        if type_:
            pokemon = pokemon.filter(types__type__name=type_)

        # Generación
        if generation:
            try:
                generation = int(generation)
                pokemon = pokemon.filter(generation=generation)
            except ValueError:
                pass

        # Etapa evolutiva
        if evo_stage:
            try:
                evo_stage = int(evo_stage)
                if evo_stage == 1:
                    pokemon = pokemon.filter(
                        evolves_from__isnull=True,
                        evolves_to__isnull=False
                    )
                elif evo_stage == 2:
                    pokemon = pokemon.filter(
                        evolves_from__isnull=False,
                        evolves_to__isnull=False
                    )
                elif evo_stage == 3:
                    pokemon = pokemon.filter(
                        evolves_from__isnull=False,
                        evolves_to__isnull=True
                    )
                elif evo_stage == 4:
                    pokemon = pokemon.filter(
                        evolves_from__isnull=True,
                        evolves_to__isnull=True
                    )

            except ValueError:
                pass

        pokemon = pokemon.distinct()[:1025]

        data = [{
            'name': p.name,
            'pokedex_id': p.pokedex_id,
            'sprite': p.sprite_default
        } for p in pokemon]

        return JsonResponse(data, safe=False)

class PokemonDetailView(DetailView):
    model = Pokemon
    template_name = 'all_templates/pokemon_detail.html'



