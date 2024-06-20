from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from wypozyczalnia.forms import FormularzKsiazek, FormularzRecenzji, FormularzKategorii, FormularzSzukania
from wypozyczalnia.models import Ksiazka, Kategoria, SzukanaKsiazka, Recenzja
from django.views.generic import ListView
from django.http import JsonResponse
from collections import Counter
from rest_framework.parsers import JSONParser
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from django.views import generic
from urllib.parse import urlparse
from django.forms.models import model_to_dict
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
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
#wyszukiwanie czesci książek w bazie danych
def czesc_ksiazek(tytuly):
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
    return render(request, 'dodajKategorie.html', {'formularz3':formularz3})
#strona domowa
def homeview(request):
    object_list = Ksiazka.objects.all()
    object_list_serialized = serializers.serialize('json', object_list)
    return render(request, 'homepage.html', {'object_list':object_list})
#książka szczegóły
class bookview(DetailView):
    model = Ksiazka
    template_name = 'book.html'
#strona wyszukiwanie
def filterview(request, tytul):
    ksiazki_adres = request.build_absolute_uri()
    ksiazki_adres = tytul.split("filter/",1)[0]
    ksiazki = filtruj_ksiazki(ksiazki_adres)
    return render(request, 'filtruj.html', {'object_list_serialized':ksiazki})
#filtrowanie książek nowe
def filtruj_ksiazki(tytul):
    lista_ksiazek=[]
    lista_ksiazek=[ksiazka.pk for ksiazka in Ksiazka.objects.all() if not tytul.lower() in ksiazka.tytul.lower()]
    lista_ksiazek = Ksiazka.objects.exclude(pk__in=lista_ksiazek)
    return lista_ksiazek
#tworzenie użytkownika
class RejestracjaUzytkownikaView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'rejestracja.html'
    success_url = '/home'
    def get_initial(self):
        return { 'Recenzje': Recenzja.objects.all() }
