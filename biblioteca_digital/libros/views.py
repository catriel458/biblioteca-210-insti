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

def pantalla_principal(request):
    return render(request, 'libros/pantalla_principal.html')

def mapas_view(request):
    # Filtrar mapas que están disponibles
    mapas = Mapas.objects.filter(estado='Disponible')
    return render(request, 'libros/mapas.html', {'mapas': mapas})

def multimedia_view(request):
    # Aquí deberías obtener la lista de multimedia desde la base de datos
    multimedia = []  # Reemplaza esto con tu lógica para obtener multimedia
    return render(request, 'multimedia.html', {'multimedia': multimedia})

def notebook_view(request):
    # Aquí deberías obtener la lista de notebooks desde la base de datos
    notebooks = []  # Reemplaza esto con tu lógica para obtener notebooks
    return render(request, 'notebook.html', {'notebooks': notebooks})

def proyector_view(request):
    # Aquí deberías obtener la lista de proyectores desde la base de datos
    proyectores = []  # Reemplaza esto con tu lógica para obtener proyectores
    return render(request, 'proyector.html', {'proyectores': proyectores})

def varios_view(request):
    # Aquí deberías obtener la lista de varios desde la base de datos
    varios = []  # Reemplaza esto con tu lógica para obtener varios
    return render(request, 'varios.html', {'varios': varios})

def baja_mapa(request):
    if request.method == 'POST':
        mapa_id = request.POST.get('mapa_id')
        motivo_baja = request.POST.get('motivo_baja')
        imagen_rota = request.FILES.get('imagen_rota')

        # Lógica para actualizar el estado del mapa
        mapa = Mapas.objects.get(id_mapa=mapa_id)
        mapa.estado = 'No disponible'
        mapa.motivo_baja = motivo_baja
        if imagen_rota:
            mapa.imagen_rota = imagen_rota
        mapa.save()

        return redirect('mapas')  # Redirigir a la lista de mapas

    return redirect('mapas')  # En caso de que no sea un POST, redirigir


from .models import Mapas
from .forms import MapaForm  # Asegúrate de que tienes este formulario creado

def alta_mapa(request):
    if request.method == 'POST':
        form = MapaForm(request.POST)
        if form.is_valid():
            # Guarda el mapa, que incluye datos de Inventario
            mapa = form.save(commit=False)  # No guardar aún
            mapa.save()  # Ahora guarda
            return render(request, 'libros/alta_mapa.html', {'form': form, 'success': 'Mapa registrado exitosamente.'})
        else:
            return render(request, 'libros/alta_mapa.html', {'form': form, 'error': 'Por favor complete todos los campos obligatorios.'})
    else:
        form = MapaForm()
    
    return render(request, 'libros/alta_mapa.html', {'form': form})


def editar_mapa(request, mapa_id):
    mapa = get_object_or_404(Mapas, id_mapa=mapa_id)
    
    if request.method == 'POST':
        form = MapaForm(request.POST, instance=mapa)
        if form.is_valid():
            form.save()
            return redirect('mapas')  # Redirige a la lista de mapas
    else:
        form = MapaForm(instance=mapa)
    
    return render(request, 'libros/editar_mapa.html', {'form': form, 'mapa': mapa})