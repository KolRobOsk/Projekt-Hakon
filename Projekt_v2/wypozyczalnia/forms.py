from django import forms
from .models import Ksiazka, Recenzja, Kategoria, SzukanaKsiazka, SzukanaKategoria
from django.core import serializers
from django_filters.views import FilterView
class FormularzKsiazek(forms.ModelForm):
    class Meta:
        model = Ksiazka
        fields = '__all__'
        require_all_fields=True
class FormularzRecenzji(forms.ModelForm):
    class Meta:
        model = Recenzja
        fields = '__all__'
        require_all_fields=True
class FormularzKategorii(forms.ModelForm):
    class Meta:
        model = Kategoria
        fields = '__all__'
        require_all_fields=True
class FormularzSzukania(forms.ModelForm):
    class Meta:
        model = SzukanaKsiazka
        fields = {
            'tytul',
        }
class FormularzFiltrowania(forms.ModelForm):
    class Meta:
        model = SzukanaKategoria
        fields = {
            'nazwa',
        }
