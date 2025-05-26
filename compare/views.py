from django.views.generic import FormView
from django.shortcuts import get_object_or_404
from .models import Comparison
from pokemon.models import Pokemon
from .forms import ComparisonForm

class PokemonCompareView(FormView):
    template_name = "compare.html"
    form_class = ComparisonForm

    def form_valid(self, form):
        p1 = get_object_or_404(Pokemon, id=form.cleaned_data['pokemon_1'].id)
        p2 = get_object_or_404(Pokemon, id=form.cleaned_data['pokemon_2'].id)

        stats = ["hp", "attack", "defense", "special_attack", "special_defense", "speed"]

        p1_score = sum(getattr(p1, stat) for stat in stats)
        p2_score = sum(getattr(p2, stat) for stat in stats)

        if p1_score > p2_score:
            winner = p1
        elif p2_score > p1_score:
            winner = p2
        else:
            winner = None

        comparison = Comparison.objects.create(
            pokemon_1=p1, pokemon_2=p2, winner=winner
        )

        context = self.get_context_data(
            form=form,
            result={
                "comparison": comparison,
                "p1_score": p1_score,
                "p2_score": p2_score,
            }
        )
        return self.render_to_response(context)