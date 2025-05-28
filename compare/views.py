from django.views.generic import FormView
from .forms import CompareForm
from .models import Compare


class PokemonCompareView(FormView):
    template_name = "compare.html"
    form_class = CompareForm

    def form_valid(self, form):
        pokemon_1 = form.cleaned_data['pokemon_1']
        pokemon_2 = form.cleaned_data['pokemon_2']

        comparison = Compare(pokemon_1=pokemon_1, pokemon_2=pokemon_2)
        comparison.calculate_winner()
        comparison.save()

        context = self.get_context_data(form=form)
        context['comparison'] = comparison
        context['stat_colors'] = comparison.get_stat_comparisons()
        return self.render_to_response(context)