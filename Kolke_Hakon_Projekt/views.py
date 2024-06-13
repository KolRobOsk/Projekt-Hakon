from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from Wypozyczalnia.forms import FormularzKsiazek
from Wypozyczalnia.models import Ksiazka
from django.views.generic import ListView
from django.http import JsonResponse
from collections import Counter
from rest_framework.parsers import JSONParser
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

#strona główna
def home(request):
    return render(request, 'homepage.html')

def ksiazki(request):
    ksiazki = Ksiazka.objects.all()
    ksiazki = serializers.serialize("json", ksiazki)
    return JsonResponse(ksiazki, safe=False)

#strona dodawania
def dodaj(request):
    template_name = 'dodaj.html'
    formularz = FormularzKsiazek(request.POST)
    if request.method == 'POST':
        if formularz.is_valid():
            formularz.save()
            return redirect(home)
    else:
        formularz = FormularzKsiazek()
    return render(request, 'dodaj.html', {'formularz':formularz})
