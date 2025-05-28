import random
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import PokewordleGame, PokewordleAttempt, PokewordleHint
from pokemon.models import Pokemon, PokemonAbility, PokemonType


class StartGameView(View):
    def get(self, request, *args, **kwargs):
        pokemon = random.choice(Pokemon.objects.all())
        game = PokewordleGame.objects.create(pokemon_to_guess=pokemon)
        return redirect(reverse('pokewordle:play_game', kwargs={'game_id': game.id}))


class PlayGameView(View):
    template_name = 'pokewordle.html'

    def get(self, request, game_id, *args, **kwargs):
        game = get_object_or_404(PokewordleGame, id=game_id)
        context = self.get_context_data(game=game, message='', hint1=None, hint2=None)
        return render(request, self.template_name, context)

    def post(self, request, game_id, *args, **kwargs):
        game = get_object_or_404(PokewordleGame, id=game_id)
        guess = request.POST.get('guess', '').strip().lower()
        message = ''
        hint1 = None
        hint2 = None

        if game.is_finished:
            # Si ya terminó, solo mostrar resultado
            context = self.get_context_data(game=game, message=message, hint1=hint1, hint2=hint2)
            return render(request, self.template_name, context)

        is_correct = guess == game.pokemon_to_guess.name.lower()
        PokewordleAttempt.objects.create(game=game, guess=guess, is_correct=is_correct)

        if is_correct:
            game.is_finished = True
            game.save()
            return redirect(reverse('pokewordle:play_game', kwargs={'game_id': game.id}))
        else:
            message = "¡Incorrecto! Sigue intentando."

        attempts_count = game.attempts.count()

        if attempts_count == 3:
            abilities = PokemonAbility.objects.filter(pokemon=game.pokemon_to_guess)
            ability_names = [a.ability.name for a in abilities]
            hint_text = f"Habilidad: {', '.join(ability_names)}"
            PokewordleHint.objects.create(game=game, hint_text=hint_text)
            hint1 = hint_text

        if attempts_count == 5:
            types = PokemonType.objects.filter(pokemon=game.pokemon_to_guess).order_by('slot')
            type_names = [t.type.name for t in types]
            hint_text = f"Tipo(s): {', '.join(type_names)}"
            PokewordleHint.objects.create(game=game, hint_text=hint_text)
            hint2 = hint_text

        # Mostrar pistas previas si existen
        hints = game.hints.all().order_by('created_at')
        if not hint1 and hints.count() >= 1:
            hint1 = hints[0].hint_text
        if not hint2 and hints.count() >= 2:
            hint2 = hints[1].hint_text

        context = self.get_context_data(game=game, message=message, hint1=hint1, hint2=hint2)
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        game = kwargs.get('game')
        message = kwargs.get('message', '')
        hint1 = kwargs.get('hint1')
        hint2 = kwargs.get('hint2')

        context = {
            'game': game,
            'attempts': game.attempts.all(),
            'message': message,
            'hint1': hint1,
            'hint2': hint2,
        }
        return context
