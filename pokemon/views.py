import random
from django.http import JsonResponse
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django.db.models import Q
from pokemon.models import Pokemon, Type, PokemonType
from django.db.models import Prefetch
from django.shortcuts import render

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

    def get_queryset(self):
        queryset = Pokemon.objects.all()

        queryset = queryset.prefetch_related(
            Prefetch('types', queryset=PokemonType.objects.select_related('type')),
            'evolves_from',
            'evolves_to'
        )

        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(pokedex_id__icontains=search_query)
            )

        type_filter = self.request.GET.get('type')
        if type_filter:
            queryset = queryset.filter(types__type__name=type_filter)

        gen_filter = self.request.GET.get('generation')
        if gen_filter:
            queryset = queryset.filter(generation=gen_filter)

        evo_stage = self.request.GET.get('evolution_stage')
        if evo_stage:
            if evo_stage == '1':
                queryset = queryset.filter(evolves_from__isnull=True, evolves_to__isnull=False)
            elif evo_stage == '2':
                queryset = queryset.filter(evolves_from__isnull=False, evolves_to__isnull=False)
            elif evo_stage == '3':
                queryset = queryset.filter(evolves_from__isnull=False, evolves_to__isnull=True)
            elif evo_stage == '4':
                queryset = queryset.filter(evolves_from__isnull=True, evolves_to__isnull=True)

        return queryset.distinct()

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        context['types'] = Type.objects.all()
        context['generations'] = range(1, 10)
        return render(request, self.template_name, context)

class PokemonDetailView(DetailView):
    model = Pokemon
    template_name = 'all_templates/pokemon_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pokemon = self.object

        def get_pre_evolutions(p):
            chain = []
            while p.evolves_from.exists():
                p = p.evolves_from.first().from_pokemon
                chain.insert(0, p)
            return chain

        def get_post_evolutions(p):
            result = []

            def recurse(current):
                for evo in current.evolves_to.all():
                    next_p = evo.to_pokemon
                    result.append(next_p)
                    recurse(next_p)

            recurse(p)
            return result

        context['pre_evolutions'] = get_pre_evolutions(pokemon)
        context['current_pokemon'] = pokemon
        context['post_evolutions'] = get_post_evolutions(pokemon)
        return context




