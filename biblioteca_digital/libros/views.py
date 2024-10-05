import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from collections import Counter
from .models import Libro, Inventario, Mapas, Multimedia, Notebook, Proyector, Varios
from .forms import LibroForm, MapaForm, MultimediaForm, NotebookForm, ProyectorForm, VariosForm
import csv
import io  # Agregar esta línea
from django.contrib import messages #Para mensajes

def cargar_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']

        # Verifica que el archivo sea un CSV
        if not csv_file.name.endswith('.csv'):
            return HttpResponse("El archivo no es un CSV.")

        # Procesar el archivo CSV
        decoded_file = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)

        for row in reader:
            try:
                num_ejemplar = int(row.get('num_ejemplar') or 0)  # Asignar 0 si está vacío
                edicion = int(row.get('edicion', 1999))  # Asignar valor por defecto
                num_inventario = int(row.get('num_inventario', 1))  # Asignar valor por defecto

                libro = Libro(
                    estado="Disponible",  # Establecer estado como "Disponible"
                    motivo_baja=row.get('motivo_baja'),
                    descripcion=row.get('descripcion'),
                    num_ejemplar=num_ejemplar,
                    imagen_rota=row.get('imagen_rota'),
                    titulo=row.get('titulo'),
                    autor=row.get('autor'),
                    editorial=row.get('editorial'),
                    edicion=edicion,
                    codigo_materia=row.get('codigo_materia', '1'),
                    siglas_autor_titulo=row.get('siglas_autor_titulo', 'ABC'),
                    num_inventario=num_inventario,
                    resumen=row.get('resumen'),
                    img=row.get('img')
                )
                libro.save()
            except (ValueError, TypeError) as e:
                # Manejo de errores, puedes loggear o notificar el problema
                print(f"Error al procesar la fila {row}: {e}")

        return redirect('success_url')  # Cambia 'success_url' por el nombre que has definido en urls.py

    return render(request, 'libros/upload_csv.html')

def success_view(request):
    return render(request, 'libros/success.html')

# Borrar libros

def borrar_libros(request):
    if request.method == 'POST':
        Libro.objects.all().delete()
        messages.success(request, "Todos los libros han sido borrados.")
        return redirect('lista_libros')  # Cambia esto a la URL donde quieras redirigir después de borrar

    return render(request, 'libros/borrar_libros.html')  # Crea un template para confirmar la acción

# Métodos de biblioteca:


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

# Método alumno y profesor:


def solicitar_prestamo(request):
    pass

# Pantalla principal

# Vista para la pantalla principal:


def pantalla_principal(request):
    return render(request, 'libros/pantalla_principal.html')

# Libros

# Vista para listar libros (todos los disponibles):


def lista_libros(request):
    # Filtra los libros disponibles
    libros = Libro.objects.filter(estado='Disponible')
    return render(request, 'libros/lista_libros.html', {'libros': libros})

# Vista para dar de alta un libro:


def alta_libro(request):
    form = LibroForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        libro = form.save(commit=False)
        libro.save()
        context = {'form': form, 'success': 'Libro registrado exitosamente.'}
    else:
        context = {'form': form, 'error': 'Por favor complete todos los campos obligatorios.'} if request.method == 'POST' else {
            'form': form}

    return render(request, 'libros/alta_libro.html', context)

# Vista para dar de baja un libro:


def baja_libro(request):
    if request.method == 'POST':
        libro_id = request.POST.get('libro_id')
        motivo_baja = request.POST.get('motivo_baja')
        imagen_rota = request.FILES.get('imagen_rota')

        # Lógica para actualizar el estado del libro
        # Cambiado para asegurar que sea Libro
        libro = get_object_or_404(Libro, id_libro=libro_id)
        libro.estado = 'No disponible'  # Asegúrate de cambiar el estado
        libro.motivo_baja = motivo_baja
        if imagen_rota:
            libro.imagen_rota = imagen_rota
        libro.save()

        # Redirigir a la lista de libros después de la baja
        return redirect('lista_libros')

    return redirect('lista_libros')


# Vista para editar un libro:


def editar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id_libro=libro_id)

    if request.method == 'POST':
        form = LibroForm(request.POST, instance=libro)
        if form.is_valid():
            form.save()
            return redirect('lista_libros')
    else:
        form = LibroForm(instance=libro)

    return render(request, 'libros/editar_libro.html', {'form': form, 'libro': libro})


# Mapas

# Vista para listar mapas disponibles:


def mapas_view(request):
    mapas = Mapas.objects.filter(estado='Disponible')
    return render(request, 'libros/mapas.html', {'mapas': mapas})

# Vista para dar de baja un mapa:


def baja_mapa(request):
    if request.method == 'POST':
        mapa_id = request.POST.get('mapa_id')
        motivo_baja = request.POST.get('motivo_baja')
        imagen_rota = request.FILES.get('imagen_rota')

        # Lógica para actualizar el estado del mapa
        mapa = get_object_or_404(Mapas, id_mapa=mapa_id)
        mapa.estado = 'No disponible'
        mapa.motivo_baja = motivo_baja
        if imagen_rota:
            mapa.imagen_rota = imagen_rota
        mapa.save()

        return redirect('mapas')

    return redirect('mapas')

# Vista para dar de alta un mapa:


def alta_mapa(request):
    form = MapaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        mapa = form.save(commit=False)
        mapa.save()
        context = {'form': form, 'success': 'Mapa registrado exitosamente.'}
    else:
        context = {'form': form, 'error': 'Por favor complete todos los campos obligatorios.'} if request.method == 'POST' else {
            'form': form}

    return render(request, 'libros/alta_mapa.html', context)

# Vista para editar un mapa:


def editar_mapa(request, mapa_id):
    mapa = get_object_or_404(Mapas, id_mapa=mapa_id)

    if request.method == 'POST':
        form = MapaForm(request.POST, instance=mapa)
        if form.is_valid():
            form.save()
            return redirect('mapas')
    else:
        form = MapaForm(instance=mapa)

    return render(request, 'libros/editar_mapa.html', {'form': form, 'mapa': mapa})

# Vista para mostrar elementos multimedia (por implementar):

# Multimedia


def multimedia_view(request):
    multimedia = Multimedia.objects.filter(estado='Disponible')
    return render(request, 'libros/multimedia.html', {'multimedia': multimedia})

# Vista para dar de baja un mapa:


def baja_multimedia(request):
    if request.method == 'POST':
        multi_id = request.POST.get('id_multi')
        motivo_baja = request.POST.get('motivo_baja')
        imagen_rota = request.FILES.get('imagen_rota')

        # Lógica para actualizar el estado del mapa
        multimedia = get_object_or_404(Multimedia, id_multi=multi_id)
        multimedia.estado = 'No disponible'
        multimedia.motivo_baja = motivo_baja
        if imagen_rota:
            multimedia.imagen_rota = imagen_rota
        multimedia.save()

        return redirect('multimedia')

    return redirect('multimedia')

# Vista para dar de alta un mapa:


def alta_multimedia(request):
    form = MultimediaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        multimedia = form.save(commit=False)
        multimedia.save()
        context = {'form': form,
                   'success': 'Multimedia registrado exitosamente.'}
    else:
        context = {'form': form, 'error': 'Por favor complete todos los campos obligatorios.'} if request.method == 'POST' else {
            'form': form}

    return render(request, 'libros/alta_multimedia.html', context)

# Vista para editar un mapa:


def editar_multimedia(request, multi_id):
    multimedia = get_object_or_404(Multimedia, id_multi=multi_id)

    if request.method == 'POST':
        form = MultimediaForm(request.POST, instance=multimedia)
        if form.is_valid():
            form.save()
            return redirect('multimedia')
    else:
        form = MultimediaForm(instance=multimedia)

    return render(request, 'libros/editar_multimedia.html', {'form': form, 'mapa': multimedia})

# Notebook


def notebook_view(request):
    notebook = Notebook.objects.filter(estado='Disponible')
    return render(request, 'libros/notebook.html', {'notebook': notebook})

# Vista para dar de baja un mapa:


def baja_notebook(request):
    if request.method == 'POST':
        not_id = request.POST.get('not_id')
        motivo_baja = request.POST.get('motivo_baja')
        imagen_rota = request.FILES.get('imagen_rota')

        # Lógica para actualizar el estado del mapa
        notebook = get_object_or_404(Notebook, id_not=not_id)
        notebook.estado = 'No disponible'
        notebook.motivo_baja = motivo_baja
        if imagen_rota:
            notebook.imagen_rota = imagen_rota
        notebook.save()

        return redirect('notebook')

    return redirect('notebook')

# Vista para dar de alta un mapa:


def alta_notebook(request):
    form = NotebookForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        notebook = form.save(commit=False)
        notebook.save()
        context = {'form': form,
                   'success': 'Notebook registrado exitosamente.'}
    else:
        context = {'form': form, 'error': 'Por favor complete todos los campos obligatorios.'} if request.method == 'POST' else {
            'form': form}

    return render(request, 'libros/alta_notebook.html', context)

# Vista para editar un mapa:


def editar_notebook(request, not_id):
    notebook = get_object_or_404(Notebook, id_not=not_id)

    if request.method == 'POST':
        form = NotebookForm(request.POST, instance=notebook)
        if form.is_valid():
            form.save()
            return redirect('notebook')
    else:
        form = NotebookForm(instance=notebook)

    return render(request, 'libros/editar_notebook.html', {'form': form, 'notebook': notebook})

# Proyector


def proyector_view(request):
    proyector = Proyector.objects.filter(estado='Disponible')
    return render(request, 'libros/proyector.html', {'proyector': proyector})

# Vista para dar de baja un mapa:


def baja_proyector(request):
    if request.method == 'POST':
        proyector_id = request.POST.get('proyector_id')
        motivo_baja = request.POST.get('motivo_baja')
        imagen_rota = request.FILES.get('imagen_rota')

        # Lógica para actualizar el estado del mapa
        proyector = get_object_or_404(Proyector, id_proyector=proyector_id)
        proyector.estado = 'No disponible'
        proyector.motivo_baja = motivo_baja
        if imagen_rota:
            proyector.imagen_rota = imagen_rota
        proyector.save()

        return redirect('proyector')

    return redirect('proyector')

# Vista para dar de alta un mapa:


def alta_proyector(request):
    form = ProyectorForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        proyector = form.save(commit=False)
        proyector.save()
        context = {'form': form,
                   'success': 'Proyector registrado exitosamente.'}
    else:
        context = {'form': form, 'error': 'Por favor complete todos los campos obligatorios.'} if request.method == 'POST' else {
            'form': form}

    return render(request, 'libros/alta_proyector.html', context)

# Vista para editar un mapa:


def editar_proyector(request, proyector_id):
    proyector = get_object_or_404(Proyector, id_proyector=proyector_id)

    if request.method == 'POST':
        form = ProyectorForm(request.POST, instance=proyector)
        if form.is_valid():
            form.save()
            return redirect('proyector')
    else:
        form = ProyectorForm(instance=proyector)

    return render(request, 'libros/editar_proyector.html', {'form': form, 'proyector': proyector})


# Varios


def varios_view(request):
    varios = Varios.objects.filter(estado='Disponible')
    return render(request, 'libros/varios.html', {'varios': varios})

# Vista para dar de baja un mapa:


def baja_varios(request):
    if request.method == 'POST':
        varios_id = request.POST.get('varios_id')
        motivo_baja = request.POST.get('motivo_baja')
        imagen_rota = request.FILES.get('imagen_rota')

        # Lógica para actualizar el estado del mapa
        varios = get_object_or_404(Varios, id_varios=varios_id)
        varios.estado = 'No disponible'
        varios.motivo_baja = motivo_baja
        if imagen_rota:
            varios.imagen_rota = imagen_rota
        varios.save()

        return redirect('varios')

    return redirect('varios')

# Vista para dar de alta un mapa:


def alta_varios(request):
    form = VariosForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        varios = form.save(commit=False)
        varios.save()
        context = {'form': form,
                   'success': 'Varios registrado exitosamente.'}
    else:
        context = {'form': form, 'error': 'Por favor complete todos los campos obligatorios.'} if request.method == 'POST' else {
            'form': form}

    return render(request, 'libros/alta_varios.html', context)

# Vista para editar un mapa:


def editar_varios(request, varios_id):
    varios = get_object_or_404(Varios, id_varios=varios_id)

    if request.method == 'POST':
        form = VariosForm(request.POST, instance=varios)
        if form.is_valid():
            form.save()
            return redirect('varios')
    else:
        form = VariosForm(instance=varios)

    return render(request, 'libros/editar_varios.html', {'form': form, 'varios': varios})
