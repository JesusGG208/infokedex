import requests
from pokemon.models import Pokemon, Type, PokemonType, Ability, PokemonAbility


def fetch_pokemon_data(pokemon_id):
    # Datos básicos del Pokémon
    pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/"
    pokemon_data = requests.get(pokemon_url).json()

    # Datos de la especie (para la descripción)
    species_url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}/"
    species_data = requests.get(species_url).json()

    # Buscar la primera descripción en español
    description = None
    for entry in species_data["flavor_text_entries"]:
        if entry["language"]["name"] == "es":
            description = entry["flavor_text"].replace("\n", " ").replace("\f", " ")
            break

    # Crear o actualizar el Pokémon
    pokemon, created = Pokemon.objects.update_or_create(
        pokedex_id=pokemon_id,
        defaults={
            "name": pokemon_data["name"],
            "height": pokemon_data["height"],
            "weight": pokemon_data["weight"],
            "hp": pokemon_data["stats"][0]["base_stat"],
            "attack": pokemon_data["stats"][1]["base_stat"],
            "defense": pokemon_data["stats"][2]["base_stat"],
            "special_attack": pokemon_data["stats"][3]["base_stat"],
            "special_defense": pokemon_data["stats"][4]["base_stat"],
            "speed": pokemon_data["stats"][5]["base_stat"],
            "sprite_default": pokemon_data["sprites"]["front_default"],
            "sprite_shiny": pokemon_data["sprites"]["front_shiny"],
            "description": description,
            "is_legendary": species_data["is_legendary"],
            "is_mythical": species_data["is_mythical"],
            "generation": int(species_data["generation"]["url"].split("/")[-2]),
        }
    )

    # Procesar tipos
    for type_data in pokemon_data["types"]:
        type_name = type_data["type"]["name"]
        type_obj, _ = Type.objects.get_or_create(name=type_name)
        PokemonType.objects.get_or_create(
            pokemon=pokemon,
            type=type_obj,
            slot=type_data["slot"]
        )

    # Procesar habilidades
    for ability_data in pokemon_data["abilities"]:
        ability_name = ability_data["ability"]["name"]
        ability_obj, _ = Ability.objects.get_or_create(name=ability_name)
        PokemonAbility.objects.get_or_create(
            pokemon=pokemon,
            ability=ability_obj,
            is_hidden=ability_data["is_hidden"]
        )


if __name__ == "__main__":
    for i in range(1, 1026):
        fetch_pokemon_data(i)
        print(f"Pokémon {i} importado!")