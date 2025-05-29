from django.db import models
from pokemon.models import Pokemon

class PokewordleGame(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    attempts = models.PositiveSmallIntegerField(default=0)
    success = models.BooleanField(default=False)

class PokewordleGuess(models.Model):
    game = models.ForeignKey(PokewordleGame, on_delete=models.CASCADE, related_name='guesses')
    guess_text = models.CharField(max_length=50)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)