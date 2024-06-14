from django import forms
from .models import Ksiazka, Recenzja, Uzytkownik, Kategoria

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
class FromularzRejestracji(forms.ModelForm):
    class Meta:
        model = Uzytkownik
        fields = '__all__'
        require_all_fields=True
class FormularzKategorii(forms.ModelForm):
    class Meta:
        model = Kategoria
        fields = '__all__'
        require_all_fields=True
