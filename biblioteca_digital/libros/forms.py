from django import forms
from .models import Libro
from .models import Mapas


class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = [
            'titulo', 'autor', 'editorial', 'edicion','codigo_materia','siglas_autor_titulo','num_inventario',
            'resumen', 'img',
            
        ]

class MapaForm(forms.ModelForm):
    class Meta:
        model = Mapas
        fields = ['id_mapa', 'tipo', 'estado', 'descripcion', 'num_ejemplar']  # Agrega los campos que necesites

