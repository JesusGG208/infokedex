from django.db import models

class Pokemon(models.Model):
    pokedex_id = models.PositiveIntegerField(unique=True, verbose_name="Pokédex ID")
    name = models.CharField(max_length=50, verbose_name="Nombre")
    height = models.FloatField(verbose_name="Altura (dm)")
    weight = models.FloatField(verbose_name="Peso (hg)")
    hp = models.PositiveIntegerField(verbose_name="PS")
    attack = models.PositiveIntegerField(verbose_name="Ataque")
    defense = models.PositiveIntegerField(verbose_name="Defensa")
    special_attack = models.PositiveIntegerField(verbose_name="Ataque especial")
    special_defense = models.PositiveIntegerField(verbose_name="Defensa especial")
    speed = models.PositiveIntegerField(verbose_name="Velocidad")
    is_legendary = models.BooleanField(default=False, verbose_name="¿Es legendario?")
    is_mythical = models.BooleanField(default=False, verbose_name="¿Es mítico?")
    generation = models.PositiveIntegerField(verbose_name="Generación")
    sprite_default = models.URLField(verbose_name="Sprite frontal")
    sprite_shiny = models.URLField(verbose_name="Sprite shiny frontal")
    official_artwork_default = models.URLField(verbose_name="Artwork oficial")
    official_artwork_shiny = models.URLField(blank=True, null=True, verbose_name="Artwork oficial shiny")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")

    def __str__(self):
        return f"{self.pokedex_id} - {self.name}"

    class Meta:
        verbose_name = "Pokémon"
        verbose_name_plural = "Pokémon"
        ordering = ['pokedex_id']


class Type(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name="Nombre")
    icon = models.ImageField(upload_to='types/icons/', verbose_name="Icono")
    named_icon = models.ImageField(upload_to='types/name_types/', verbose_name="Icono con nombre")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tipo"
        verbose_name_plural = "Tipos"
        ordering = ['name']


class PokemonType(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name="types")
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    slot = models.PositiveIntegerField(verbose_name="Slot (1 o 2)")

    def __str__(self):
        return f"{self.pokemon.name} - {self.type.name} (Slot {self.slot})"

    class Meta:
        verbose_name = "Tipo de Pokémon"
        verbose_name_plural = "Tipos de Pokémon"
        unique_together = ('pokemon', 'type', 'slot')
        ordering = ['pokemon', 'slot']


class Ability(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Nombre")
    effect = models.TextField(blank=True, null=True, verbose_name="Efecto")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Habilidad"
        verbose_name_plural = "Habilidades"
        ordering = ['name']


class PokemonAbility(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name="abilities")
    ability = models.ForeignKey(Ability, on_delete=models.CASCADE)
    is_hidden = models.BooleanField(default=False, verbose_name="¿Es oculta?")

    def __str__(self):
        return f"{self.pokemon.name} - {self.ability.name} (Oculta: {'Sí' if self.is_hidden else 'No'})"

    class Meta:
        verbose_name = "Habilidad de Pokémon"
        verbose_name_plural = "Habilidades de Pokémon"
        unique_together = ('pokemon', 'ability')
        ordering = ['pokemon', 'is_hidden']


class Evolution(models.Model):
    from_pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='evolves_to', verbose_name="Evoluciona de")
    to_pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='evolves_from', verbose_name="Evoluciona a")
    trigger = models.CharField(max_length=100, blank=True, null=True, verbose_name="Condición de evolución")
    level = models.PositiveIntegerField(blank=True, null=True, verbose_name="Nivel requerido")
    item = models.CharField(max_length=100, blank=True, null=True, verbose_name="Objeto requerido")

    def __str__(self):
        return f"{self.from_pokemon.name} ➜ {self.to_pokemon.name}"

    class Meta:
        verbose_name = "Evolución"
        verbose_name_plural = "Evoluciones"
        unique_together = ('from_pokemon', 'to_pokemon')
        ordering = ['from_pokemon', 'to_pokemon']
