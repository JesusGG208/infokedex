from django.contrib.auth.models import User
from django.db import models # Importa el sistema de modelos de Django
from pokemon.models import Pokemon # Importa el modelo de Pokémon desde la app correspondiente

# Modelo que representa una comparación entre dos Pokémon
class Compare(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    pokemon_1 = models.ForeignKey(Pokemon, related_name="pokemon_1", on_delete=models.CASCADE) # Relación con el primer Pokémon
    pokemon_2 = models.ForeignKey(Pokemon, related_name="pokemon_2", on_delete=models.CASCADE) # Relación con el segundo Pokémon
    winner = models.ForeignKey(Pokemon, related_name="pokemon_winner", on_delete=models.SET_NULL, null=True, blank=True) # Pokémon ganador (puede ser nulo si hay empate o no se ha calculado aún)
    created_at = models.DateTimeField(auto_now_add=True) # Fecha y hora de creación de la comparación (se establece automáticamente)

    # Metodo que indica si la comparación resultó en empate
    def is_draw(self):
        return self.winner is None

    # Calcula cuál Pokémon gana comparando el total de estadísticas básicas
    def calculate_winner(self):
        # Lista de estadísticas que se compararán
        stats = ['hp', 'attack', 'defense', 'special_attack', 'special_defense', 'speed']

        # Suma total de estadísticas para cada Pokémon usando getattr para obtener cada atributo
        total_1 = sum(getattr(self.pokemon_1, stat, 0) for stat in stats)
        total_2 = sum(getattr(self.pokemon_2, stat, 0) for stat in stats)

        # Asigna como ganador al que tenga mayor total, o deja como empate (None)
        if total_1 > total_2:
            self.winner = self.pokemon_1
        elif total_2 > total_1:
            self.winner = self.pokemon_2
        else:
            self.winner = None  # Empate

    # Genera un diccionario que indica cuál Pokémon es mejor en cada estadística (para visualización)
    def get_stat_comparisons(self):
        stats = ['hp', 'attack', 'defense', 'special_attack', 'special_defense', 'speed']
        result = {}

        # Compara estadística por estadística y asigna clases CSS apropiadas
        for stat in stats:
            val1 = getattr(self.pokemon_1, stat, 0)
            val2 = getattr(self.pokemon_2, stat, 0)

            if val1 > val2:
                result[stat] = ['stat-better', 'stat-worse']
            elif val2 > val1:
                result[stat] = ['stat-worse', 'stat-better']
            else:
                result[stat] = ['stat-equal', 'stat-equal']

        # También compara el total general de estadísticas
        total1 = sum(getattr(self.pokemon_1, stat, 0) for stat in stats)
        total2 = sum(getattr(self.pokemon_2, stat, 0) for stat in stats)

        if total1 > total2:
            result['total'] = ['stat-better', 'stat-worse']
        elif total2 > total1:
            result['total'] = ['stat-worse', 'stat-better']
        else:
            result['total'] = ['stat-equal', 'stat-equal']

        return result
