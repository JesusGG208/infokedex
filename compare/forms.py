from django import forms
from pokemon.models import Pokemon

class CompareForm(forms.Form):
    pokemon_1 = forms.ModelChoiceField(queryset=Pokemon.objects.all(), label="Pokémon 1")
    pokemon_2 = forms.ModelChoiceField(queryset=Pokemon.objects.all(), label="Pokémon 2")

    def clean(self):
        cleaned_data = super().clean()
        pokemon_1 = cleaned_data.get("pokemon_1")
        pokemon_2 = cleaned_data.get("pokemon_2")

        if pokemon_1 == pokemon_2:
            raise forms.ValidationError("Debes seleccionar dos Pokémon diferentes.")

        return cleaned_data