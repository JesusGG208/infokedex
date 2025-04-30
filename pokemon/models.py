from django.db import models


class EvolutionChain(models.Model):
    """
    Representa una cadena evolutiva completa.
    """
    chain_id = models.IntegerField(unique=True)  # ID de la PokeAPI

    def __str__(self):
        return f"Evolution Chain {self.chain_id}"


class Pokemon(models.Model):
    """
    Toda la información de un pokemon.
    """
    name = models.CharField(max_length=100, unique=True)
    pokedex_id = models.IntegerField(unique=True)
    primary_type = models.CharField(max_length=100)
    secondary_type = models.CharField(max_length=100, null=True, blank=True)
    height = models.IntegerField()
    weight = models.IntegerField()
    sprite_url = models.URLField()

    # Estadísticas base
    hp = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    special_attack = models.IntegerField()
    special_defense = models.IntegerField()
    speed = models.IntegerField()

    # Evolución
    evolution_chain = models.ForeignKey(EvolutionChain, on_delete=models.SET_NULL, null=True, related_name='pokemons')
    evolution_stage = models.IntegerField()

    def __str__(self):
        return self.name