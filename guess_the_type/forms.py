from django import forms

class TypeGuessForm(forms.Form):
    pokemon_id = forms.IntegerField(widget=forms.HiddenInput())
    selected_option = forms.CharField(label="¿Qué tipo tiene?", widget=forms.RadioSelect)
    options_list = forms.CharField(widget=forms.HiddenInput())