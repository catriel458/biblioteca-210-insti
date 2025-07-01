import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from collections import Counter
from .models import Libro, Inventario, Mapas, Multimedia, Notebook, Proyector, Varios, Prestamo
from .forms import LibroForm, MapaForm, MultimediaForm, NotebookForm, ProyectorForm, VariosForm
import csv
import io  # Agregar esta línea
from django.contrib import messages #Para mensajes
from django.http import JsonResponse
from django.db.models import Q  # Añade esta línea
from django.contrib import messages
from django.utils import timezone
import datetime

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegistroForm, LoginForm, CambiarPasswordForm
from .models import Usuario


import csv
import io
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Libro, Mapas, Multimedia, Notebook, Proyector, Varios

import csv
import io
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Libro, Mapas, Multimedia, Notebook, Proyector, Varios

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

                # Procesar según el tipo de material
                if tipo_material == 'Libro':
                    num_inventario = int(row.get('num_inventario') or 1)  # Valor por defecto si está vacío
                    libro = Libro(
                        estado=estado,
                        motivo_baja=motivo_baja,
                        descripcion=descripcion,
                        num_ejemplar=num_ejemplar,
                        imagen_rota=row.get('imagen_rota'),
                        titulo=row.get('titulo'),
                        autor=row.get('autor'),
                        editorial=row.get('editorial'),
                        clasificacion_cdu=row.get('clasificacion_cdu'),
                        siglas_autor_titulo=row.get('siglas_autor_titulo'),
                        num_inventario=num_inventario,
                        resumen=row.get('resumen'),
                        etiqueta_palabra_clave=row.get('etiqueta_palabra_clave'),
                        sede=row.get('sede'),
                        disponibilidad=row.get('disponibilidad'),
                        observaciones=row.get('observaciones'),
                        img=row.get('img')
                    )
                    libro.save()
                    print(f"Libro guardado: {libro}")  # Imprimir confirmación

                elif tipo_material == 'Mapa':
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

    return render(request, 'libros/upload_csv.html')  # Cambia la plantilla según corresponda


def success_view(request):
    return render(request, 'libros/success.html')

# Busqueda libros

def buscar_libros(request):
    query = request.GET.get('q', '')
    libros = Libro.objects.filter(
        Q(titulo__icontains=query) | 
        Q(autor__icontains=query) | 
        Q(resumen__icontains=query),
        estado='Disponible'
    ).values('num_inventario','titulo', 'autor', 'editorial', 'clasificacion_cdu', 'siglas_autor_titulo', 'descripcion', 'etiqueta_palabra_clave', 'sede', 'disponibilidad', 'observaciones', 'img')

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

def home(request):
    """
    Vista principal de la aplicación - Pantalla de inicio
    """
    return render(request, 'home.html')  # ← CORRECTO

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


# Pantalla principal

# Vista para la pantalla principal:


def pantalla_principal(request):
    return render(request, 'libros/pantalla_principal.html')

# Libros

# Vista para listar libros (todos los disponibles):


def lista_libros(request):
    # Filtra los libros disponibles
    libros = Libro.objects.filter(estado='Disponible')
    return render(request, 'materiales/libros/lista_libros.html', {'libros': libros})

# Vista para dar de alta un libro:





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

    return render(request, 'materiales/formularios_editar/editar_libro.html', {'form': form, 'libro': libro})


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


# Vista para registro de bajas 

def registro_bajas(request):
    # Filtrar solo los libros que están 'No disponible'
    libros_no_disponibles = Libro.objects.filter(estado='No disponible')

    # Contexto a pasar al template
    context = {
        'libros_no_disponibles': libros_no_disponibles,
    }

    return render(request, 'libros/registro_bajas.html', context)

# Reactivar libros en el historial de bajas
def reactivar_libro(request, libro_id):
    if request.method == 'POST':
        libro = get_object_or_404(Libro, id_libro=libro_id)
        libro.estado = 'Disponible'
        libro.motivo_baja = ''  # Opcional: limpiar el motivo de baja
        libro.save()
        messages.success(request, f'El libro "{libro.titulo}" ha sido reactivado exitosamente.')
        return redirect('registro_de_bajas')
    return redirect('registro_de_bajas')

# PRESTAMOS

def solicitar_prestamo(request, libro_id):
    libro = get_object_or_404(Libro, id_libro=libro_id)
    
    # Verificar si el libro está disponible
    if libro.estado != 'Disponible':
        messages.error(request, "Este libro no está disponible para préstamo.")
        return redirect('lista_libros')
    
    # Crear el préstamo
    if request.method == 'POST':
        nombre_usuario = request.POST.get('nombre_usuario', '')
        email_usuario = request.POST.get('email_usuario', '')
        tipo_usuario = request.POST.get('tipo_usuario', 'alumno')
        tipo_prestamo = request.POST.get('tipo_prestamo', 'domicilio')
        
        # NO calcular fecha límite aquí - se calculará cuando se apruebe
        prestamo = Prestamo(
            nombre_usuario=nombre_usuario,
            email_usuario=email_usuario,
            libro=libro,
            tipo_prestamo=tipo_prestamo,
            tipo_usuario=tipo_usuario,
            estado='solicitado',
            fecha_limite_reserva=None  # Se establecerá cuando se apruebe la solicitud
        )
        prestamo.save()
        
        # Cambiar estado del libro a reservado
        libro.estado = 'Reservado'
        libro.save()
        
        messages.success(request, f"Has solicitado el préstamo del libro '{libro.titulo}'. La bibliotecaria revisará tu solicitud y tendrás 3 días hábiles para retirarlo una vez aprobada.")
        return redirect('prestamos_solicitados')
    
    return render(request, 'libros/solicitar_prestamo.html', {'libro': libro})


def aprobar_solicitud_prestamo(request, prestamo_id):
    """
    Aprueba la solicitud de préstamo y empieza el cronómetro de reserva
    """
    prestamo = get_object_or_404(Prestamo, id_prestamo=prestamo_id)
    
    if prestamo.estado != 'solicitado':
        messages.error(request, f"La solicitud no puede ser aprobada porque su estado actual es {prestamo.get_estado_display()}.")
        return redirect('gestionar_prestamos')
    
    # AQUÍ es donde empieza el cronómetro de reserva (3 días hábiles)
    fecha_limite = calcular_dias_habiles(timezone.now(), 3)
    
    prestamo.estado = 'aprobado_reserva'  # Nuevo estado: aprobado para reserva
    prestamo.fecha_limite_reserva = fecha_limite
    prestamo.fecha_aprobacion = timezone.now()
    prestamo.save()
    
    # Calcular días hábiles restantes para mostrar en el mensaje
    dias_habiles = 3
    messages.success(request, f"✅ RESERVA APROBADA: '{prestamo.libro.titulo}' para {prestamo.nombre_usuario}. Tiempo límite: {fecha_limite.strftime('%d/%m/%Y a las %H:%M')} ({dias_habiles} días hábiles).")
    
    return redirect('gestionar_prestamos')

def cancelar_reserva_usuario(request, prestamo_id):
    """
    Permite al usuario cancelar su propia solicitud o reserva
    """
    prestamo = get_object_or_404(Prestamo, id_prestamo=prestamo_id)
    
    # Solo permitir cancelar si está en estado solicitado o aprobado_reserva
    if prestamo.estado not in ['solicitado', 'aprobado_reserva']:
        messages.error(request, f"No puedes cancelar este préstamo porque su estado actual es {prestamo.get_estado_display()}.")
        return redirect('gestionar_prestamos')
    
    if request.method == 'POST':
        motivo_cancelacion = request.POST.get('motivo_cancelacion', 'Cancelado por el usuario')
        
        # Cambiar estado a rechazado
        prestamo.estado = 'rechazado'
        prestamo.motivo_rechazo = f"CANCELADO POR USUARIO: {motivo_cancelacion}"
        prestamo.save()
        
        # Devolver el libro al estado disponible
        libro = prestamo.libro
        libro.estado = 'Disponible'
        libro.save()
        
        messages.success(request, f"Has cancelado exitosamente la reserva del libro '{prestamo.libro.titulo}'.")
        
        return redirect('gestionar_prestamos')
    
    return render(request, 'libros/cancelar_reserva_usuario.html', {'prestamo': prestamo})

def prestamos_solicitados(request):
    # Verificar préstamos vencidos antes de mostrar
    verificar_prestamos_vencidos()
    
    # Obtener todos los préstamos (simplificado sin filtrado por usuario)
    prestamos = Prestamo.objects.all().order_by('-fecha_solicitud')
    
    # Verificar si hay alertas de tiempo (menos de 1 día hábil restante)
    alertas = []
    ahora = timezone.now()
    
    for prestamo in prestamos:
        if prestamo.estado == 'solicitado' and prestamo.fecha_limite_reserva:
            tiempo_restante = prestamo.fecha_limite_reserva - ahora
            # Si queda menos de 24 horas
            if tiempo_restante.total_seconds() > 0 and tiempo_restante.total_seconds() < 86400:  # 24 horas en segundos
                alertas.append(f"¡ATENCIÓN! El préstamo del libro '{prestamo.libro.titulo}' vence pronto.")
    
    return render(request, 'libros/prestamos_solicitados.html', {
        'prestamos': prestamos,
        'alertas': alertas
    })

def aprobar_prestamo(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id_prestamo=prestamo_id)
    
    if prestamo.estado != 'solicitado':
        messages.error(request, f"El préstamo no puede ser aprobado porque su estado actual es {prestamo.get_estado_display()}.")
        return redirect('gestionar_prestamos')
    
    prestamo.estado = 'aprobado'
    prestamo.fecha_aprobacion = timezone.now()
    
    # Calcular fecha de devolución (15 días)
    prestamo.fecha_devolucion_programada = timezone.now() + datetime.timedelta(days=15)
    
    # Limpiar fecha límite de reserva ya que fue retirado
    prestamo.fecha_limite_reserva = None
    
    prestamo.save()
    
    messages.success(request, f"El préstamo del libro '{prestamo.libro.titulo}' ha sido aprobado. Fecha de devolución: {prestamo.fecha_devolucion_programada.strftime('%d/%m/%Y')}.")
    
    return redirect('gestionar_prestamos')

# MODIFICAR ESTA FUNCIÓN EXISTENTE
def rechazar_prestamo(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id_prestamo=prestamo_id)
    
    if prestamo.estado not in ['solicitado', 'vencido']:
        messages.error(request, f"El préstamo no puede ser rechazado porque su estado actual es {prestamo.get_estado_display()}.")
        return redirect('gestionar_prestamos')
    
    if request.method == 'POST':
        motivo_rechazo = request.POST.get('motivo_rechazo', '')
        prestamo.estado = 'rechazado'
        prestamo.motivo_rechazo = motivo_rechazo
        prestamo.save()
        
        # Devolver el libro al estado disponible
        libro = prestamo.libro
        libro.estado = 'Disponible'
        libro.save()
        
        messages.success(request, f"El préstamo del libro '{prestamo.libro.titulo}' ha sido rechazado.")
        
        return redirect('gestionar_prestamos')
    
    return render(request, 'libros/rechazar_prestamo.html', {'prestamo': prestamo})

def finalizar_prestamo(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id_prestamo=prestamo_id)
    
    if prestamo.estado != 'aprobado':
        messages.error(request, f"El préstamo no puede ser finalizado porque su estado actual es {prestamo.get_estado_display()}.")
        return redirect('gestionar_prestamos')
    
    prestamo.estado = 'finalizado'
    prestamo.fecha_devolucion_real = timezone.now()
    prestamo.save()
    
    # Devolver el libro al estado disponible
    libro = prestamo.libro
    libro.estado = 'Disponible'
    libro.save()
    
    messages.success(request, f"El préstamo del libro '{prestamo.libro.titulo}' ha sido finalizado.")
    
    return redirect('gestionar_prestamos')


def gestionar_prestamos(request):
    # Verificar préstamos vencidos antes de mostrar
    verificar_prestamos_vencidos()
    
    # Obtener préstamos según filtro (sin verificación de permisos)
    filtro = request.GET.get('filtro', 'todos')
    
    if filtro == 'solicitados':
        prestamos = Prestamo.objects.filter(estado='solicitado').order_by('-fecha_solicitud')
    elif filtro == 'activos':
        prestamos = Prestamo.objects.filter(estado='aprobado').order_by('-fecha_aprobacion')
    elif filtro == 'finalizados':
        prestamos = Prestamo.objects.filter(estado__in=['finalizado', 'rechazado', 'vencido']).order_by('-fecha_solicitud')
    else:
        prestamos = Prestamo.objects.all().order_by('-fecha_solicitud')
    
    return render(request, 'libros/gestionar_prestamos.html', {
        'prestamos': prestamos,
        'filtro': filtro
    })


# FUNCIÓN PARA CALCULAR DÍAS HÁBILES (Lunes a Viernes)
def calcular_dias_habiles(fecha_inicio, dias_habiles):
    """
    Calcula una fecha que esté N días hábiles después de la fecha de inicio
    """
    dias_agregados = 0
    fecha_actual = fecha_inicio
    
    while dias_agregados < dias_habiles:
        fecha_actual += datetime.timedelta(days=1)
        # Si es día de semana (lunes=0, domingo=6), contar como día hábil
        if fecha_actual.weekday() < 5:  # 0-4 son lunes a viernes
            dias_agregados += 1
    
    return fecha_actual

# FUNCIÓN PARA VERIFICAR PRÉSTAMOS VENCIDOS
def verificar_prestamos_vencidos():
    """
    Verifica y actualiza préstamos que han vencido su tiempo de reserva
    """
    ahora = timezone.now()
    
    # Buscar préstamos aprobados para reserva que han vencido
    prestamos_vencidos = Prestamo.objects.filter(
        estado='aprobado_reserva',  # Cambio aquí: solo los aprobados para reserva
        fecha_limite_reserva__lt=ahora
    )
    
    for prestamo in prestamos_vencidos:
        # Cambiar estado del préstamo a vencido
        prestamo.estado = 'vencido'
        prestamo.save()
        
        # Devolver el libro al estado disponible
        libro = prestamo.libro
        libro.estado = 'Disponible'
        libro.save()

# AGREGAR ESTAS FUNCIONES NUEVAS

def confirmar_retiro_libro(request, prestamo_id):
    """
    Confirma que el alumno retiró el libro físicamente
    """
    prestamo = get_object_or_404(Prestamo, id_prestamo=prestamo_id)
    
    if prestamo.estado not in ['aprobado_reserva']:  # Cambio aquí
        messages.error(request, f"No se puede confirmar el retiro porque el estado actual es {prestamo.get_estado_display()}.")
        return redirect('gestionar_prestamos')
    
    # Verificar si aún está dentro del tiempo de reserva
    if prestamo.fecha_limite_reserva and timezone.now() > prestamo.fecha_limite_reserva:
        messages.error(request, "El tiempo de reserva ha vencido. No se puede confirmar el retiro.")
        return redirect('gestionar_prestamos')
    
    if request.method == 'POST':
        # Cambiar estado a aprobado (libro retirado y préstamo activo)
        prestamo.estado = 'aprobado'
        prestamo.fecha_retiro_real = timezone.now()  # Nueva fecha de retiro
        
        # Calcular fecha de devolución (15 días desde el retiro)
        prestamo.fecha_devolucion_programada = timezone.now() + datetime.timedelta(days=15)
        
        # Limpiar fecha límite de reserva ya que fue retirado
        prestamo.fecha_limite_reserva = None
        
        prestamo.save()
        
        messages.success(request, f"Se confirmó el retiro del libro '{prestamo.libro.titulo}'. Fecha de devolución: {prestamo.fecha_devolucion_programada.strftime('%d/%m/%Y')}.")
        
        return redirect('gestionar_prestamos')
    
    return render(request, 'libros/confirmar_retiro.html', {'prestamo': prestamo})

def marcar_no_retiro(request, prestamo_id):
    """
    Marca que el alumno no retiró el libro
    """
    prestamo = get_object_or_404(Prestamo, id_prestamo=prestamo_id)
    
    if prestamo.estado != 'solicitado':
        messages.error(request, f"No se puede marcar como no retirado porque el estado actual es {prestamo.get_estado_display()}.")
        return redirect('gestionar_prestamos')
    
    if request.method == 'POST':
        motivo = request.POST.get('motivo', 'No retirado por el usuario')
        
        # Cambiar estado a rechazado
        prestamo.estado = 'rechazado'
        prestamo.motivo_rechazo = motivo
        prestamo.save()
        
        # Devolver el libro al estado disponible
        libro = prestamo.libro
        libro.estado = 'Disponible'
        libro.save()
        
        messages.success(request, f"Se marcó como no retirado el libro '{prestamo.libro.titulo}'. El libro está nuevamente disponible.")
        
        return redirect('gestionar_prestamos')
    
    return render(request, 'libros/marcar_no_retiro.html', {'prestamo': prestamo})

# Agregar estos imports al inicio de tu archivo views.py
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegistroForm, LoginForm, CambiarPasswordForm
from .models import Usuario

# Funciones auxiliares para verificar permisos
#def es_bibliotecaria(user):
    #return user.is_authenticated and user.perfil == 'bibliotecaria'

# Agregar estas vistas al final de tu archivo views.py

# def login_view(request):
#     if request.user.is_authenticated:
#         return redirect('pantalla_principal')
    
#     if request.method == 'POST':
#         form = LoginForm(request, data=request.POST)
#         if form.is_valid():
#             dni = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username=dni, password=password)
#             if user is not None:
#                 login(request, user)
#                 messages.success(request, f'Bienvenido/a {user.get_full_name()}')
#                 return redirect('pantalla_principal')
#     else:
#         form = LoginForm()
    
#     return render(request, 'libros/login.html', {'form': form})

def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Cuenta creada exitosamente. Ya puedes iniciar sesión.')
            return redirect('login')
    else:
        form = RegistroForm()
    
    return render(request, 'materiales/formularios_altas/alta_libro.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')

@login_required
def perfil_usuario(request):
    return render(request, 'libros/perfil_usuario.html', {'usuario': request.user})

@login_required
def cambiar_password(request):
    if request.method == 'POST':
        form = CambiarPasswordForm(request.user, request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data['password_nueva'])
            request.user.save()
            messages.success(request, 'Contraseña cambiada exitosamente. Inicia sesión nuevamente.')
            return redirect('login')
    else:
        form = CambiarPasswordForm(request.user)
    
    return render(request, 'libros/cambiar_password.html', {'form': form})

# Actualizar estas vistas existentes para agregar autenticación

@login_required  # Agregar este decorador
def pantalla_principal(request):
    return render(request, 'libros/pantalla_principal.html')

#@login_required  # Agregar este decorador
def lista_libros(request):
    libros = Libro.objects.filter(estado='Disponible')
    return render(request, 'materiales/libros/lista_libros.html', {'libros': libros})

def formulario_libro(request):
    """
    Vista para mostrar el formulario de alta de libro (solo GET)
    """
    form = LibroForm()
    return render(request, 'materiales/formularios_altas/formulario_libro.html', {'form': form})  

def alta_materiales(request):
    """
    Vista principal para mostrar la página de alta de materiales
    Desde aquí se selecciona el tipo de material y se carga el formulario específico
    """
    return render(request, 'materiales/formularios_altas/alta_materiales.html') # con materiales

def alta_libro(request):
    """
    Vista para procesar el envío del formulario de alta de libro
    CORREGIDA: NO guarda en base de datos, solo valida y redirige al modal
    """
    print(f"🔥🔥🔥 INICIO alta_libro")
    print(f"🔥 Método: {request.method}")
    print(f"🔥 URL: {request.path}")
    print(f"🔥 POST data keys: {list(request.POST.keys()) if request.method == 'POST' else 'No POST'}")
    
    if request.method == 'POST':
        print("🔥 POST recibido en alta_libro - procesando para modal")
        
        # Verificar si hay datos en POST
        if not request.POST:
            print("❌ POST está vacío!")
            return redirect('formulario_libro')
            
        form = LibroForm(request.POST, request.FILES)
        print(f"🔍 Formulario creado. Es válido? {form.is_valid()}")
        
        if form.is_valid():
            print("✅ Formulario válido - guardando en sesión")
            try:
                # NO guardar en base de datos, solo en sesión
                form_data = {
                    'titulo': form.cleaned_data.get('titulo', ''),
                    'autor': form.cleaned_data.get('autor', ''),
                    'editorial': form.cleaned_data.get('editorial', ''),
                    'descripcion': form.cleaned_data.get('descripcion', ''),
                    'siglas_autor_titulo': form.cleaned_data.get('siglas_autor_titulo', ''),
                    'clasificacion_cdu': form.cleaned_data.get('clasificacion_cdu', ''),
                    'etiqueta_palabra_clave': form.cleaned_data.get('etiqueta_palabra_clave', ''),
                    'num_inventario': form.cleaned_data.get('num_inventario', 1),
                    'sede': form.cleaned_data.get('sede', ''),
                    'disponibilidad': form.cleaned_data.get('disponibilidad', ''),
                    'observaciones': form.cleaned_data.get('observaciones', ''),
                    'resumen': form.cleaned_data.get('resumen', ''),
                    'num_ejemplar': form.cleaned_data.get('num_ejemplar', 1),
                }
                
                # Manejar imagen si existe
                img_field = form.cleaned_data.get('img')
                if img_field:
                    # Verificar si es un archivo o una URL/string
                    if hasattr(img_field, 'name'):
                        form_data['img_name'] = img_field.name
                    else:
                        form_data['img_name'] = str(img_field)
                    print(f"📷 Imagen procesada: {form_data['img_name']}")
                
                # Guardar en sesión
                request.session['libro_data'] = form_data
                print(f"📦 Datos guardados en sesión: {form_data}")
                
                # Redirigir al modal de confirmación
                print("🚀 Redirigiendo a confirmar_alta_libro")
                return redirect('confirmar_alta_libro')
                
            except Exception as e:
                print(f"❌ Error al procesar: {e}")
                import traceback
                traceback.print_exc()
                messages.error(request, f'Error al procesar el libro: {str(e)}')
                return render(request, 'materiales/formularios_altas/formulario_libro.html', {'form': form})
        else:
            print(f"❌ Formulario inválido: {form.errors}")
            messages.error(request, 'Por favor corrige los errores en el formulario.')
            return render(request, 'materiales/formularios_altas/formulario_libro.html', {'form': form})
    else:
        # Si es GET, redirigir al formulario
        print("🔄 GET recibido en alta_libro, redirigiendo a formulario")
        return redirect('formulario_libro')

def confirmar_alta_libro(request):
    """
    Vista para mostrar el modal de confirmación
    CORREGIDA: Verifica datos en sesión
    """
    print("🎯 Llegó a confirmar_alta_libro")  # Debug
    
    # Verificar que existan datos en la sesión
    if 'libro_data' not in request.session:
        print("❌ No hay datos en sesión")  # Debug
        messages.error(request, 'No hay datos para confirmar. Por favor, complete el formulario nuevamente.')
        return redirect('formulario_libro')
    
    # Obtener datos de la sesión
    form_data = request.session['libro_data']
    print(f"📋 Datos de sesión: {form_data}")  # Debug
    
    # Renderizar página con modal automático
    return render(request, 'materiales/formularios_altas/confirmacion_alta_material.html', {
        'form_data': form_data
    })


def guardar_libro_confirmado(request):
    """
    Vista para guardar definitivamente después de confirmar en el modal
    ESTA ES LA ÚNICA FUNCIÓN QUE GUARDA EN BASE DE DATOS
    """
    print("💾 Llegó a guardar_libro_confirmado")  # Debug
    
    if request.method == 'POST' and 'libro_data' in request.session:
        try:
            # Obtener datos de la sesión
            libro_data = request.session['libro_data']
            print(f"📦 Datos a guardar: {libro_data}")  # Debug
            
            # Crear el libro en base de datos
            libro = Libro(
                estado='Disponible',
                titulo=libro_data.get('titulo', ''),
                autor=libro_data.get('autor', ''),
                editorial=libro_data.get('editorial', ''),
                descripcion=libro_data.get('descripcion', ''),
                siglas_autor_titulo=libro_data.get('siglas_autor_titulo', ''),
                clasificacion_cdu=libro_data.get('clasificacion_cdu', ''),
                etiqueta_palabra_clave=libro_data.get('etiqueta_palabra_clave', ''),
                num_inventario=libro_data.get('num_inventario', 1),
                sede=libro_data.get('sede', ''),
                disponibilidad=libro_data.get('disponibilidad', ''),
                observaciones=libro_data.get('observaciones', ''),
                resumen=libro_data.get('resumen', ''),
                num_ejemplar=libro_data.get('num_ejemplar', 1),
                # img se manejará después si es necesario
            )
            
            # GUARDAR EN BASE DE DATOS
            libro.save()
            print(f"✅ Libro guardado en BD: {libro.id}")  # Debug
            
            # Limpiar sesión
            del request.session['libro_data']
            
            messages.success(request, f'✅ Libro "{libro.titulo}" registrado exitosamente.')
            return redirect('lista_libros')
            
        except Exception as e:
            print(f"❌ Error al guardar: {e}")  # Debug
            messages.error(request, f'❌ Error al guardar el libro: {str(e)}')
            return redirect('formulario_libro')
    else:
        print("❌ No hay datos o método incorrecto")  # Debug
        messages.error(request, 'No hay datos para guardar.')
        return redirect('formulario_libro')


def cancelar_alta_libro(request):
    """
    Vista para cancelar la alta y limpiar datos de sesión
    """
    print("🔴 Cancelando alta de libro")  # Debug
    
    if 'libro_data' in request.session:
        del request.session['libro_data']
        print("🗑️ Datos de sesión eliminados")  # Debug
    
    messages.info(request, 'Operación cancelada.')
    return redirect('formulario_libro')
# Agregar decoradores similares a todas las vistas de alta de material
#@user_passes_test(es_bibliotecaria)
def alta_mapa(request):
    # ... código existente ...
    pass

#@user_passes_test(es_bibliotecaria)
def alta_multimedia(request):
    # ... código existente ...
    pass

#@user_passes_test(es_bibliotecaria)
def alta_notebook(request):
    # ... código existente ...
    pass

#@user_passes_test(es_bibliotecaria)
def alta_proyector(request):
    # ... código existente ...
    pass

#@user_passes_test(es_bibliotecaria)
def alta_varios(request):
    # ... código existente ...
    pass

# Actualizar la vista de préstamos solicitados para mostrar solo los del usuario actual
@login_required
def prestamos_solicitados(request):
    # Verificar préstamos vencidos antes de mostrar
    verificar_prestamos_vencidos()
    
    # Filtrar préstamos según el tipo de usuario
    if request.user.es_bibliotecaria():
        # La bibliotecaria ve todos los préstamos
        prestamos = Prestamo.objects.all().order_by('-fecha_solicitud')
    else:
        # Los usuarios normales solo ven sus propios préstamos
        prestamos = Prestamo.objects.filter(
            Q(email_usuario=request.user.email) | Q(usuario=request.user)
        ).order_by('-fecha_solicitud')
    
    # Verificar si hay alertas de tiempo (menos de 1 día hábil restante)
    alertas = []
    ahora = timezone.now()
    
    for prestamo in prestamos:
        if prestamo.estado == 'solicitado' and prestamo.fecha_limite_reserva:
            tiempo_restante = prestamo.fecha_limite_reserva - ahora
            # Si queda menos de 24 horas
            if tiempo_restante.total_seconds() > 0 and tiempo_restante.total_seconds() < 86400:  # 24 horas en segundos
                alertas.append(f"¡ATENCIÓN! El préstamo del libro '{prestamo.libro.titulo}' vence pronto.")
    
    return render(request, 'libros/prestamos_solicitados.html', {
        'prestamos': prestamos,
        'alertas': alertas
    })

# Actualizar la vista de solicitar préstamo para usar el usuario logueado
@login_required
def solicitar_prestamo(request, libro_id):
    libro = get_object_or_404(Libro, id_libro=libro_id)
    
    # Verificar si el libro está disponible
    if libro.estado != 'Disponible':
        messages.error(request, "Este libro no está disponible para préstamo.")
        return redirect('lista_libros')
    
    # Crear el préstamo
    if request.method == 'POST':
        tipo_usuario = request.POST.get('tipo_usuario', 'alumno')
        tipo_prestamo = request.POST.get('tipo_prestamo', 'domicilio')
        
        prestamo = Prestamo(
            usuario=request.user,  # Asignar el usuario logueado
            nombre_usuario=request.user.get_full_name(),  # Llenar automáticamente
            email_usuario=request.user.email,  # Llenar automáticamente
            libro=libro,
            tipo_prestamo=tipo_prestamo,
            tipo_usuario=tipo_usuario,
            estado='solicitado',
            fecha_limite_reserva=None
        )
        prestamo.save()
        
        # Cambiar estado del libro a reservado
        libro.estado = 'Reservado'
        libro.save()
        
        messages.success(request, f"Has solicitado el préstamo del libro '{libro.titulo}'. La biblioteca revisará tu solicitud.")
        return redirect('prestamos_solicitados')
    
    return render(request, 'libros/solicitar_prestamo.html', {'libro': libro})

# Gestión de préstamos solo para bibliotecarias
#@user_passes_test(es_bibliotecaria)
def gestionar_prestamos(request):
    # ... mantener el código existente ...
    verificar_prestamos_vencidos()
    
    filtro = request.GET.get('filtro', 'todos')
    
    if filtro == 'solicitados':
        prestamos = Prestamo.objects.filter(estado='solicitado').order_by('-fecha_solicitud')
    elif filtro == 'activos':
        prestamos = Prestamo.objects.filter(estado='aprobado').order_by('-fecha_aprobacion')
    elif filtro == 'finalizados':
        prestamos = Prestamo.objects.filter(estado__in=['finalizado', 'rechazado', 'vencido']).order_by('-fecha_solicitud')
    else:
        prestamos = Prestamo.objects.all().order_by('-fecha_solicitud')
    
    return render(request, 'libros/gestionar_prestamos.html', {
        'prestamos': prestamos,
        'filtro': filtro
    })

# Agregar el decorador a todas las funciones de gestión de préstamos
#@user_passes_test(es_bibliotecaria)
def aprobar_prestamo(request, prestamo_id):
    # ... código existente ...
    pass

#@user_passes_test(es_bibliotecaria)
def rechazar_prestamo(request, prestamo_id):
    # ... código existente ...
    pass

#@user_passes_test(es_bibliotecaria)
def finalizar_prestamo(request, prestamo_id):
    # ... código existente ...
    pass