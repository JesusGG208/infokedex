from django.contrib.auth.mixins import LoginRequiredMixin # Importa un mixin que restringe el acceso a usuarios autenticados
from django.views.generic import FormView # Importa una vista genérica basada en formulario
from .forms import CompareForm # Importa el formulario de comparación personalizado
from .models import Compare # Importa el modelo que representa una comparación de Pokémon

# Vista para comparar dos Pokémon; solo accesible para usuarios autenticados
class PokemonCompareView(LoginRequiredMixin, FormView):
    template_name = "compare.html" # Plantilla HTML que se utilizará
    form_class = CompareForm # Clase de formulario asociada a la vista

    # Añade datos adicionales al contexto del template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agrega las 5 comparaciones más recientes al contexto
        context['last_comparisons'] = Compare.objects.order_by('-created_at')[:5]
        return context

    # Se ejecuta si el formulario es válido (POST con datos correctos)
    def form_valid(self, form):
        # Obtiene los dos Pokémon seleccionados en el formulario
        pokemon_1 = form.cleaned_data['pokemon_1']
        pokemon_2 = form.cleaned_data['pokemon_2']

        # Crea un objeto de comparación y calcula el ganador
        comparison = Compare(pokemon_1=pokemon_1, pokemon_2=pokemon_2)
        comparison.calculate_winner()  # Lógica definida en el modelo
        comparison.save()  # Guarda en la base de datos

        # Elimina comparaciones antiguas si hay más de 5 en total
        all_comparisons = Compare.objects.order_by('created_at')
        if all_comparisons.count() > 5:
            for c in all_comparisons[:all_comparisons.count() - 5]:
                c.delete()

        # Prepara el contexto para renderizar la respuesta
        context = self.get_context_data(form=form)
        context['comparison'] = comparison  # Comparación actual
        context['stat_colors'] = comparison.get_stat_comparisons()  # Colores por estadística comparada
        return self.render_to_response(context)  # Renderiza la plantilla con el contexto
