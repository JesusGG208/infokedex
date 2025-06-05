import random  # Importa random para mezclar listas
from django.http import JsonResponse  # Para devolver respuestas tipo JSON
from django.views import View  # Vista base para manejar métodos como GET o POST
from django.views.generic import DetailView, ListView, TemplateView  # Vistas predefinidas
from django.db.models import Q, Prefetch  # Q permite hacer búsquedas OR. Prefetch mejora eficiencia
from django.shortcuts import render  # Para renderizar plantillas HTML
from pokemon.models import Pokemon, Type, PokemonType, Ability  # Se importan los modelos


# Vista que muestra la página principal con 10 Pokémon al azar
class HomePageView(TemplateView):
    template_name = 'all_templates/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pokemonList = list(Pokemon.objects.all())  # Se obtienen todos los Pokémon y se convierten en lista
        random.shuffle(pokemonList)  # Se mezclan en orden aleatorio
        context['pokemon'] = pokemonList[:10]  # Se agregan solo los primeros 10 al contexto
        return context


# Vista que devuelve datos JSON según lo que el usuario busque
class SearchView(View):
    def get(self, request):
        q = request.GET.get('q', '')  # Se obtiene el texto de búsqueda del parámetro 'q'
        # Se filtran los Pokémon cuyo nombre o número contenga la búsqueda
        query = Pokemon.objects.filter(Q(name__icontains=q) | Q(pokedex_id__icontains=q))[:10]
        # Se convierte a lista de diccionarios con info básica
        context = [{'name': p.name, 'pokedex_id': p.pokedex_id, 'sprite': p.sprite_default} for p in query]
        return JsonResponse(context, safe=False)  # Se devuelve como respuesta JSON


# Vista que lista todos los Pokémon, con filtros por búsqueda, tipo, generación y evolución
class PokemonListView(ListView):
    model = Pokemon
    template_name = 'all_templates/pokemon_list.html'
    context_object_name = 'pokemon'  # Nombre que se usará en la plantilla

    # Metodo para obtener los Pokémon que se van a mostrar
    def get_queryset(self):
        pokemon = Pokemon.objects.all()  # Se parte de todos los Pokémon

        # Se añaden relaciones para evitar consultas innecesarias al acceder a tipos y evoluciones
        pokemon_q = pokemon.prefetch_related(
            Prefetch('types', queryset=PokemonType.objects.select_related('type')),
            'evolves_from',
            'evolves_to'
        )

        # Filtro si se escribe algo en el buscador
        q = self.request.GET.get('q', '').strip()
        if q:
            pokemon_q = pokemon_q.filter(Q(name__icontains=q) | Q(pokedex_id__icontains=q))

        # Filtro por tipo
        type_q = self.request.GET.get('type')
        if type_q:
            pokemon_q = pokemon_q.filter(types__type__name=type_q)

        # Filtro por generación
        gen_q = self.request.GET.get('generation')
        if gen_q:
            pokemon_q = pokemon_q.filter(generation=gen_q)

        # Filtro por etapa evolutiva (inicio, intermedio, final o sin evolución)
        evo = self.request.GET.get('evolution_stage')
        if evo:
            if evo == '1':
                pokemon_q = pokemon_q.filter(evolves_from__isnull=True, evolves_to__isnull=False)
            elif evo == '2':
                pokemon_q = pokemon_q.filter(evolves_from__isnull=False, evolves_to__isnull=False)
            elif evo == '3':
                pokemon_q = pokemon_q.filter(evolves_from__isnull=False, evolves_to__isnull=True)
            elif evo == '4':
                pokemon_q = pokemon_q.filter(evolves_from__isnull=True, evolves_to__isnull=True)

        return pokemon_q.distinct()  # Se quitan duplicados por si hubo combinaciones

    # Sobreescribe el metodo GET para añadir más datos al contexto
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        context['types'] = Type.objects.all()  # Se agregan los tipos al contexto
        context['generations'] = range(1, 10)  # Generaciones del 1 al 9
        return render(request, self.template_name, context)


# Vista para mostrar la información completa de un Pokémon específico
class PokemonDetailView(DetailView):
    model = Pokemon
    template_name = 'all_templates/pokemon_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Esta función convierte un queryset de evoluciones en una lista de datos
        def get_evolution_list(evolution_queryset, attribute_name):
            evolution_list = []
            for evolution in evolution_queryset.select_related(attribute_name):
                data = {
                    'pokemon': getattr(evolution, attribute_name),
                    'trigger': evolution.trigger,
                    'level': evolution.level,
                    'item': evolution.item
                }
                evolution_list.append(data)
            return evolution_list

        # Se añaden evoluciones hacia adelante y hacia atrás, y habilidades visibles y ocultas
        context['evolutions'] = get_evolution_list(self.object.evolves_to, 'to_pokemon')
        context['preevolutions'] = get_evolution_list(self.object.evolves_from, 'from_pokemon')
        context['normal_abilities'] = self.object.abilities.filter(is_hidden=False)
        context['hidden_abilities'] = self.object.abilities.filter(is_hidden=True)
        return context


# Vista para mostrar los detalles de una habilidad en particular
class AbilityDetailView(DetailView):
    model = Ability
    template_name = 'all_templates/ability_detail.html'
    context_object_name = 'ability'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Se buscan todos los Pokémon que tengan esta habilidad
        context['pokemon_list'] = Pokemon.objects.filter(abilities__ability=self.object).distinct()
        return context
