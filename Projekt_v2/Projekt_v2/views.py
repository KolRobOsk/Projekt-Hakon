from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from wypozyczalnia.forms import FormularzKsiazek
from wypozyczalnia.models import Ksiazka
from django.views.generic import ListView
from django.http import JsonResponse
from collections import Counter
from rest_framework.parsers import JSONParser
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView

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
#strona domowa
class homeview(ListView):
    model = Ksiazka
    template_name = 'homepage.html'
#książka szczegóły
class bookview(DetailView):
    model = Ksiazka
    template_name = 'book.html'
