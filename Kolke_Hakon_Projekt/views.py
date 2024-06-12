from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User

def home(request):
    return render(request, 'homepage.html')

def dodaj(request):
    return render(request, 'dodaj.html')
