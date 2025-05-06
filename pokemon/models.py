from django.db import models

class Pokemon(models.Model):
    pokedex_id = models.PositiveIntegerField(unique=True, name="Pokédex ID")
    name = models.CharField(max_length=50, name="Nombre")
    height = models.FloatField(name="Altura (dm)")
    weight = models.FloatField(name="Peso (hg)")
    hp = models.PositiveIntegerField(name="PS")
    attack = models.PositiveIntegerField(name="Ataque")
    defense = models.PositiveIntegerField(name="Defensa")
    special_attack = models.PositiveIntegerField(name="Ataque especial")
    special_defense = models.PositiveIntegerField(name="Defensa especial")
    speed = models.PositiveIntegerField(name="Velocidad")
    is_legendary = models.BooleanField(default=False, name="¿Es legendario?")
    is_mythical = models.BooleanField(default=False, name="¿Es mítico?")
    generation = models.PositiveIntegerField(name="Generación")
    sprite_default = models.URLField(name="Sprite frontal")
    sprite_shiny = models.URLField(name="Sprite shiny frontal")
    description = models.TextField(blank=True, null=True, name="Descripción")

    def __str__(self):
        return f"{self.pokedex_id} - {self.name}"

    class Meta:
        verbose_name = "Pokémon"
        verbose_name_plural = "Pokémon"
        ordering = ["pokedex_id"]

class Type(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name="Nombre")
    image = models.ImageField(upload_to='types/')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tipo"
        verbose_name_plural = "Tipos"

class PokemonType(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name="types")
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    slot = models.PositiveIntegerField(verbose_name="Slot (1 o 2)")  # 1 = Tipo principal, 2 = Secundario

    def __str__(self):
        return f"{self.pokemon.name} - {self.type.name} (Slot {self.slot})"

    class Meta:
        verbose_name = "Tipo de Pokémon"
        verbose_name_plural = "Tipos de Pokémon"
        unique_together = ("pokemon", "slot")  # Un Pokémon no puede tener dos tipos en el mismo slot

class Ability(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Nombre")
    effect = models.TextField(blank=True, null=True, verbose_name="Efecto")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Habilidad"
        verbose_name_plural = "Habilidades"

class PokemonAbility(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name="abilities")
    ability = models.ForeignKey(Ability, on_delete=models.CASCADE)
    is_hidden = models.BooleanField(default=False, verbose_name="¿Es oculta?")

    def __str__(self):
        return f"{self.pokemon.name} - {self.ability.name} (Oculta: {'Sí' if self.is_hidden else 'No'})"

    class Meta:
        verbose_name = "Habilidad de Pokémon"
        verbose_name_plural = "Habilidades de Pokémon"


