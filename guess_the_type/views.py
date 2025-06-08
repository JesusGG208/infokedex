from django.views.generic import FormView
from guess_the_type.forms import TypeGuessForm
from pokemon.models import Type, Pokemon
import random

class TypeGuessGameView(FormView):
    template_name = 'guess_the_type.html'
    form_class = TypeGuessForm

    def get_initial(self):
        # Elegimos un Pokémon y los tipos correctos
        pokemon = Pokemon.objects.order_by('?').first()
        self.pokemon = pokemon

        types = Type.objects.filter(pokemontype__pokemon=pokemon)
        correct = ', '.join(sorted([t.name for t in types]))
        self.correct_answer = correct

        # Generamos opciones
        all_types = list(Type.objects.exclude(id__in=[t.id for t in types]))
        wrong = random.sample(all_types, 2)
        options = [correct] + [t.name for t in wrong]
        random.shuffle(options)
        self.options = options

        return {
            'pokemon_id': pokemon.id,
            'options_list': '|'.join(options)
        }

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        if self.request.method == 'POST':
            options = self.request.POST.get('options_list', '').split('|')
        else:
            options = getattr(self, 'options', [])

        form.fields['selected_option'].widget.choices = [(opt, opt) for opt in options]
        return form

    def form_valid(self, form):
        selected = form.cleaned_data['selected_option']
        pokemon = Pokemon.objects.get(id=form.cleaned_data['pokemon_id'])

        # Obtener tipos correctos de nuevo
        types = Type.objects.filter(pokemontype__pokemon=pokemon)
        correct = ', '.join(sorted([t.name for t in types]))
        is_correct = (selected == correct)

        return self.render_to_response({
            'form': form,
            'answered': True,
            'is_correct': is_correct,
            'correct_answer': correct,
            'selected_option': selected,
            'pokemon': pokemon,
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'pokemon' not in context:
            context['pokemon'] = getattr(self, 'pokemon', None)

        return context