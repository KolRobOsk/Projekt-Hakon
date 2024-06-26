from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import django.db.models.options as options
from django.db import transaction
from django.conf import settings
from django.contrib.auth import get_user_model
class Ksiazka(models.Model):
    tytul = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    opis = models.TextField()
    kategoria = models.ForeignKey("Kategoria", on_delete=models.CASCADE)
    def __str__(self):
        return self.tytul
class Recenzja(models.Model):
    ksiazka = models.ForeignKey("Ksiazka", related_name="ksiazeczka", on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(),
        on_delete=models.CASCADE)
    opinia = models.TextField()
    ocena = models.IntegerField(
    default=1,
    validators=[
        MaxValueValidator(5),
        MinValueValidator(1)
    ])
class Kategoria(models.Model):
    nazwa = models.CharField(max_length=255)
    def __str__(self):
        return self.nazwa
class SzukanaKsiazka(Ksiazka):
    def filter():
        return Ksiazka.objects.filter(tytul=tytul)
    def __str__(self):
        return self.tytul
class SzukanaKategoria(Kategoria):
    def filter():
        return Kategoria.objects.filter(nazwa=nazwa)
    def __str__(self):
        return self.tytul
