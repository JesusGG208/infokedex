from django.db import models
from pokemon.models import Pokemon

class Compare(models.Model):
    pokemon_1 = models.ForeignKey(Pokemon, related_name="pokemon_1", on_delete=models.CASCADE)
    pokemon_2 = models.ForeignKey(Pokemon, related_name="pokemon_2", on_delete=models.CASCADE)
    winner = models.ForeignKey(Pokemon, related_name="pokemon_winner", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_draw(self):
        return self.winner is None

    def calculate_winner(self):
        stats = ['hp', 'attack', 'defense', 'special_attack', 'special_defense', 'speed']

        # Comparar total sin modificar modelo Pokemon
        total_1 = sum(getattr(self.pokemon_1, stat, 0) for stat in stats)
        total_2 = sum(getattr(self.pokemon_2, stat, 0) for stat in stats)

        if total_1 > total_2:
            self.winner = self.pokemon_1
        elif total_2 > total_1:
            self.winner = self.pokemon_2
        else:
            self.winner = None  # Empate

    def get_stat_comparisons(self):
        stats = ['hp', 'attack', 'defense', 'special_attack', 'special_defense', 'speed']
        result = {}

        for stat in stats:
            val1 = getattr(self.pokemon_1, stat, 0)
            val2 = getattr(self.pokemon_2, stat, 0)

            if val1 > val2:
                result[stat] = ['stat-better', 'stat-worse']
            elif val2 > val1:
                result[stat] = ['stat-worse', 'stat-better']
            else:
                result[stat] = ['stat-equal', 'stat-equal']

        # Calcula el total también
        total1 = sum(getattr(self.pokemon_1, stat, 0) for stat in stats)
        total2 = sum(getattr(self.pokemon_2, stat, 0) for stat in stats)

        if total1 > total2:
            result['total'] = ['stat-better', 'stat-worse']
        elif total2 > total1:
            result['total'] = ['stat-worse', 'stat-better']
        else:
            result['total'] = ['stat-equal', 'stat-equal']

        return result