from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from Wypozyczalnia.forms import FormularzKsiazek
from Wypozyczalnia.models import Ksiazka
from django.views.generic import ListView

#strona główna
def home(request):
    if request.method == 'POST':
        form = Ksiazka(request.POST,)
        form.save()
    else:
        form = Ksiazka()
    return render(request, 'homepage.html')

#strona dodawania
def dodaj(request):
    template_name = 'dodaj.html'
    form = FormularzKsiazek(request.POST)
    if request.method == "POST":
        if form.is_valid():
            tytul = form.cleaned_data['tytul']
            form.save()
            return redirect(home)
        else:
            errors = form.errors.as_json()
    return render(request, 'dodaj.html', {"form": form})
