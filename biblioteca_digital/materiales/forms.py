from django import forms
from .models import (
    Libro,
    Ejemplar,
    Mapas,
    Multimedia,
    Notebook,
    Programa,
    Proyector,
    Varios,
    TipoVarios,
    EjemplarVarios,
)

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = [
            'titulo',
            'autor',
            'editorial',
            'descripcion',
            'siglas_autor_titulo',
            'clasificacion_cdu',
            'palabras_clave',
        ]

class EjemplarForm(forms.ModelForm):
    class Meta:
        model = Ejemplar
        fields = [
            'libro',
            'numero_ejemplar',
            'sede',
            'disponibilidad',
            'observaciones',
        ]
            
class MapaForm(forms.ModelForm):
    class Meta:
        model = Mapas
        fields = ['sede']

    
class MultimediaForm(forms.ModelForm):
    class Meta:
        model = Multimedia
        fields = [
            'profesor',
            'url',
            'carrera',
            'materia',
            'titulo',
            # Si necesitas campos de Inventario como 'num_ejemplar', agrégalos aquí
        ]

class NotebookForm(forms.ModelForm):
    class Meta:
        model = Notebook
        fields = ['marca_not']

class ProgramaForm(forms.ModelForm):
    class Meta:
        model = Programa
        fields = ['profesor', 'url', 'carrera', 'materia']

class ProyectorForm(forms.ModelForm):
    class Meta:
        model = Proyector
        fields = ['marca_pro']  # 'sede' viene de Inventario

class VariosForm(forms.ModelForm):
    class Meta:
        model = Varios
        fields = ['sede']