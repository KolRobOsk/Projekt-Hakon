from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import django.db.models.options as options
from django.db import transaction

class Ksiazka(models.Model):
    tytul = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    opis = models.TextField()
    kategoria = models.ForeignKey("Kategoria", on_delete=models.CASCADE)
    def __str__(self):
        return self.tytul + '|' + self.autor + '|' + self.opis
class Recenzja(models.Model):
    ksiazka = models.ForeignKey("Ksiazka", on_delete=models.CASCADE)
    autor_rec = models.ForeignKey("Uzytkownik", on_delete=models.CASCADE)
    ocena = models.IntegerField(
    default=1,
    validators=[
        MaxValueValidator(5),
        MinValueValidator(1)
    ])
class Kategoria(models.Model):
    nazwa = models.CharField(max_length=255)
class Uzytkownik(models.Model):
    autor_rec = models.CharField(max_length=40)
    password = models.CharField(max_length=30)
