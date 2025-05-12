from django.core.management.base import BaseCommand
from pokemon.models import Pokemon, Type, PokemonType, Ability, PokemonAbility, Evolution
import requests
import time

class Command(BaseCommand):
    help = 'Cargar Pokémon desde la PokéAPI'

    def handle(self, *args, **kwargs):

        # Obtiene el nombre en español de un recurso si está disponible
        def get_spanish_names(datos, campo="names"):
            for cosa in datos.get(campo, []):
                if cosa["language"]["name"] == "es":
                    return cosa["name"]
            return datos.get("name", "Nombre desconocido")

        # Obtiene la descripción en español de un Pokémon
        def get_spanish_texts(textos):
            for texto in textos:
                if texto["language"]["name"] == "es":
                    return texto["flavor_text"].replace('\n', ' ').replace('\f', ' ')
            return ""

        # Función principal para importar los datos de un Pokémon por su ID
        def import_data(poke_id):
            try:
                # Obtener datos básicos y de especie
                info = requests.get(f"https://pokeapi.co/api/v2/pokemon/{poke_id}/").json()
                especie = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{poke_id}/").json()

                # Nombre y descripción en español
                nombre = get_spanish_names(especie)
                descripcion = get_spanish_texts(especie["flavor_text_entries"])

                # Imágenes oficiales del Pokémon
                imagenes = info["sprites"]["other"]["official-artwork"]
                arte_normal = imagenes.get("front_default")
                arte_brillante = imagenes.get("front_shiny")

                # Estadísticas base
                stats = {}
                for s in info["stats"]:
                    stats[s["stat"]["name"]] = s["base_stat"]

                # Crear o actualizar el objeto Pokémon en la base de datos
                pokemon, _ = Pokemon.objects.update_or_create(
                    pokedex_id=poke_id,
                    defaults={
                        "name": nombre,
                        "height": info["height"],
                        "weight": info["weight"],
                        "hp": stats.get("hp", 0),
                        "attack": stats.get("attack", 0),
                        "defense": stats.get("defense", 0),
                        "special_attack": stats.get("special-attack", 0),
                        "special_defense": stats.get("special-defense", 0),
                        "speed": stats.get("speed", 0),
                        "description": descripcion,
                        "generation": int(especie["generation"]["url"].split("/")[-2]),
                        "is_legendary": especie["is_legendary"],
                        "is_mythical": especie["is_mythical"],
                        "sprite_default": info["sprites"]["front_default"],
                        "sprite_shiny": info["sprites"]["front_shiny"],
                        "official_artwork_default": arte_normal,
                        "official_artwork_shiny": arte_brillante,
                    }
                )

                # Relacionar los tipos del Pokémon
                PokemonType.objects.filter(pokemon=pokemon).delete()  # Limpiar tipos anteriores
                for tipo in info["types"]:
                    tipo_data = requests.get(tipo["type"]["url"]).json()
                    tipo_nombre = get_spanish_names(tipo_data)
                    tipo_obj, _ = Type.objects.get_or_create(name=tipo_nombre)
                    PokemonType.objects.create(pokemon=pokemon, type=tipo_obj, slot=tipo["slot"])

                # Relacionar las habilidades del Pokémon
                PokemonAbility.objects.filter(pokemon=pokemon).delete()  # Limpiar habilidades anteriores
                for hab in info["abilities"]:
                    hab_data = requests.get(hab["ability"]["url"]).json()
                    hab_nombre = get_spanish_names(hab_data)
                    efecto = get_spanish_texts(hab_data.get("flavor_text_entries", []))

                    habilidad, _ = Ability.objects.get_or_create(name=hab_nombre, defaults={"effect": efecto})

                    # Si la habilidad ya existe, pero no tiene descripción, actualizarla
                    if not habilidad.effect and efecto:
                        habilidad.effect = efecto
                        habilidad.save()

                    # Crear o actualizar relación entre Pokémon y habilidad
                    PokemonAbility.objects.update_or_create(
                        pokemon=pokemon,
                        ability=habilidad,
                        defaults={"is_hidden": hab["is_hidden"]}
                    )

                # Procesar cadena evolutiva
                evo_url = especie["evolution_chain"]["url"]
                evo_data = requests.get(evo_url).json()

                # Función recursiva para recorrer la cadena de evolución
                def procesar_evoluciones(cadena):
                    desde = cadena["species"]["name"]
                    desde_poke = Pokemon.objects.filter(name__iexact=desde).first()

                    for evolucion in cadena["evolves_to"]:
                        hacia = evolucion["species"]["name"]
                        hacia_poke = Pokemon.objects.filter(name__iexact=hacia).first()

                        # Manejo seguro de detalles de evolución
                        detalles_list = evolucion.get("evolution_details", [])
                        if detalles_list and len(detalles_list) > 0:
                            detalles = detalles_list[0]
                        else:
                            detalles = {}

                        trigger = detalles.get("trigger", {}).get("name")
                        nivel = detalles.get("min_level")
                        objeto = detalles.get("item", {}).get("name") if detalles.get("item") else None

                        # Crear relación de evolución si ambos Pokémon existen en DB
                        if desde_poke and hacia_poke:
                            Evolution.objects.update_or_create(
                                from_pokemon=desde_poke,
                                to_pokemon=hacia_poke,
                                defaults={
                                    "trigger": trigger,
                                    "level": nivel,
                                    "item": objeto
                                }
                            )

                        # Recursión para procesar evoluciones siguientes
                        procesar_evoluciones(evolucion)

                if "chain" in evo_data:
                    procesar_evoluciones(evo_data["chain"])

                self.stdout.write(self.style.SUCCESS(f"Pokémon {poke_id} cargado bien"))
                return True

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error con el Pokémon {poke_id}: {str(e)}"))
                return False

        # Recorrer todos los Pokémon hasta el ID 1025
        for num in range(1, 1026):
            import_data(num)
            time.sleep(0.25)  # Pausa para evitar ser bloqueado por la API
