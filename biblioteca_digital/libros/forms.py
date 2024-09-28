from django import forms
from .models import Libro
from .models import Mapas
from .models import Multimedia
from .models import Notebook
from .models import Proyector
from .models import Varios


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
        fields = ['id_mapa', 'tipo', 'descripcion', 'num_ejemplar']  # Agrega los campos que necesites

class MultimediaForm(forms.ModelForm):
    class Meta:
        model = Multimedia
        fields = ['id_multi', 'materia','contenido', 'descripcion', 'num_ejemplar']  # Agrega los campos que necesites


class NotebookForm(forms.ModelForm):
    class Meta:
        model = Notebook
        fields = ['id_not', 'marca_not','modelo_not', 'descripcion', 'num_ejemplar']  # Agrega los campos que necesites

class ProyectorForm(forms.ModelForm):
    class Meta:
        model = Proyector
        fields = ['id_proyector', 'marca_pro','modelo_pro', 'descripcion', 'num_ejemplar']  # Agrega los campos que necesites

class VariosForm(forms.ModelForm):
    class Meta:
        model = Varios
        fields = ['id_varios', 'tipo', 'descripcion', 'num_ejemplar']  # Agrega los campos 

