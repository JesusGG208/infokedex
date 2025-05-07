from django.contrib import admin
from pokemon.models import Pokemon, PokemonType, Type, Ability, PokemonAbility, Evolution

# Register your models here.
admin.site.register(Pokemon)
admin.site.register(Type)
admin.site.register(PokemonType)
admin.site.register(Ability)
admin.site.register(PokemonAbility)
admin.site.register(Evolution)

