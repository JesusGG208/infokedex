from django import forms # Importa el módulo de formularios de Django
from pokemon.models import Pokemon # Importa el modelo Pokemon desde la app correspondiente

# Formulario que permite seleccionar dos Pokémon para comparar
class CompareForm(forms.Form):
    pokemon_1 = forms.ModelChoiceField(queryset=Pokemon.objects.all(), label="Pokémon 1") # Campo para seleccionar el primer Pokémon, usando un desplegable de todos los Pokémon disponibles
    pokemon_2 = forms.ModelChoiceField(queryset=Pokemon.objects.all(), label="Pokémon 2") # Campo para seleccionar el segundo Pokémon

    # Metodo de validación adicional para el formulario completo
    def clean(self):
        # Llama al metodo de limpieza del formulario base
        cleaned_data = super().clean()
        pokemon_1 = cleaned_data.get("pokemon_1")
        pokemon_2 = cleaned_data.get("pokemon_2")

        # Verifica que no se hayan seleccionado el mismo Pokémon en ambos campos
        if pokemon_1 == pokemon_2:
            raise forms.ValidationError("Debes seleccionar dos Pokémon diferentes.")

        # Devuelve los datos validados
        return cleaned_data
