from django.db import models

# Create your models here.
class Pokemon(models.Model):
    name = models.CharField(max_length=200, unique=True)
    primary_type = models.CharField(max_length=200)
    secondary_type = models.CharField(max_length=200)
    hp = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    special_attack = models.IntegerField()
    special_deffense = models.IntegerField()
    speed = models.IntegerField()

    def __str__(self):
        return f"{self.name}"