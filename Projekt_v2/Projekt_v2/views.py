from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from wypozyczalnia.forms import FormularzKsiazek, FormularzRecenzji, FormularzKategorii
from wypozyczalnia.models import Ksiazka
from django.views.generic import ListView
from django.http import JsonResponse
from collections import Counter
from rest_framework.parsers import JSONParser
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
#wyszukiwanie kategorii w bazie danych
def kategorie(request):
    kategorie = kategoria.objects.all()
    kategorie = serializers.serialize("xml", kategorie)
    return JsonResponse(kategorie, safe=False)
#wyszukiwanie książek w bazie danych
def ksiazki(request):
    ksiazki = Ksiazka.objects.all()
    ksiazki = serializers.serialize("xml", ksiazki)
    return JsonResponse(ksiazki, safe=False)
#strona dodawania
def dodaj(request):
    template_name = 'dodaj.html'
    formularz = FormularzKsiazek(request.POST)
    if request.method == 'POST':
        if formularz.is_valid():
            formularz.save()
        else:
            formularz = FormularzKsiazek()
    formularz = FormularzKsiazek()
    return render(request, 'dodaj.html', {'formularz':formularz})
#dodawanie recenzji
def dodajrec(request):
    template_name = 'dodajRecenzje.html'
    formularz2 = FormularzRecenzji(request.POST)
    if request.method == 'POST':
        if formularz2.is_valid():
            formularz2.save()
        else:
            formularz2 = FormularzRecenzji()
    formularz2 = FormularzRecenzji()
    return render(request, 'dodajRecenzje.html', {'formularz2':formularz2})
#dodawanie kategorii
def dodajkat(request):
    template_name = 'dodajKategorie.html'
    formularz3 = FormularzKategorii(request.POST)
    if request.method == 'POST':
        if formularz3.is_valid():
            formularz3.save()
        else:
            formularz3 = FormularzKategorii()
    formularz3 = FormularzKategorii()
    return render(request, 'dodajKategorie.html', {'formularz3':formularz3})
#strona domowa
class homeview(ListView):
    model = Ksiazka
    template_name = 'homepage.html'
#książka szczegóły
class bookview(DetailView):
    model = Ksiazka
    template_name = 'book.html'
