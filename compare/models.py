from django.db import models
from pokemon.models import Pokemon

class Comparison(models.Model):
    pokemon_1 = models.ForeignKey(Pokemon, related_name="pokemon_1", on_delete=models.CASCADE)
    pokemon_2 = models.ForeignKey(Pokemon, related_name="pokemon_2", on_delete=models.CASCADE)
    winner = models.ForeignKey(Pokemon, related_name="pokemon_winner", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_draw(self):
        return self.winner is None

    def __str__(self):
        if self.is_draw():
            return f"{self.pokemon_1.name} vs {self.pokemon_2.name} → Empate"
        return f"{self.pokemon_1.name} vs {self.pokemon_2.name} → Ganador: {self.winner.name}"