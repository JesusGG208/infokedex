from django.db import models

# Modelo principal que representa a un Pokémon con sus estadísticas y datos generales.
class Pokemon(models.Model):
    pokedex_id = models.PositiveIntegerField(unique=True, verbose_name="Pokédex ID")  # ID único del Pokémon en la Pokédex
    name = models.CharField(max_length=50, verbose_name="Nombre")  # Nombre del Pokémon
    height = models.FloatField(verbose_name="Altura (dm)")  # Altura en decímetros
    weight = models.FloatField(verbose_name="Peso (hg)")  # Peso en hectogramos
    hp = models.PositiveIntegerField(verbose_name="PS")  # Puntos de salud
    attack = models.PositiveIntegerField(verbose_name="Ataque")  # Estadística de ataque
    defense = models.PositiveIntegerField(verbose_name="Defensa")  # Estadística de defensa
    special_attack = models.PositiveIntegerField(verbose_name="Ataque especial")  # Ataque especial
    special_defense = models.PositiveIntegerField(verbose_name="Defensa especial")  # Defensa especial
    speed = models.PositiveIntegerField(verbose_name="Velocidad")  # Velocidad
    is_legendary = models.BooleanField(default=False, verbose_name="¿Es legendario?")  # Indicador si es legendario
    is_mythical = models.BooleanField(default=False, verbose_name="¿Es mítico?")  # Indicador si es mítico
    generation = models.PositiveIntegerField(verbose_name="Generación")  # Generación del Pokémon
    sprite_default = models.URLField(verbose_name="Sprite frontal")  # URL al sprite frontal estándar
    sprite_shiny = models.URLField(verbose_name="Sprite shiny frontal")  # URL al sprite frontal shiny
    official_artwork_default = models.URLField(verbose_name="Artwork oficial")  # URL al arte oficial normal
    official_artwork_shiny = models.URLField(blank=True, null=True, verbose_name="Artwork oficial shiny")  # URL opcional al arte shiny
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")  # Descripción opcional

    def __str__(self):
        return f"{self.pokedex_id} - {self.name}"

    class Meta:
        verbose_name = "Pokémon"
        verbose_name_plural = "Pokémon"
        ordering = ['pokedex_id']  # Orden por ID de Pokédex


# Modelo que representa un tipo de Pokémon (agua, fuego, planta, etc.)
class Type(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name="Nombre")  # Nombre del tipo
    named_icon = models.ImageField(upload_to='types/name_types/', verbose_name="Icono con nombre")  # Icono representativo

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tipo"
        verbose_name_plural = "Tipos"
        ordering = ['name']


# Modelo intermedio para asociar tipos a un Pokémon, indicando su posición (1º o 2º tipo).
class PokemonType(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name="types")  # Pokémon asociado
    type = models.ForeignKey(Type, on_delete=models.CASCADE)  # Tipo asignado
    slot = models.PositiveIntegerField(verbose_name="Slot (1 o 2)")  # Posición del tipo (1 = principal, 2 = secundario)

    def __str__(self):
        return f"{self.pokemon.name} - {self.type.name} (Slot {self.slot})"

    class Meta:
        verbose_name = "Tipo de Pokémon"
        verbose_name_plural = "Tipos de Pokémon"
        unique_together = ('pokemon', 'type', 'slot')  # Combinación única de Pokémon, tipo y slot
        ordering = ['pokemon', 'slot']


# Modelo que representa una habilidad que puede tener un Pokémon
class Ability(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Nombre")  # Nombre de la habilidad
    effect = models.TextField(blank=True, null=True, verbose_name="Efecto")  # Descripción del efecto de la habilidad

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Habilidad"
        verbose_name_plural = "Habilidades"
        ordering = ['name']


# Modelo intermedio para asociar habilidades a Pokémon, permitiendo marcar si es una habilidad oculta.
class PokemonAbility(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name="abilities")  # Pokémon asociado
    ability = models.ForeignKey(Ability, on_delete=models.CASCADE)  # Habilidad asociada
    is_hidden = models.BooleanField(default=False, verbose_name="¿Es oculta?")  # Indica si la habilidad es oculta

    def __str__(self):
        return f"{self.pokemon.name} - {self.ability.name} (Oculta: {'Sí' if self.is_hidden else 'No'})"

    class Meta:
        verbose_name = "Habilidad de Pokémon"
        verbose_name_plural = "Habilidades de Pokémon"
        unique_together = ('pokemon', 'ability')  # Evita duplicidad de habilidades por Pokémon
        ordering = ['pokemon', 'is_hidden']


# Modelo que representa una evolución de un Pokémon a otro.
class Evolution(models.Model):
    from_pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='evolves_to', verbose_name="Evoluciona de")  # Pokémon base
    to_pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='evolves_from', verbose_name="Evoluciona a")  # Pokémon resultado
    trigger = models.CharField(max_length=100, blank=True, null=True, verbose_name="Condición de evolución")  # Condición de evolución (por nivel, objeto, etc.)
    level = models.PositiveIntegerField(blank=True, null=True, verbose_name="Nivel requerido")  # Nivel necesario, si aplica
    item = models.CharField(max_length=100, blank=True, null=True, verbose_name="Objeto requerido")  # Objeto necesario, si aplica

    def __str__(self):
        return f"{self.from_pokemon.name} ➜ {self.to_pokemon.name}"

    class Meta:
        verbose_name = "Evolución"
        verbose_name_plural = "Evoluciones"
        unique_together = ('from_pokemon', 'to_pokemon')  # Impide duplicación de evoluciones
        ordering = ['from_pokemon', 'to_pokemon']