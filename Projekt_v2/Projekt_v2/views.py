from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic.edit import CreateView
from wypozyczalnia.forms import FormularzKsiazek, FormularzRecenzji, FormularzKategorii, FormularzSzukania, FormularzFiltrowania
from wypozyczalnia.models import Ksiazka, Kategoria, SzukanaKsiazka, Recenzja
from django.views.generic import ListView
from django.http import JsonResponse
from collections import Counter, defaultdict
from rest_framework.parsers import JSONParser
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from django.views import generic
from urllib.parse import urlparse
from django.forms.models import model_to_dict
import json
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.contrib.auth import get_user_model
#filtrowanie książek nowe
def filtruj_ksiazki(tytul):
    lista_ksiazek=[]
    lista_ksiazek=[ksiazka.pk for ksiazka in Ksiazka.objects.all() if not tytul.lower() in ksiazka.tytul.lower()]
    lista_ksiazek = Ksiazka.objects.exclude(pk__in=lista_ksiazek)
    return lista_ksiazek
#filtrowanie po kategoriach
def filtruj_ksiazki_kat(tytul):
    lista_ksiazek=[]
    lista_ksiazek=[ksiazka.pk for ksiazka in Ksiazka.objects.all() if not tytul.lower() in ksiazka.kategoria.nazwa.lower()]
    lista_ksiazek = Ksiazka.objects.exclude(pk__in=lista_ksiazek)
    return lista_ksiazek
#filtrowanie ocen po tytulach
def oceny_po_tytulach(tytul):
    wybrane_recenzje, oceny, i = Recenzja.objects.filter(ksiazka=tytul), 0, 0
    for recenzja in wybrane_recenzje:
        i += 1
        oceny += recenzja.ocena
    return oceny/i
#strona dodawania
def dodaj(request):
    template_name = 'dodaj.html'
    formularz = FormularzKsiazek(request.POST)
    if request.method == 'POST':
        if formularz.is_valid():
            formularz.save()
        else:
            formularz = FormularzKsiazek()
    return render(request, 'dodaj.html', {'filtr_kategorii':FormularzFiltrowania(request.POST), 'formularz':formularz})
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
    return render(request, 'dodajKategorie.html', {'filtr_kategorii':FormularzFiltrowania(request.POST), 'formularz3':formularz3})
#strona domowa
def homeview(request):
    kategorie_do_filtrow, ksiazki_pk, tabela_srednich_ocen, ksiazki, recenzje  =  Kategoria.objects.all(), Ksiazka.objects.all().count(), [[],[]], Ksiazka.objects.all(), Recenzja.objects.all()
    for i in range(ksiazki_pk):
        tabela_srednich_ocen[0].append(float(0))
        tabela_srednich_ocen[1].append(float(0))
    for recenzja in recenzje:
        if Ksiazka.objects.get(tytul=recenzja.ksiazka):
            tabela_srednich_ocen[0][Ksiazka.objects.get(tytul=recenzja.ksiazka).pk-1] += recenzja.ocena
            tabela_srednich_ocen[1][Ksiazka.objects.get(tytul=recenzja.ksiazka).pk-1] += 1
    if len(tabela_srednich_ocen)==0:
        pass
    else:
        for i in range(len(tabela_srednich_ocen)-1):
            if tabela_srednich_ocen[0][i] == 0:
                pass
            else:
                tabela_srednich_ocen[0][i]=round(tabela_srednich_ocen[0][i]/tabela_srednich_ocen[1][i], 2)
    return render(request, 'homepage.html', {'filtr_kategorii':FormularzFiltrowania(request.POST), 'ksiazki': ksiazki, 'srednie_oceny': tabela_srednich_ocen, 'kategorie':kategorie_do_filtrow})
#książka szczegóły
def bookview(request, pk):
    template_name = 'book.html'
    formularz = FormularzRecenzji(request.POST)
    if request.method == 'POST':
        if formularz.is_valid():
            formularz.save()
    return render(request, 'book.html', {'recenzje': Recenzja.objects.all(), 'ksiazka': Ksiazka.objects.get(pk=pk), 'formularz':formularz})
#strona wyszukiwanie
def filterview(request, tytul):
    ksiazki_pk, kategorie_do_filtrow = Ksiazka.objects.all().count(), Kategoria.objects.all()
    tabela_srednich_ocen, ksiazki, recenzje  = [[],[]], Ksiazka.objects.all(), Recenzja.objects.all()
    for i in range(ksiazki_pk):
        tabela_srednich_ocen[0].append(float(0))
        tabela_srednich_ocen[1].append(float(0))
    for recenzja in recenzje:
        if Ksiazka.objects.get(tytul=recenzja.ksiazka):
            tabela_srednich_ocen[0][Ksiazka.objects.get(tytul=recenzja.ksiazka).pk-1] += recenzja.ocena
            tabela_srednich_ocen[1][Ksiazka.objects.get(tytul=recenzja.ksiazka).pk-1] += 1
    if len(tabela_srednich_ocen)==0:
        pass
    else:
        for i in range(len(tabela_srednich_ocen)-1):
            if tabela_srednich_ocen[0][i] == 0:
                pass
            else:
                tabela_srednich_ocen[0][i]=round(tabela_srednich_ocen[0][i]/tabela_srednich_ocen[1][i], 2)
    ksiazki_adres = request.build_absolute_uri()
    ksiazki_adres = tytul.split("filter/",1)[0]
    ksiazki = filtruj_ksiazki(ksiazki_adres)
    return render(request, 'filtruj.html', {'filtr_kategorii':FormularzFiltrowania(request.POST), 'ksiazki':ksiazki, 'srednie_oceny': tabela_srednich_ocen, 'kategorie':kategorie_do_filtrow})
#tworzenie użytkownika
class RejestracjaUzytkownikaView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'rejestracja.html'
    success_url = '/home'
    def get_initial(self):
        return {'Recenzje': Recenzja.objects.all()}
def katview(request, kategoria):
    ksiazki_pk, kategorie_do_filtrow = Ksiazka.objects.all().count(), Kategoria.objects.all()
    tabela_srednich_ocen, ksiazki, recenzje  = [[],[]], Ksiazka.objects.all(), Recenzja.objects.all()
    for i in range(ksiazki_pk):
        tabela_srednich_ocen[0].append(float(0))
        tabela_srednich_ocen[1].append(float(0))
    for recenzja in recenzje:
        if Ksiazka.objects.get(tytul=recenzja.ksiazka):
            tabela_srednich_ocen[0][Ksiazka.objects.get(tytul=recenzja.ksiazka).pk-1] += recenzja.ocena
            tabela_srednich_ocen[1][Ksiazka.objects.get(tytul=recenzja.ksiazka).pk-1] += 1
    if len(tabela_srednich_ocen)==0:
        pass
    else:
        for i in range(len(tabela_srednich_ocen)-1):
            if tabela_srednich_ocen[0][i] == 0:
                pass
            else:
                tabela_srednich_ocen[0][i]=round(tabela_srednich_ocen[0][i]/tabela_srednich_ocen[1][i], 2)
    ksiazki_adres = request.build_absolute_uri()
    ksiazki_adres = kategoria.split("kat/",1)[0]
    ksiazki = filtruj_ksiazki_kat(ksiazki_adres)
    return render(request, 'filtruj_kat.html', {'filtr_kategorii':FormularzFiltrowania(request.POST), 'ksiazki':ksiazki, 'srednie_oceny': tabela_srednich_ocen, 'kategorie':kategorie_do_filtrow})
