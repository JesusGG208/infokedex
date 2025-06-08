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
        # Mostrar solo las 5 últimas comparaciones del usuario actual
        context['last_comparisons'] = Compare.objects.filter(user=self.request.user).order_by('-created_at')[:5]
        return context

    def form_valid(self, form):
        pokemon_1 = form.cleaned_data['pokemon_1']
        pokemon_2 = form.cleaned_data['pokemon_2']

        # Crear la comparación asociada al usuario actual
        comparison = Compare(pokemon_1=pokemon_1,pokemon_2=pokemon_2,user=self.request.user)
        comparison.calculate_winner()
        comparison.save()

        # Eliminar comparaciones antiguas de este usuario si hay más de 5
        user_comparisons = Compare.objects.filter(user=self.request.user).order_by('created_at')
        if user_comparisons.count() > 5:
            for c in user_comparisons[:user_comparisons.count() - 5]:
                c.delete()

        # Agregar comparación al contexto para mostrar el resultado
        context = self.get_context_data(form=form)
        context['comparison'] = comparison
        context['stat_colors'] = comparison.get_stat_comparisons()
        return self.render_to_response(context)
