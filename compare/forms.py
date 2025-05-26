from django import forms
from pokemon.models import Pokemon

class ComparisonForm(forms.Form):
    pokemon_1 = forms.ModelChoiceField(queryset=Pokemon.objects.all(), label="Pokémon 1")
    pokemon_2 = forms.ModelChoiceField(queryset=Pokemon.objects.all(), label="Pokémon 2")