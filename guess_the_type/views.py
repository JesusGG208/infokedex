from django.views.generic import FormView
from guess_the_type.forms import TypeGuessForm
from pokemon.models import Type, Pokemon
import random

# Vista basada en clase que maneja el juego de adivinar los tipos de un Pokémon aleatorio
class TypeGuessGameView(FormView):
    template_name = 'guess_the_type.html'  # Plantilla HTML que se usará
    form_class = TypeGuessForm  # Formulario que se renderiza en la vista

    def get_initial(self):
        # Obtiene un Pokémon aleatorio desde la base de datos
        pokemon = Pokemon.objects.order_by('?').first()
        self.pokemon = pokemon  # Guardamos el Pokémon para acceder luego en el contexto

        # Recupera los tipos reales del Pokémon
        types = Type.objects.filter(pokemontype__pokemon=pokemon)
        correct_names = sorted([t.name for t in types])  # Lista con nombres de tipos ordenados
        correct = ', '.join(correct_names)  # String con los tipos separados por coma (p.ej. "Fuego, Volador")
        self.correct_answer = correct  # Guardamos la respuesta correcta para usar más adelante

        # Verificamos cuántos tipos tiene el Pokémon (1 o 2)
        num_types = len(correct_names)

        # Obtenemos todos los nombres de tipos que NO tiene este Pokémon
        all_type_names = list(Type.objects.exclude(id__in=[t.id for t in types]).values_list('name', flat=True))

        wrong_options = set()  # Conjunto para asegurar que no se repitan las opciones incorrectas

        # Generamos 2 combinaciones incorrectas con el mismo número de tipos que el correcto
        while len(wrong_options) < 2:
            sample = sorted(random.sample(all_type_names, num_types))  # Escoge tipos aleatorios
            candidate = ', '.join(sample)
            if candidate != correct:  # Asegura que la opción incorrecta no sea igual a la correcta
                wrong_options.add(candidate)

        # Mezcla la respuesta correcta con las incorrectas
        options = [correct] + list(wrong_options)
        random.shuffle(options)
        self.options = options  # Guardamos las opciones para reutilizarlas en el formulario

        return {
            'pokemon_id': pokemon.id,
            'options_list': '|'.join(options)  # Pasamos las opciones codificadas como string separado por '|'
        }

    def get_form(self, form_class=None):
        # Construye el formulario base
        form = super().get_form(form_class)

        # Si es un POST, recuperamos las opciones que se enviaron en el formulario
        if self.request.method == 'POST':
            options = self.request.POST.get('options_list', '').split('|')
        else:
            # Si es GET, usamos las opciones generadas en get_initial
            options = getattr(self, 'options', [])

        # Seteamos las opciones del widget como choices del campo 'selected_option'
        form.fields['selected_option'].widget.choices = [(opt, opt) for opt in options]
        return form

    def form_valid(self, form):
        # Se llama cuando el formulario es válido (POST correcto)
        selected = form.cleaned_data['selected_option']  # Opción elegida por el usuario
        pokemon = Pokemon.objects.get(id=form.cleaned_data['pokemon_id'])  # Recuperamos el Pokémon usando su ID

        # Volvemos a calcular los tipos correctos del Pokémon
        types = Type.objects.filter(pokemontype__pokemon=pokemon)
        correct = ', '.join(sorted([t.name for t in types]))
        is_correct = (selected == correct)  # Comparamos la opción del usuario con la correcta

        # Devolvemos la respuesta renderizada con la información del resultado
        return self.render_to_response({
            'form': form,
            'answered': True,
            'is_correct': is_correct,
            'correct_answer': correct,
            'selected_option': selected,
            'pokemon': pokemon,
        })

    def get_context_data(self, **kwargs):
        # Añadimos el Pokémon al contexto si no está ya presente
        context = super().get_context_data(**kwargs)
        if 'pokemon' not in context:
            context['pokemon'] = getattr(self, 'pokemon', None)
        return context
