from django.db import models
from pokemon.models import Pokemon, Ability, Type

class PokewordleGame(models.Model):
    pokemon_to_guess = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return f"Juego #{self.pk} - Pokémon: {self.pokemon_to_guess.name}"

class PokewordleAttempt(models.Model):
    game = models.ForeignKey(PokewordleGame, on_delete=models.CASCADE, related_name='attempts')
    guess = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Intento #{self.pk} en juego {self.game.pk}: {self.guess}"

class PokewordleHint(models.Model):
    game = models.ForeignKey(PokewordleGame, on_delete=models.CASCADE, related_name='hints')
    hint_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pista #{self.pk} en juego {self.game.pk}"