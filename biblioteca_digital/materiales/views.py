import json
import csv
import io
from collections import Counter

import requests
from django.core.files.base import ContentFile
from urllib.parse import urlparse
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .forms import (
    LibroForm, MapaForm, MultimediaForm, NotebookForm, ProyectorForm, VariosForm
)
from .models import (
    Libro, Mapas, Multimedia, Notebook, Proyector, Varios, Ejemplar
)

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

        # Verificar si el archivo tiene al menos una fila de datos (después del encabezado)
        rows = list(reader)
        if not rows:  # Si no hay filas de datos
            return HttpResponse("El archivo CSV está vacío o solo contiene encabezados.")

        # Restablecer el puntero del archivo para procesarlo nuevamente
        io_string.seek(0)
        reader = csv.DictReader(io_string)

        for row in reader:
            print(f"Fila procesada: {row}")  # Imprimir la fila para depuración

            try:
                estado = "Disponible"
                motivo_baja = row.get('motivo_baja')
                descripcion = row.get('descripcion')

                # Manejar num_ejemplar
                num_ejemplar = int(row.get('num_ejemplar') or 1)

                tipo_material = row.get('tipo_material')  # Campo que determina el tipo de material

                # --- BLOQUE RELACIONADO CON INVENTARIO ELIMINADO ---
                # El siguiente bloque ha sido comentado porque dependía del modelo Inventario, ya eliminado.
                # Refactorizar la lógica de alta de libros según el nuevo modelo actual.
                # ---
                # Procesar según el tipo de material
                # if tipo_material == 'Libro':
                #     num_inventario = int(row.get('num_inventario') or 1)  # Valor por defecto si está vacío
                #     libro = Libro(
                #         estado=estado,
                #         motivo_baja=motivo_baja,
                #         descripcion=descripcion,
                #         num_ejemplar=num_ejemplar,
                #         imagen_rota=row.get('imagen_rota'),
                #         titulo=row.get('titulo'),
                #         autor=row.get('autor'),
                #         editorial=row.get('editorial'),
                #         edicion=int(row.get('edicion') or 1999),  # Valor por defecto
                #         codigo_materia=row.get('codigo_materia', '1'),
                #         siglas_autor_titulo=row.get('siglas_autor_titulo', 'ABC'),
                #         num_inventario=num_inventario,
                #         resumen=row.get('resumen'),
                #         img=row.get('img')
                #     )
                #   Nota: Este bloque fue comentado porque usaba campos de Inventario y otros que ya no existen en el modelo Libro. Refactorizar según la nueva estructura de modelos.
                #     libro.save()
                #     print(f"Libro guardado: {libro}")  # Imprimir confirmación
                # --- FIN BLOQUE INVENTARIO ---

                if tipo_material == 'Mapa':
                    mapa = Mapas(
                        estado=estado,
                        motivo_baja=motivo_baja,
                        descripcion=descripcion,
                        num_ejemplar=num_ejemplar,
                        tipo=row.get('tipo')  # Campo específico para Mapas
                    )
                    mapa.save()
                    print(f"Mapa guardado: {mapa}")  # Imprimir confirmación

                elif tipo_material == 'Multimedia':
                    multimedia = Multimedia(
                        estado=estado,
                        motivo_baja=motivo_baja,
                        descripcion=descripcion,
                        num_ejemplar=num_ejemplar,
                        materia=row.get('materia'),
                        contenido=row.get('contenido')
                    )
                    multimedia.save()
                    print(f"Multimedia guardada: {multimedia}")  # Imprimir confirmación

                elif tipo_material == 'Notebook':
                    notebook = Notebook(
                        estado=estado,
                        motivo_baja=motivo_baja,
                        descripcion=descripcion,
                        num_ejemplar=num_ejemplar,
                        marca_not=row.get('marca_not'),
                        modelo_not=row.get('modelo_not')
                    )
                    notebook.save()
                    print(f"Notebook guardada: {notebook}")  # Imprimir confirmación

                elif tipo_material == 'Programa':
                    programa = Programa(
                        estado=estado,
                        motivo_baja=motivo_baja,
                        descripcion=descripcion,
                        num_ejemplar=num_ejemplar,
                        marca_pro=row.get('marca_pro'),
                        modelo_pro=row.get('modelo_pro')
                    )
                    programa.save()
                    print(f"Programa guardado: {programa}")  # Imprimir confirmación
            
                elif tipo_material == 'Proyector':
                    proyector = Proyector(
                        estado=estado,
                        motivo_baja=motivo_baja,
                        descripcion=descripcion,
                        num_ejemplar=num_ejemplar,
                        marca_pro=row.get('marca_pro'),
                        modelo_pro=row.get('modelo_pro')
                    )
                    proyector.save()
                    print(f"Proyector guardado: {proyector}")  # Imprimir confirmación

                elif tipo_material == 'Varios':
                    varios = Varios(
                        estado=estado,
                        motivo_baja=motivo_baja,
                        descripcion=descripcion,
                        num_ejemplar=num_ejemplar,
                        tipo=row.get('tipo')
                    )
                    varios.save()
                    print(f"Varios guardado: {varios}")  # Imprimir confirmación

            except (ValueError, TypeError) as e:
                print(f"Error al procesar la fila {row}: {e}")

        return redirect('success_url')  # Cambia 'success_url' por el nombre que has definido en urls.py

    return render(request, 'materiales/utilidades/upload_csv.html')  # Cambia la plantilla según corresponda

def success_view(request):
    return render(request, 'materiales/utilidades/success.html')

# =========================
# BÚSQUEDAS
# =========================

# =========================
# BÚSQUEDAS
# =========================

# Busqueda libros

def buscar_libros(request):
    query = request.GET.get('q', '')
    libros = Libro.objects.filter(
        Q(titulo__icontains=query) | 
        Q(autor__icontains=query) | 
        Q(resumen__icontains=query),
        estado='Disponible'
    ).values('id_libro', 'titulo', 'autor', 'editorial', 'edicion', 'codigo_materia', 'resumen', 'img')

    return JsonResponse(list(libros), safe=False)

# Buscar de mapas
def buscar_mapas(request):
    query = request.GET.get('q', '')
    mapas = Mapas.objects.filter(
        Q(tipo__icontains=query) | 
        Q(descripcion__icontains=query),
        estado='Disponible'
    ).values('id_mapa', 'tipo', 'descripcion', 'num_ejemplar')

    return JsonResponse(list(mapas), safe=False)

# Buscador de multimedia
def buscar_multimedia(request):
    query = request.GET.get('q', '')
    multimedia = Multimedia.objects.filter(
        Q(materia__icontains=query) | 
        Q(contenido__icontains=query),
        estado='Disponible'
    ).values('id_multi', 'materia', 'contenido', 'num_ejemplar')

    return JsonResponse(list(multimedia), safe=False) 

# Buscador de notebooks
# Código viejo
'''def buscar_notebooks(request):
    query = request.GET.get('q', '')
    notebooks = Notebook.objects.filter(
        Q(marca__icontains=query) | 
        Q(modelo__icontains=query)
    ).values('id_netbook', 'marca', 'modelo', 'num_ejemplar')

    return JsonResponse(list(notebooks), safe=False)'''

# Código modificado (funcionando)
def buscar_notebooks(request):
    query = request.GET.get('q', '')
    if query:
        notebooks = Notebook.objects.filter(marca_not__icontains=query, estado='Disponible') | Notebook.objects.filter(modelo_not__icontains=query, estado='Disponible')
    else:
        notebooks = Notebook.objects.filter(estado='Disponible')

    data = list(notebooks.values('id_not', 'marca_not', 'modelo_not', 'num_ejemplar'))
    return JsonResponse(data, safe=False)

# Buscador de proyectores

def buscar_proyectores(request):
    query = request.GET.get('q', '')
    proyectores = Proyector.objects.filter(
        Q(marca_pro__icontains=query) | Q(modelo_pro__icontains=query),
        estado='Disponible'  # Asegúrate de que esto coincide con el campo en tu modelo
    ).values('id_proyector', 'marca_pro', 'modelo_pro', 'num_ejemplar')

    return JsonResponse(list(proyectores), safe=False)

# Buscador de varios
def buscar_varios(request):
    query = request.GET.get('q', '')
    varios = Varios.objects.filter(
        Q(tipo__icontains=query),
        estado='Disponible' 
    ).values('id_varios', 'tipo', 'num_ejemplar')

    return JsonResponse(list(varios), safe=False)

# =========================
# UTILIDADES Y OTRAS FUNCIONES
# =========================

# Borrar libros

def borrar_libros(request):
    if request.method == 'POST':
        Libro.objects.all().delete()
        messages.success(request, "Todos los libros han sido borrados.")
        return redirect('lista_libros')  # Cambia esto a la URL donde quieras redirigir después de borrar

    return render(request, 'materiales/registros/borrar_libros.html')  # Crea un template para confirmar la acción

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

# =========================
# VISTAS PRINCIPALES
# =========================

# Pantalla principal

# Vista para la pantalla principal:


# Libros

# =========================
# LIBROS
# =========================

# Vista para listar libros (todos los disponibles):

def lista_libros(request):
    # Filtra los libros disponibles
    libros = Libro.objects.all()
    return render(request, 'materiales/libros/lista_libros.html', {'libros': libros})

# =========================
# ALTAS
# =========================

# =========================
# ALTAS
# =========================


def alta_libro(request):
    if request.method == 'POST':
        print("POST recibido:", request.POST)
        libro_form = LibroForm(request.POST, request.FILES)
        if libro_form.is_valid():
            libro = libro_form.save(commit=False)
            # --- NUEVO: Manejo de imagen por URL ---
            url_imagen = request.POST.get('url_upload_input', '').strip()
            if url_imagen and not request.FILES.get('imagen') and not getattr(libro, 'imagen', None):
                try:
                    response = requests.get(url_imagen)
                    if response.status_code == 200:
                        nombre_archivo = os.path.basename(urlparse(url_imagen).path)
                        if not nombre_archivo:
                            nombre_archivo = 'imagen_libro.jpg'
                        libro.imagen.save(nombre_archivo, ContentFile(response.content), save=False)
                except Exception as e:
                    print("Error descargando imagen:", e)
            libro.save()
            numeros = request.POST.getlist('numero_ejemplar[]')
            sedes = request.POST.getlist('sede[]')
            disponibilidades = request.POST.getlist('disponibilidad[]')
            observaciones = request.POST.getlist('observaciones[]')
            # Validación de longitud de arrays
            total_ejemplares = min(len(numeros), len(sedes), len(disponibilidades), len(observaciones))
            for i in range(total_ejemplares):
                Ejemplar.objects.create(
                    libro=libro,
                    numero_ejemplar=numeros[i],
                    sede=sedes[i],
                    disponibilidad=disponibilidades[i],
                    observaciones=observaciones[i]
                )
            return redirect('lista_libros')
        else:
            # Opcional: mensajes de error para el usuario
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        libro_form = LibroForm()
    return render(request, 'materiales/formularios_altas/alta_libro.html', {'form': libro_form})
# =========================
# BAJAS
# =========================

# =========================
# BAJAS
# =========================

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


# =========================
# EDICIÓN
# =========================

# Vista para editar un libro:

def editar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)

    if request.method == 'POST':
        form = LibroForm(request.POST, instance=libro)
        if form.is_valid():
            form.save()
            return redirect('lista_libros')
    else:
        form = LibroForm(instance=libro)

    return render(request, 'components/modificacion_materiales/modificacion_editar_material.html', {'form': form, 'libro': libro})


# Mapas

# Vista para listar mapas disponibles:


def mapas_view(request):
    mapas = Mapas.objects.filter(estado='Disponible')
    return render(request, 'materiales/mapas/lista_mapas.html', {'mapas': mapas})

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

    return render(request, 'materiales/formularios_altas/alta_mapa.html', context)

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

    return render(request, 'materiales/formularios_editar/editar_mapa.html', {'form': form, 'mapa': mapa})

# Vista para mostrar elementos multimedia (por implementar):

# Multimedia


def multimedia_view(request):
    multimedia = Multimedia.objects.filter(estado='Disponible')
    return render(request, 'materiales/multimedia/lista_multimedia.html', {'multimedia': multimedia})

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

    return render(request, 'materiales/formularios_altas/alta_multimedia.html', context)

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

    return render(request, 'materiales/formularios_editar/editar_multimedia.html', {'form': form, 'mapa': multimedia})

# Notebook


def notebook_view(request):
    notebook = Notebook.objects.filter(estado='Disponible')
    return render(request, 'materiales/notebook/lista_notebooks.html', {'notebook': notebook})

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

    return render(request, 'materiales/formularios_altas/alta_notebook.html', context)

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

    return render(request, 'materiales/formularios_editar/editar_notebook.html', {'form': form, 'notebook': notebook})

# Proyector


def proyector_view(request):
    proyector = Proyector.objects.filter(estado='Disponible')
    return render(request, 'materiales/proyector/lista_proyectores.html', {'proyector': proyector})

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

    return render(request, 'materiales/formularios_altas/alta_proyector.html', context)

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

    return render(request, 'materiales/formularios_editar/editar_proyector.html', {'form': form, 'proyector': proyector})


# Varios

def alta_programa(request):
    """
    Vista temporal para el alta de programas. Devuelve una respuesta simple para evitar errores de importación.
    """
    return HttpResponse("Vista de alta de programa en construcción.")


def varios_view(request):
    varios = Varios.objects.filter(estado='Disponible')
    return render(request, 'materiales/varios/lista_varios.html', {'varios': varios})

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

    return render(request, 'materiales/formularios_altas/alta_varios.html', context)

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

    return render(request, 'materiales/formularios_editar/editar_varios.html', {'form': form, 'varios': varios})


# Vista para registro de bajas 

def registro_bajas(request):
    # Filtrar solo los libros que están 'No disponible'
    libros_no_disponibles = Libro.objects.filter(estado='No disponible')

    # Contexto a pasar al template
    context = {
        'libros_no_disponibles': libros_no_disponibles,
    }

    return render(request, 'materiales/registros/registro_bajas.html', context)

# Estas funciones se han movido al proyecto principal (biblioteca_digital/views.py)
'''def home(request):
    return render(request, 'home.html')

def alta_material(request):
    return render(request, 'materiales/alta_material.html')'''

def get_material_template(request, tipo):
    """
    Vista para servir los templates específicos de cada tipo de material
    """
    template_name = f'materiales/formularios_altas/alta_{tipo}.html'
    try:
        return render(request, template_name)
    except TemplateDoesNotExist:
        return HttpResponse('', status=404)



@csrf_exempt  # Si tienes CSRF en AJAX, puedes cambiarlo por @csrf_protect
@require_POST
def guardar_material_ajax(request):
    """
    Vista AJAX para guardar materiales de cualquier tipo y devolver JSON con el id creado.
    """
    tipo = request.POST.get('tipo_material')
    if not tipo:
        return JsonResponse({'success': False, 'error': 'Tipo de material no especificado'})

    # --- Libro ---
    if tipo == 'libro':
        form = LibroForm(request.POST, request.FILES)
        if form.is_valid():
            libro = form.save()
            # Crear ejemplares si se reciben arrays
            numeros = request.POST.getlist('numero_ejemplar[]')
            sedes = request.POST.getlist('sede[]')
            disponibilidades = request.POST.getlist('disponibilidad[]')
            observaciones = request.POST.getlist('observaciones[]')
            total_ejemplares = min(len(numeros), len(sedes), len(disponibilidades), len(observaciones))
            for i in range(total_ejemplares):
                Ejemplar.objects.create(
                    libro=libro,
                    numero_ejemplar=numeros[i],
                    sede=sedes[i],
                    disponibilidad=disponibilidades[i],
                    observaciones=observaciones[i]
                )
            return JsonResponse({'success': True, 'id_material': libro.id})
        else:
            return JsonResponse({'success': False, 'error': form.errors.as_json()})

    # --- Mapa ---
    elif tipo == 'mapa':
        form = MapaForm(request.POST, request.FILES)
        if form.is_valid():
            mapa = form.save()
            return JsonResponse({'success': True, 'id_material': mapa.id})
        else:
            return JsonResponse({'success': False, 'error': form.errors.as_json()})

    # --- Multimedia ---
    elif tipo == 'multimedia':
        form = MultimediaForm(request.POST, request.FILES)
        if form.is_valid():
            multimedia = form.save()
            return JsonResponse({'success': True, 'id_material': multimedia.id_multi})
        else:
            return JsonResponse({'success': False, 'error': form.errors.as_json()})

    # --- Notebook ---
    elif tipo == 'notebook':
        form = NotebookForm(request.POST, request.FILES)
        if form.is_valid():
            notebook = form.save()
            return JsonResponse({'success': True, 'id_material': notebook.id_not})
        else:
            return JsonResponse({'success': False, 'error': form.errors.as_json()})

    # --- Proyector ---
    elif tipo == 'proyector':
        form = ProyectorForm(request.POST, request.FILES)
        if form.is_valid():
            proyector = form.save()
            return JsonResponse({'success': True, 'id_material': proyector.id_proyector})
        else:
            return JsonResponse({'success': False, 'error': form.errors.as_json()})

    # --- Varios ---
    elif tipo == 'varios':
        form = VariosForm(request.POST, request.FILES)
        if form.is_valid():
            varios = form.save()
            return JsonResponse({'success': True, 'id_material': varios.id})
        else:
            return JsonResponse({'success': False, 'error': form.errors.as_json()})

    return JsonResponse({'success': False, 'error': 'Tipo de material no soportado'})

def modificacion_materiales(request):
    return render(request, 'materiales/modificacion_materiales.html')

def prestamos(request):
    return render(request, 'materiales/prestamos.html')
