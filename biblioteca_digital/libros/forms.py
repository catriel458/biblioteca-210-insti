from django import forms
from .models import Libro

from django import forms
from .models import Libro


class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = [
            'titulo', 'autor', 'editorial', 'edicion','codigo_materia','siglas_autor_titulo','num_inventario',
            'resumen', 'img',
            
        ]

