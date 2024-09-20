from django import forms
from .models import Libro

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['id_libro', 'titulo', 'autor','editorial','cdu','resumen','img']
