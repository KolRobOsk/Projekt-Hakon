from django import forms
from .models import Ksiazka

class FormularzKsiazek(forms.ModelForm):
    class Meta:
        model = Ksiazka
        fields = '__all__'
        require_all_fields=True,
