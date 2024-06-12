from django.db import models

# Create your models here.
# class Ksiazka(models.Model):
#     tytul = models.CharField(max_length=255)
#     autor = models.CharField(max_length=255)
#     opis = models.CharField(max_length=255)
#     kategoria = models.ForeignKey("Recenzja", on_delete=models.CASCADE)
#
# class Recenzja(models.Model):
#     tytul = models.ForeignKey("Ksiazka", on_delete=models.CASCADE)
#     autor = models.ForeignKey("Uzytkownik", on_delete=models.CASCADE)
#     kategoria = models.CharField(max_length=255)
#     ocena = models.IntegerField(
#     default=1,
#         validators=[
#             MaxValueValidator(5),
#             MinValueValidator(1)
#         ])
#
# class Uzytkownik(models.Model):
#     autor = models.CharField(max_length=255)
