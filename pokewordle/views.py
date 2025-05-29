from django.views.generic import DetailView, View
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .models import PokewordleGame, PokewordleGuess
from pokemon.models import Pokemon
import random

class StartPokewordleGame(View):
    def get(self, request):
        pokemon = random.choice(Pokemon.objects.all())
        game = PokewordleGame.objects.create(pokemon=pokemon)
        return redirect(reverse('pokewordle:play', kwargs={'pk': game.pk}))

class PlayPokewordleGame(DetailView):
    model = PokewordleGame
    template_name = 'play.html'
    context_object_name = 'game'

    def post(self, request, *args, **kwargs):
        game = self.get_object()
        if game.completed:
            return redirect(reverse('pokewordle:play', kwargs={'pk': game.pk}))

        guess_text = request.POST.get('guess', '').strip()
        is_correct = guess_text.lower() == game.pokemon.name.lower()

        PokewordleGuess.objects.create(game=game, guess_text=guess_text, is_correct=is_correct)

        game.attempts += 1
        if is_correct:
            game.success = True
            game.completed = True
        elif game.attempts >= 7:
            game.completed = True
        game.save()
        return redirect(reverse('pokewordle:play', kwargs={'pk': game.pk}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = self.get_object()
        pokemon = game.pokemon
        context['guesses'] = game.guesses.all()

        if game.attempts >= 2:
            context['hint_1'] = ', '.join([a.ability.name for a in pokemon.abilities.all()])
        if game.attempts >= 4:
            context['hint_2'] = f"Generación {pokemon.generation}"
        if game.attempts >= 6:
            context['hint_3'] = ', '.join([pt.type.name for pt in pokemon.types.all()])
        return context
