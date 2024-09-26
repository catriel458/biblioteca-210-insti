import json
from django.shortcuts import render
from collections import Counter
from .models import Libro  # Ensure this is at the top of your views.py
from .forms import LibroForm
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Inventario


#Metodos de biblioteca:

def alta_inventario(request):
    pass

def baja_inventario(request):
    pass

def modificacion_inventario(request):
    pass

def asignar_prestamo(request):
    pass

def cancelar_prestamo(request):
    pass

def modificar_prestamo(request):
    pass

# Metodo alumno y profesor

def solicitar_prestamo(request):
    pass

def lista_libros(request):
    libros = Libro.objects.all()  # Obtener todos los libros
    return render(request, 'libros/lista_libros.html', {'libros': libros})

def alta_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            # Guarda el libro, que incluye datos de Inventario
            libro = form.save(commit=False)  # No guardar aún
            libro.save()  # Ahora guarda
            return render(request, 'libros/alta_libro.html', {'form': form, 'success': 'Libro registrado exitosamente.'})
        else:
            return render(request, 'libros/alta_libro.html', {'form': form, 'error': 'Por favor complete todos los campos obligatorios.'})
    else:
        form = LibroForm()
    
    return render(request, 'libros/alta_libro.html', {'form': form})

def baja_libro(request):
    if request.method == 'POST':
        libro_id = request.POST.get('libro_id')
        motivo_baja = request.POST.get('motivo_baja')
        imagen_rota = request.FILES.get('imagen_rota')

        # Lógica para actualizar el estado del libro
        libro = Inventario.objects.get(id_inventario=libro_id)
        libro.estado = 'No disponible'
        libro.motivo_baja = motivo_baja
        if imagen_rota:
            libro.imagen_rota = imagen_rota
        libro.save()

        return redirect('lista_libros')  # Redirigir a la lista de libros
    
def lista_libros(request):
    libros = Libro.objects.exclude(estado='No disponible')  # Filtra los libros
    return render(request, 'libros/lista_libros.html', {'libros': libros})

def editar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id_libro=libro_id)

    if request.method == 'POST':
        form = LibroForm(request.POST, instance=libro)
        if form.is_valid():
            form.save()
            return redirect('lista_libros')  # Redirige a la lista de libros
    else:
        form = LibroForm(instance=libro)

    return render(request, 'libros/editar_libro.html', {'form': form, 'libro': libro})