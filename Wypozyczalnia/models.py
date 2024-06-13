from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Ksiazka(models.Model):
    tytul = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    opis = models.CharField(max_length=255)
    def __str__(self):
        return self.name
#    kategoria = models.ForeignKey("Recenzja", on_delete=models.CASCADE)

# class Recenzja(models.Model):
#     tytul = models.ForeignKey("Ksiazka", on_delete=models.CASCADE)
#     autor_rec = models.ForeignKey("Uzytkownik", on_delete=models.CASCADE)
#     kategoria = models.CharField(max_length=255)
#     ocena = models.IntegerField(
#     default=1,
#         validators=[
#             MaxValueValidator(5),
#             MinValueValidator(1)
#         ])
#
# class Uzytkownik(models.Model):
#     autor_rec = models.CharField(max_length=255)
