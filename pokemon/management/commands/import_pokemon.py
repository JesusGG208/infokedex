from django.core.management.base import BaseCommand
from pokemon.models import Pokemon, Type, PokemonType, Ability, PokemonAbility, Evolution
import requests
import time
import os
from django.core.files import File
from django.conf import settings


class Command(BaseCommand):
    help = 'Importa Pokémon desde PokéAPI a la base de datos usando imágenes locales'

    def handle(self, *args, **options):
        # Mapeo de nombres de tipos en inglés a español para las imágenes
        TYPE_IMAGE_NAMES = {
            'normal': 'normal',
            'fire': 'fuego',
            'water': 'agua',
            'electric': 'eléctrico',
            'grass': 'planta',
            'ice': 'hielo',
            'fighting': 'lucha',
            'poison': 'veneno',
            'ground': 'tierra',
            'flying': 'volador',
            'psychic': 'psíquico',
            'bug': 'bicho',
            'rock': 'roca',
            'ghost': 'fantasma',
            'dragon': 'dragón',
            'dark': 'siniestro',
            'steel': 'acero',
            'fairy': 'hada'
        }

        def get_spanish_name(api_data, field="names"):
            try:
                return next(
                    item['name'] for item in api_data.get(field, [])
                    if item['language']['name'] == 'es'
                )
            except StopIteration:
                return api_data['name']

        def get_ability_description(entries, lang='es'):
            texts = [
                entry for entry in entries
                if entry['language']['name'] == lang
            ]
            if texts:
                return texts[-1]['flavor_text'].replace('\n', ' ').replace('\f', ' ')
            return ""

        def assign_local_images(type_obj, type_name_en):
            """Asigna imágenes locales al tipo basado en el nombre en inglés"""
            image_base_name = TYPE_IMAGE_NAMES.get(type_name_en.lower())
            if not image_base_name:
                return

            named_icon_path = os.path.join(settings.MEDIA_ROOT, 'types', 'named_icons', f'{image_base_name}.png')

            # Asignar icono con nombre
            if os.path.exists(named_icon_path):
                with open(named_icon_path, 'rb') as f:
                    type_obj.named_icon.save(f'{image_base_name}_named.png', File(f), save=True)
            else:
                self.stdout.write(
                    self.style.WARNING(f'Icono con nombre no encontrado para tipo {type_name_en} en {named_icon_path}'))

        def fetch_pokemon_data(pokemon_id):
            try:
                # Datos básicos
                pokemon_data = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/", timeout=10).json()
                species_data = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}/",
                                            timeout=10).json()

                # Traducción
                name_es = get_spanish_name(species_data)
                description_es = get_ability_description(species_data['flavor_text_entries'])

                # Sprites del artwork oficial
                artwork = pokemon_data['sprites']['other']['official-artwork']
                artwork_default = artwork.get('front_default')
                artwork_shiny = artwork.get('front_shiny')

                # Crear o actualizar Pokémon
                stats = {stat['stat']['name']: stat['base_stat'] for stat in pokemon_data['stats']}

                pokemon, _ = Pokemon.objects.update_or_create(
                    pokedex_id=pokemon_id,
                    defaults={
                        'name': name_es,
                        'height': pokemon_data['height'],
                        'weight': pokemon_data['weight'],
                        'hp': stats.get('hp', 0),
                        'attack': stats.get('attack', 0),
                        'defense': stats.get('defense', 0),
                        'special_attack': stats.get('special-attack', 0),
                        'special_defense': stats.get('special-defense', 0),
                        'speed': stats.get('speed', 0),
                        'description': description_es,
                        'generation': int(species_data['generation']['url'].split('/')[-2]),
                        'is_legendary': species_data['is_legendary'],
                        'is_mythical': species_data['is_mythical'],
                        'sprite_default': pokemon_data['sprites']['front_default'],
                        'sprite_shiny': pokemon_data['sprites']['front_shiny'],
                        'official_artwork_default': artwork_default,
                        'official_artwork_shiny': artwork_shiny,
                    }
                )

                # Tipos - usando imágenes locales
                PokemonType.objects.filter(pokemon=pokemon).delete()
                for t in pokemon_data['types']:
                    type_data = requests.get(t['type']['url'], timeout=10).json()
                    type_name_en = type_data['name']
                    type_name_es = get_spanish_name(type_data)

                    # Crear o actualizar el tipo
                    type_obj, created = Type.objects.get_or_create(name=type_name_es)

                    # Asignar imágenes locales si es un nuevo tipo o si no tiene imágenes
                    if created or not type_obj.named_icon:
                        assign_local_images(type_obj, type_name_en)

                    PokemonType.objects.create(pokemon=pokemon, type=type_obj, slot=t['slot'])

                # Habilidades
                PokemonAbility.objects.filter(pokemon=pokemon).delete()
                for ability_entry in pokemon_data['abilities']:
                    ability_data = requests.get(ability_entry['ability']['url'], timeout=10).json()
                    ability_name_es = get_spanish_name(ability_data)

                    # Buscar texto en flavor_text_entries (último)
                    effect_text = get_ability_description(ability_data.get('flavor_text_entries', []))

                    ability_obj, _ = Ability.objects.get_or_create(
                        name=ability_name_es,
                        defaults={'effect': effect_text}
                    )

                    # Si ya existe sin efecto, actualizarlo
                    if not ability_obj.effect and effect_text:
                        ability_obj.effect = effect_text
                        ability_obj.save()

                    PokemonAbility.objects.update_or_create(
                        pokemon=pokemon,
                        ability=ability_obj,
                        defaults={'is_hidden': ability_entry['is_hidden']}
                    )

                # Evoluciones
                evolution_chain_url = species_data['evolution_chain']['url']
                evolution_data = requests.get(evolution_chain_url, timeout=10).json()

                def process_evolution_chain(chain):
                    current_name = chain['species']['name']
                    from_pokemon = Pokemon.objects.filter(name__iexact=current_name).first()

                    for evo in chain.get('evolves_to', []):
                        target_name = evo['species']['name']
                        to_pokemon = Pokemon.objects.filter(name__iexact=target_name).first()

                        details = evo['evolution_details'][0] if evo['evolution_details'] else {}
                        trigger = details.get('trigger', {}).get('name')
                        level = details.get('min_level')
                        item = details.get('item', {}).get('name') if details.get('item') else None

                        if from_pokemon and to_pokemon:
                            Evolution.objects.update_or_create(
                                from_pokemon=from_pokemon,
                                to_pokemon=to_pokemon,
                                defaults={
                                    'trigger': trigger,
                                    'level': level,
                                    'item': item
                                }
                            )

                        process_evolution_chain(evo)

                if 'chain' in evolution_data:
                    process_evolution_chain(evolution_data['chain'])

                self.stdout.write(self.style.SUCCESS(f'Pokémon {pokemon_id} importado'))
                return True

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error con Pokémon {pokemon_id}: {str(e)}'))
                return False

        # Crear directorios para los tipos si no existen
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'types', 'named_icons'), exist_ok=True)

        # Importar Pokémon del 1 al 1025 (o el rango que desees)
        for i in range(1, 1026):
            fetch_pokemon_data(i)
            time.sleep(0.25)