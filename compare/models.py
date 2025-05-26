from django.db import models
from pokemon.models import Pokemon

class Comparison(models.Model):
    pokemon_1 = models.ForeignKey(Pokemon, related_name="pokemon_1", on_delete=models.CASCADE)
    pokemon_2 = models.ForeignKey(Pokemon, related_name="pokemon_2", on_delete=models.CASCADE)
    winner = models.ForeignKey(Pokemon, related_name="pokemon_winner", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_draw(self):
        return self.winner is None

    def calculate_winner(self):
        stats = [
            'hp',
            'attack',
            'defense',
            'special_attack',
            'special_defense',
            'speed',
        ]

        p1_score = 0
        p2_score = 0

        for stat in stats:
            stat_1 = getattr(self.pokemon_1, stat, 0)
            stat_2 = getattr(self.pokemon_2, stat, 0)
            if stat_1 > stat_2:
                p1_score += 1
            elif stat_2 > stat_1:
                p2_score += 1

        # Comparar total sin modificar modelo Pokemon
        total_1 = sum(getattr(self.pokemon_1, stat, 0) for stat in stats)
        total_2 = sum(getattr(self.pokemon_2, stat, 0) for stat in stats)

        if total_1 > total_2:
            p1_score += 1
        elif total_2 > total_1:
            p2_score += 1

        if p1_score > p2_score:
            self.winner = self.pokemon_1
        elif p2_score > p1_score:
            self.winner = self.pokemon_2
        else:
            self.winner = None  # Empate