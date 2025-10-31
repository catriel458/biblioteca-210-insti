import json
import csv
import io
import datetime
from collections import Counter

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Libro, Inventario, Mapas, Multimedia, Notebook, Proyector, Varios, Prestamo, Usuario, Programa
from .forms import LibroForm, MapaForm, MultimediaForm, MultimediaEditForm, NotebookForm, ProyectorForm, VariosForm, RegistroForm, LoginForm, CambiarPasswordForm, ProgramaForm

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
    ).values('titulo', 'autor', 'editorial', 'clasificacion_cdu', 'siglas_autor_titulo', 'descripcion', 'etiqueta_palabra_clave', 'sede', 'disponibilidad', 'observaciones', 'img')

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
        Q(modelo__icontains=query)
    ).values('id_netbook', 'modelo', 'num_ejemplar')

    return JsonResponse(list(notebooks), safe=False)'''

@login_required
def home(request):
    """
    Vista principal de la aplicación - Pantalla de inicio
    """
    return render(request, 'home.html')  # ← CORRECTO

def gestion(request):
    """
    Vista principal de gestión - Pantalla de gestión
    """
    return render(request, 'gestion/gestion.html')

# Función auxiliar para verificar si el usuario es bibliotecaria
def es_bibliotecaria(user):
    return user.is_authenticated and user.perfil == 'bibliotecaria'

# Decorador personalizado para requerir permisos de bibliotecaria
def bibliotecaria_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debe iniciar sesión para acceder a esta página.')
            return redirect('login')
        if not es_bibliotecaria(request.user):
            messages.error(request, 'No tiene permisos para acceder a esta página.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@bibliotecaria_required
def gestion_usuarios(request):
    """
    Vista principal de gestión de usuarios - Solo para bibliotecarias
    """
    usuarios = Usuario.objects.all().order_by('-fecha_registro')
    
    context = {
        'usuarios': usuarios,
        'total_usuarios': usuarios.count(),
        'usuarios_activos': usuarios.filter(is_active=True).count(),
        'usuarios_inactivos': usuarios.filter(is_active=False).count(),
        'bibliotecarias': usuarios.filter(perfil='bibliotecaria').count(),
        'estudiantes': usuarios.filter(perfil='estudiante').count(),
        'docentes': usuarios.filter(perfil='docente').count(),
    }
    
    return render(request, 'gestion/gestion_usuarios.html', context)

@bibliotecaria_required
def buscar_usuarios(request):
    """
    Vista AJAX para buscar usuarios por DNI, nombre, apellido o email
    """
    if request.method == 'GET':
        query = request.GET.get('q', '').strip()
        
        if query:
            usuarios = Usuario.objects.filter(
                Q(dni__icontains=query) |
                Q(nombre__icontains=query) |
                Q(apellido__icontains=query) |
                Q(email__icontains=query)
            ).order_by('-fecha_registro')
        else:
            usuarios = Usuario.objects.all().order_by('-fecha_registro')
        
        usuarios_data = []
        for usuario in usuarios:
            usuarios_data.append({
                'id': usuario.id,
                'dni': usuario.dni,
                'nombre': usuario.nombre,
                'apellido': usuario.apellido,
                'email': usuario.email,
                'perfil': usuario.get_perfil_display(),
                'perfil_value': usuario.perfil,
                'is_active': usuario.is_active,
                'fecha_registro': usuario.fecha_registro.strftime('%d/%m/%Y'),
            })
        
        return JsonResponse({'usuarios': usuarios_data})
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@bibliotecaria_required
def crear_usuario(request):
    """
    Vista para crear un nuevo usuario - Solo para bibliotecarias
     Usa el mismo formulario que registro.html para consistencia
    """
    if request.method == 'POST':
        try:
            # Crear una copia mutable de POST data
            post_data = request.POST.copy()
            
            # El perfil viene del formulario de gestión de usuarios
            perfil = post_data.get('perfil')
            
            # Agregar password2 para que coincida con el formulario de registro
            password1 = post_data.get('password')
            post_data['password1'] = password1
            post_data['password2'] = password1
            
            # Crear el formulario usando RegistroForm (mismo que registro.html)
            form = RegistroForm(post_data)
            
            if form.is_valid():
                # Crear el usuario usando el formulario
                user = form.save(commit=False)
                
                # Asignar el perfil seleccionado desde el modal
                if perfil in ['estudiante', 'docente', 'bibliotecaria']:
                    user.perfil = perfil
                else:
                    user.perfil = 'estudiante'  # Valor por defecto
                
                # Guardar el usuario
                user.save()
                
                return JsonResponse({
                    'success': True,
                    'message': f'Usuario {user.nombre} {user.apellido} creado exitosamente.',
                    'usuario': {
                        'id': user.id,
                        'dni': user.dni,
                        'nombre': user.nombre,
                        'apellido': user.apellido,
                        'email': user.email,
                        'perfil': user.get_perfil_display(),
                        'perfil_value': user.perfil,
                        'is_active': user.is_active,
                        'fecha_registro': user.fecha_registro.strftime('%d/%m/%Y'),
                    }
                })
                
            else:
                # Recopilar errores del formulario
                errors = []
                for field, field_errors in form.errors.items():
                    for error in field_errors:
                        if field == '__all__':
                            errors.append(str(error))
                        else:
                            field_name = form.fields[field].label or field
                            errors.append(f"{field_name}: {error}")
                
                return JsonResponse({
                    'success': False,
                    'error': 'Errores en el formulario: ' + '; '.join(errors)
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error al crear el usuario: {str(e)}'
            })
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@bibliotecaria_required
def editar_usuario(request, usuario_id):
    """
    Vista para editar un usuario existente - Solo para bibliotecarias
    """
    try:
        usuario = get_object_or_404(Usuario, id=usuario_id)
        
        if request.method == 'GET':
            # Devolver datos del usuario para el formulario
            return JsonResponse({
                'success': True,
                'usuario': {
                    'id': usuario.id,
                    'dni': usuario.dni,
                    'nombre': usuario.nombre,
                    'apellido': usuario.apellido,
                    'email': usuario.email,
                    'perfil': usuario.perfil,
                    'is_active': usuario.is_active,
                }
            })
        
        elif request.method == 'POST':
            # Actualizar datos del usuario
            nombre = request.POST.get('nombre', '').strip()
            apellido = request.POST.get('apellido', '').strip()
            email = request.POST.get('email', '').strip()
            perfil = request.POST.get('perfil', '').strip()
            # Corregir el manejo del checkbox is_active
            # Si el checkbox está marcado, se envía 'on', si no está marcado, no se envía nada
            is_active = request.POST.get('is_active') == 'on'
            nueva_password = request.POST.get('nueva_password', '').strip()
            
            # Validaciones básicas
            if not all([nombre, apellido, email, perfil]):
                return JsonResponse({
                    'success': False,
                    'error': 'Nombre, apellido, email y perfil son obligatorios.'
                })
            
            # Verificar si el email ya existe (excluyendo el usuario actual)
            if Usuario.objects.filter(email=email).exclude(id=usuario.id).exists():
                return JsonResponse({
                    'success': False,
                    'error': 'Ya existe otro usuario con este email.'
                })
            
            # Validar perfil
            if perfil not in ['estudiante', 'bibliotecaria', 'docente']:
                return JsonResponse({
                    'success': False,
                    'error': 'Perfil no válido.'
                })
            
            # Actualizar campos
            usuario.nombre = nombre
            usuario.apellido = apellido
            usuario.email = email
            usuario.perfil = perfil
            usuario.is_active = is_active
            
            # Cambiar contraseña si se proporcionó una nueva
            if nueva_password:
                usuario.set_password(nueva_password)
            
            usuario.save()
            
            messages.success(request, f'Usuario {usuario.nombre} {usuario.apellido} actualizado exitosamente.')
            
            return JsonResponse({
                'success': True,
                'message': 'Usuario actualizado exitosamente.',
                'usuario': {
                    'id': usuario.id,
                    'dni': usuario.dni,
                    'nombre': usuario.nombre,
                    'apellido': usuario.apellido,
                    'email': usuario.email,
                    'perfil': usuario.get_perfil_display(),
                    'perfil_value': usuario.perfil,
                    'is_active': usuario.is_active,
                    'fecha_registro': usuario.fecha_registro.strftime('%d/%m/%Y'),
                }
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al editar el usuario: {str(e)}'
        })
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@bibliotecaria_required
def eliminar_usuario(request, usuario_id):
    """
    Vista para eliminar un usuario - Solo para bibliotecarias
    """
    if request.method == 'POST':
        try:
            usuario = get_object_or_404(Usuario, id=usuario_id)
            
            # Verificar que no sea el último bibliotecario
            if usuario.perfil == 'bibliotecaria':
                bibliotecarias_count = Usuario.objects.filter(perfil='bibliotecaria', is_active=True).count()
                if bibliotecarias_count <= 1:
                    return JsonResponse({
                        'success': False,
                        'error': 'No se puede eliminar el último bibliotecario del sistema.'
                    })
            
            # Verificar que el usuario no se esté eliminando a sí mismo
            if usuario.id == request.user.id:
                return JsonResponse({
                    'success': False,
                    'error': 'No puede eliminar su propia cuenta.'
                })
            
            nombre_completo = f"{usuario.nombre} {usuario.apellido}"
            usuario.delete()
            
            messages.success(request, f'Usuario {nombre_completo} eliminado exitosamente.')
            
            return JsonResponse({
                'success': True,
                'message': 'Usuario eliminado exitosamente.'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error al eliminar el usuario: {str(e)}'
            })
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def gestion_prestamos(request):
    """
    Vista de gestión de préstamos
    """
    return render(request, 'gestion/gestion_prestamos.html')

def gestion_sanciones(request):
    """
    Vista de gestión de sanciones
    """
    return render(request, 'gestion/gestion_sanciones.html')

# Código modificado (funcionando)
def buscar_notebooks(request):
    query = request.GET.get('q', '')
    if query:
        notebooks = Notebook.objects.filter(modelo_not__icontains=query, estado='Disponible')
    else:
        notebooks = Notebook.objects.filter(estado='Disponible')

    data = list(notebooks.values('id_not', 'modelo_not', 'num_ejemplar'))
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
        # messages.success(request, "Todos los libros han sido borrados.")
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



# Vista para dar de alta un libro:





def baja_libro(request):
    if request.method == 'POST':
        libro_id = request.POST.get('libro_id')
        motivo_baja = request.POST.get('motivo_baja')
        imagen_rota = request.FILES.get('imagen_rota')

        # Obtener el libro
        libro = get_object_or_404(Libro, id_libro=libro_id)
        
        # Cambiar estado
        libro.estado = 'No disponible'
        libro.motivo_baja = motivo_baja
        
        # IMPORTANTE: Guardar imagen en el campo imagen_rota del modelo Inventario
        if imagen_rota:
            libro.imagen_rota = imagen_rota
        
        libro.save()

        # messages.success(request, f'Libro "{libro.titulo}" dado de baja exitosamente.')
        return redirect('modificacion_materiales')

    return redirect('modificacion_materiales')


# Vista para editar un libro:


# views.py - Función editar_libro corregida

def editar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id_libro=libro_id)
    
    if request.method == 'POST':
        print(f"🔥 POST recibido para editar libro ID: {libro_id}")
        print(f"🔥 Datos POST: {dict(request.POST)}")
        
        # Crear una copia mutable de POST para modificar
        post_data = request.POST.copy()
        
        # ARREGLAR: Manejar URL de imagen ANTES de crear el formulario
        url_input = post_data.get('url_input', '').strip()
        if url_input and not request.FILES.get('img'):
            print(f"🔗 Procesando URL de imagen: {url_input}")
            # Si hay URL pero no archivo, guardar la URL directamente en el libro
            libro.img = url_input
            # Remover el campo img del formulario para que no sea requerido
            post_data['img'] = url_input
        
        # ARREGLAR: Verificar campos requeridos vacíos
        if not post_data.get('sede'):
            print("⚠️ Sede vacía, usando valor actual del libro")
            post_data['sede'] = libro.sede or 'CENTRAL'  # Valor por defecto
            
        if not post_data.get('disponibilidad'):
            print("⚠️ Disponibilidad vacía, usando valor actual del libro")
            post_data['disponibilidad'] = libro.disponibilidad or 'DOMICILIO'  # Valor por defecto
        
        print(f"🔧 Datos POST corregidos: {dict(post_data)}")
        
        # Crear formulario con datos corregidos
        form = LibroForm(post_data, request.FILES, instance=libro)
        
        if form.is_valid():
            print("✅ Formulario válido - guardando...")
            
            try:
                # Guardar el formulario
                libro_actualizado = form.save()
                
                # Si había URL de imagen, asegurar que se guarde
                if url_input and not request.FILES.get('img'):
                    libro_actualizado.img = url_input
                    libro_actualizado.save()
                
                print(f"✅ Libro actualizado: {libro_actualizado.titulo}")
                print(f"📋 Imagen final: {libro_actualizado.img}")
                
                # messages.success(request, f'✅ Libro "{libro_actualizado.titulo}" actualizado exitosamente.')
                return redirect('modificacion_materiales')
                
            except Exception as e:
                print(f"❌ Error al guardar: {e}")
                import traceback
                traceback.print_exc()
                messages.error(request, f'❌ Error al actualizar el libro: {str(e)}')
        else:
            print(f"❌ Formulario TODAVÍA inválido!")
            print(f"❌ Errores: {form.errors}")
            
            # Mostrar errores específicos
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error en {field}: {error}')
                    print(f"❌ Error en {field}: {error}")
    else:
        form = LibroForm(instance=libro)
    
    return render(request, 'materiales/formularios_editar/editar_libro.html', {
        'form': form, 
        'libro': libro
    })


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

        # Obtener el mapa
        mapa = get_object_or_404(Mapas, id_mapa=mapa_id)
        
        # Cambiar estado
        mapa.estado = 'No disponible'
        mapa.motivo_baja = motivo_baja
        
        # Guardar imagen en el campo imagen_rota del modelo
        if imagen_rota:
            mapa.imagen_rota = imagen_rota
        
        mapa.save()

        # messages.success(request, f'Mapa "{mapa.tipo}" dado de baja exitosamente.')
        return redirect('modificacion_materiales')

    return redirect('modificacion_materiales')

# Vista para dar de alta un mapa:


def formulario_mapa(request):
    """Vista para mostrar el formulario de alta de mapa (solo GET)"""
    form = MapaForm()
    return render(request, 'materiales/formularios_altas/alta_mapa.html', {'form': form})

def formulario_multimedia(request):
    """Vista para mostrar el formulario de alta de multimedia (solo GET)"""
    form = MultimediaForm()
    return render(request, 'materiales/formularios_altas/alta_multimedia.html', {'form': form})

def formulario_notebook(request):
    """Vista para mostrar el formulario de alta de notebook (solo GET)"""
    form = NotebookForm()
    return render(request, 'materiales/formularios_altas/alta_notebook.html', {'form': form})

def formulario_proyector(request):
    """Vista para mostrar el formulario de alta de proyector (solo GET)"""
    form = ProyectorForm()
    return render(request, 'materiales/formularios_altas/alta_proyector.html', {'form': form})

def formulario_varios(request):
    """Vista para mostrar el formulario de alta de varios (solo GET)"""
    form = VariosForm()
    return render(request, 'materiales/formularios_altas/alta_varios.html', {'form': form})

# Vista para editar un mapa:


def editar_mapa(request, mapa_id):
    mapa = get_object_or_404(Mapas, id_mapa=mapa_id)

    if request.method == 'POST':
        form = MapaForm(request.POST, instance=mapa)
        if form.is_valid():
            form.save()
            return redirect('modificacion_materiales')
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

        # Lógica para actualizar el estado del multimedia
        multimedia = get_object_or_404(Multimedia, id_multi=multi_id)
        multimedia.estado = 'No disponible'
        multimedia.motivo_baja = motivo_baja
        if imagen_rota:
            multimedia.imagen_rota = imagen_rota
        multimedia.save()

        # messages.success(request, f'Multimedia "{multimedia.titulo_contenido}" dado de baja correctamente.')
        return redirect('modificacion_materiales')

    return redirect('modificacion_materiales')

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
        form = MultimediaEditForm(request.POST, instance=multimedia)
        if form.is_valid():
            form.save()
            return redirect('modificacion_materiales')
    else:
        form = MultimediaEditForm(instance=multimedia)

    return render(request, 'materiales/formularios_editar/editar_multimedia.html', {'form': form, 'multimedia': multimedia})

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

        # Lógica para actualizar el estado del notebook
        notebook = get_object_or_404(Notebook, id_not=not_id)
        notebook.estado = 'No disponible'
        notebook.motivo_baja = motivo_baja
        if imagen_rota:
            notebook.imagen_rota = imagen_rota
        notebook.save()

        return redirect('modificacion_materiales')

    return redirect('modificacion_materiales')

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
        print(f"🔥 POST recibido para editar notebook ID: {not_id}")
        print(f"🔥 Datos POST: {dict(request.POST)}")
        
        # Crear una copia mutable de POST para modificar
        post_data = request.POST.copy()
        
        # ARREGLAR: Verificar campos requeridos vacíos
        if not post_data.get('sede'):
            print("⚠️ Sede vacía, usando valor actual del notebook")
            post_data['sede'] = notebook.sede or 'La Plata'  # Valor por defecto
            
        if not post_data.get('num_registro'):
            print("⚠️ Num_registro vacío, usando valor actual del notebook")
            post_data['num_registro'] = notebook.num_registro or '1'  # Valor por defecto
            
        if not post_data.get('modelo_not'):
            print("⚠️ Modelo_not vacío, usando valor actual del notebook")
            post_data['modelo_not'] = notebook.modelo_not or 'Sin modelo'  # Valor por defecto
            
        if not post_data.get('num_ejemplar'):
            print("⚠️ Num_ejemplar vacío, usando valor actual del notebook")
            post_data['num_ejemplar'] = notebook.num_ejemplar or 1  # Valor por defecto
        
        print(f"🔧 Datos POST corregidos: {dict(post_data)}")
        
        # Imprimir datos del notebook antes de la modificación
        print(f"🔥 Notebook ANTES - sede: {notebook.sede}, num_registro: {notebook.num_registro}, modelo_not: {notebook.modelo_not}, num_ejemplar: {notebook.num_ejemplar}")
        
        # Crear formulario con datos corregidos
        form = NotebookForm(post_data, instance=notebook)
        
        if form.is_valid():
            print("✅ Formulario válido - guardando...")
            
            try:
                # Guardar el formulario
                notebook_actualizado = form.save()
                
                print(f"✅ Notebook actualizado: {notebook_actualizado}")
                print(f"📋 Datos finales - sede: {notebook_actualizado.sede}, num_registro: {notebook_actualizado.num_registro}, modelo_not: {notebook_actualizado.modelo_not}, num_ejemplar: {notebook_actualizado.num_ejemplar}")
                
                # messages.success(request, f'✅ Notebook actualizado exitosamente.')
                return redirect('modificacion_materiales')
                
            except Exception as e:
                print(f"❌ Error al guardar: {e}")
                import traceback
                traceback.print_exc()
                messages.error(request, f'❌ Error al actualizar el notebook: {str(e)}')
        else:
            print(f"❌ Formulario TODAVÍA inválido!")
            print(f"❌ Errores: {form.errors}")
            
            # Mostrar errores específicos
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error en {field}: {error}')
                    print(f"❌ Error en {field}: {error}")
    else:
        form = NotebookForm(instance=notebook)
    
    return render(request, 'materiales/formularios_editar/editar_notebook.html', {
        'form': form, 
        'notebook': notebook
    })

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

        # Lógica para actualizar el estado del proyector
        proyector = get_object_or_404(Proyector, id_proyector=proyector_id)
        proyector.estado = 'No disponible'
        proyector.motivo_baja = motivo_baja
        if imagen_rota:
            proyector.imagen_rota = imagen_rota
        proyector.save()

        return redirect('modificacion_materiales')

    return redirect('modificacion_materiales')

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
            return redirect('modificacion_materiales')
    else:
        form = ProyectorForm(instance=proyector)

    return render(request, 'materiales/formularios_editar/editar_proyector.html', {'form': form, 'proyector': proyector})


# Varios


def varios_view(request):
    varios = Varios.objects.filter(estado='Disponible')
    return render(request, 'materiales/varios/lista_varios.html', {'varios': varios})

# Vista para dar de baja un mapa:


def baja_varios(request):
    if request.method == 'POST':
        varios_id = request.POST.get('varios_id')
        motivo_baja = request.POST.get('motivo_baja')
        imagen_rota = request.FILES.get('imagen_rota')

        # Lógica para actualizar el estado de varios
        varios = get_object_or_404(Varios, id_varios=varios_id)
        varios.estado = 'No disponible'
        varios.motivo_baja = motivo_baja
        if imagen_rota:
            varios.imagen_rota = imagen_rota
        varios.save()

        return redirect('modificacion_materiales')

    return redirect('modificacion_materiales')

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
        try:
            # Debug: Imprimir datos POST recibidos
            print(f"DEBUG - POST data recibido: {dict(request.POST)}")
            
            # Crear una copia mutable de POST data
            post_data = request.POST.copy()
            
            # Asignar valores por defecto para campos requeridos si están vacíos
            if not post_data.get('tipo'):
                post_data['tipo'] = varios.tipo or 'Material Varios'
                print(f"DEBUG - Asignando tipo por defecto: {post_data['tipo']}")
            
            if not post_data.get('cantidad'):
                post_data['cantidad'] = varios.cantidad or 1
                print(f"DEBUG - Asignando cantidad por defecto: {post_data['cantidad']}")
                
            if not post_data.get('cantidad_disponible'):
                post_data['cantidad_disponible'] = varios.cantidad_disponible or 1
                print(f"DEBUG - Asignando cantidad_disponible por defecto: {post_data['cantidad_disponible']}")
            
            if not post_data.get('sede'):
                post_data['sede'] = varios.sede or 'La Plata'
                print(f"DEBUG - Asignando sede por defecto: {post_data['sede']}")
            
            # Debug: Imprimir datos antes de crear el formulario
            print(f"DEBUG - Datos procesados para el formulario: {dict(post_data)}")
            
            # Crear formulario con datos procesados
            form = VariosForm(post_data, instance=varios)
            
            # Debug: Verificar validez del formulario
            print(f"DEBUG - Formulario válido: {form.is_valid()}")
            if not form.is_valid():
                print(f"DEBUG - Errores del formulario: {form.errors}")
            
            if form.is_valid():
                # Debug: Imprimir datos antes de guardar
                print(f"DEBUG - Datos del varios antes de guardar:")
                print(f"  - ID: {varios.id_varios}")
                print(f"  - Tipo: {varios.tipo}")
                print(f"  - Cantidad: {varios.cantidad}")
                print(f"  - Cantidad Disponible: {varios.cantidad_disponible}")
                print(f"  - Sede: {varios.sede}")
                
                # Guardar el formulario
                varios_actualizado = form.save()
                
                # Debug: Imprimir datos después de guardar
                print(f"DEBUG - Datos del varios después de guardar:")
                print(f"  - ID: {varios_actualizado.id_varios}")
                print(f"  - Tipo: {varios_actualizado.tipo}")
                print(f"  - Cantidad: {varios_actualizado.cantidad}")
                print(f"  - Cantidad Disponible: {varios_actualizado.cantidad_disponible}")
                print(f"  - Sede: {varios_actualizado.sede}")
                
                # Verificar que los cambios se guardaron
                varios_verificacion = Varios.objects.get(id_varios=varios_id)
                print(f"DEBUG - Verificación desde BD:")
                print(f"  - Tipo: {varios_verificacion.tipo}")
                print(f"  - Cantidad: {varios_verificacion.cantidad}")
                print(f"  - Cantidad Disponible: {varios_verificacion.cantidad_disponible}")
                print(f"  - Sede: {varios_verificacion.sede}")
                
                messages.success(request, 'Varios editado exitosamente.')
                return redirect('modificacion_materiales')
            else:
                print(f"DEBUG - Formulario inválido. Errores: {form.errors}")
                messages.error(request, f'Error al editar el varios: {form.errors}')
                
        except Exception as e:
            print(f"DEBUG - Error en editar_varios: {str(e)}")
            import traceback
            traceback.print_exc()
            messages.error(request, f'Error inesperado al editar el varios: {str(e)}')
    else:
        form = VariosForm(instance=varios)
    
    context = {
        'form': form,
        'varios': varios,
        'title': 'Editar Varios'
    }
    
    return render(request, 'materiales/formularios_editar/editar_varios.html', context)


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
        # messages.success(request, f'El libro "{libro.titulo}" ha sido reactivado exitosamente.')
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
        tipo_usuario = request.POST.get('tipo_usuario', 'estudiante')
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
        
        # messages.success(request, f"Has solicitado el préstamo del libro '{libro.titulo}'. La bibliotecaria revisará tu solicitud y tendrás 3 días hábiles para retirarlo una vez aprobada.")
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
    # messages.success(request, f"✅ RESERVA APROBADA: '{prestamo.libro.titulo}' para {prestamo.nombre_usuario}. Tiempo límite: {fecha_limite.strftime('%d/%m/%Y a las %H:%M')} ({dias_habiles} días hábiles).")
    
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
        
        # messages.success(request, f"Has cancelado exitosamente la reserva del libro '{prestamo.libro.titulo}'.")
        
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
    
    # messages.success(request, f"El préstamo del libro '{prestamo.libro.titulo}' ha sido aprobado. Fecha de devolución: {prestamo.fecha_devolucion_programada.strftime('%d/%m/%Y')}.")
    
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
        
        # messages.success(request, f"El préstamo del libro '{prestamo.libro.titulo}' ha sido rechazado.")
        
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
    
    # messages.success(request, f"El préstamo del libro '{prestamo.libro.titulo}' ha sido finalizado.")
    
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
        
        # messages.success(request, f"Se confirmó el retiro del libro '{prestamo.libro.titulo}'. Fecha de devolución: {prestamo.fecha_devolucion_programada.strftime('%d/%m/%Y')}.")
        
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
        
        # messages.success(request, f"Se marcó como no retirado el libro '{prestamo.libro.titulo}'. El libro está nuevamente disponible.")
        
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

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            dni = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=dni, password=password)
            if user is not None:
                login(request, user)
                # messages.success(request, f'Bienvenido/a {user.get_full_name()}')
                return redirect('home')
        else:
            messages.error(request, 'DNI o contraseña incorrectos.')
    else:
        form = LoginForm()
    
    return render(request, 'login/login.html', {'form': form})

def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            # messages.success(request, 'Cuenta creada exitosamente. Ya puedes iniciar sesión.')
            return redirect('login')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = RegistroForm()
    
    return render(request, 'login/registro.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    # messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')

@login_required
def perfil_usuario(request):
    # Clear any existing messages to prevent unwanted alerts on the profile page
    storage = messages.get_messages(request)
    for message in storage:
        pass  # This consumes and clears the messages
    
    return render(request, 'login/perfil_usuario.html', {'usuario': request.user})

@login_required
def cambiar_password(request):
    if request.method == 'POST':
        form = CambiarPasswordForm(request.user, request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data['password_nueva'])
            request.user.save()
            # Mantener la sesión activa después del cambio de contraseña
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Contraseña cambiada exitosamente.')
            # En lugar de redireccionar, renderizar la misma página con el mensaje de éxito
            return render(request, 'login/cambiar_password.html', {'form': form, 'password_changed': True})
    else:
        form = CambiarPasswordForm(request.user)
    
    return render(request, 'login/cambiar_password.html', {'form': form})

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

def formulario_mapa(request):
    """
    Vista para mostrar el formulario de alta de mapa (solo GET)
    """
    form = MapaForm()
    return render(request, 'materiales/formularios_altas/alta_mapa.html', {'form': form})

def formulario_multimedia(request):
    """
    Vista para mostrar el formulario de alta de multimedia (solo GET)
    """
    form = MultimediaForm()
    return render(request, 'materiales/formularios_altas/alta_multimedia.html', {'form': form})

def formulario_notebook(request):
    """
    Vista para mostrar el formulario de alta de notebook (solo GET)
    """
    form = NotebookForm()
    return render(request, 'materiales/formularios_altas/alta_notebook.html', {'form': form})

def formulario_proyector(request):
    """
    Vista para mostrar el formulario de alta de proyector (solo GET)
    """
    form = ProyectorForm()
    return render(request, 'materiales/formularios_altas/alta_proyector.html', {'form': form})

def formulario_varios(request):
    """
    Vista para mostrar el formulario de alta de varios (solo GET)
    """
    form = VariosForm()
    return render(request, 'materiales/formularios_altas/alta_varios.html', {'form': form})

def alta_materiales(request):
    """
    Vista principal para mostrar la página de alta de materiales
    Desde aquí se selecciona el tipo de material y se carga el formulario específico
    """
    return render(request, 'materiales/formularios_altas/alta_materiales.html') # con materiales

def alta_libro(request):
    """
    Vista para procesar el envío del formulario de alta de libro
    Actualizada para manejar múltiples ejemplares sin usar LibroForm
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
        
        # Validar campos requeridos manualmente
        errores = []
        
        # Campos básicos requeridos
        campos_requeridos = ['titulo', 'autor', 'editorial', 'siglas_autor_titulo', 'clasificacion_cdu']
        for campo in campos_requeridos:
            if not request.POST.get(campo, '').strip():
                errores.append(f'El campo {campo} es requerido.')
        
        # Obtener cantidad de ejemplares
        cant_ejemplares = int(request.POST.get('cant_ejemplares', 1))
        print(f"📚 Cantidad de ejemplares: {cant_ejemplares}")
        
        # Validar campos dinámicos de ejemplares
        ejemplares = []
        for i in range(1, cant_ejemplares + 1):
            sede = request.POST.get(f'sede_{i}', '').strip()
            disponibilidad = request.POST.get(f'disponibilidad_{i}', '').strip()
            observaciones = request.POST.get(f'observaciones_{i}', '').strip()
            
            if not sede:
                errores.append(f'La sede del ejemplar {i} es requerida.')
            if not disponibilidad:
                errores.append(f'La disponibilidad del ejemplar {i} es requerida.')
            
            ejemplar_data = {
                'sede': sede,
                'disponibilidad': disponibilidad,
                'observaciones': observaciones
            }
            ejemplares.append(ejemplar_data)
        
        print(f"📋 Datos de ejemplares: {ejemplares}")
        
        # Si hay errores, mostrarlos
        if errores:
            print(f"❌ Errores de validación: {errores}")
            for error in errores:
                messages.error(request, error)
            # Crear un formulario vacío para mostrar la página
            form = LibroForm()
            return render(request, 'materiales/formularios_altas/formulario_libro.html', {'form': form})
        
        print("✅ Validación exitosa - guardando en sesión")
        try:
            # Obtener la URL de imagen
            img_url = request.POST.get('img', '').strip()
            print(f"📷 URL de imagen recibida: '{img_url}'")
            
            # NO guardar en base de datos, solo en sesión
            form_data = {
                'titulo': request.POST.get('titulo', '').strip(),
                'autor': request.POST.get('autor', '').strip(),
                'editorial': request.POST.get('editorial', '').strip(),
                'descripcion': request.POST.get('descripcion', '').strip(),
                'siglas_autor_titulo': request.POST.get('siglas_autor_titulo', '').strip(),
                'clasificacion_cdu': request.POST.get('clasificacion_cdu', '').strip(),
                'etiqueta_palabra_clave': request.POST.get('etiqueta_palabra_clave', '').strip(),
                'num_ejemplar': cant_ejemplares,
                'ejemplares': ejemplares,  # Lista de ejemplares con sus datos
                'img': img_url  # Guardar la URL directamente
            }
            
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
            form = LibroForm()
            return render(request, 'materiales/formularios_altas/formulario_libro.html', {'form': form})
    else:
        # Si es GET, redirigir al formulario
        print("🔄 GET recibido en alta_libro, redirigiendo a formulario")
        return redirect('formulario_libro')
    
    
def confirmar_alta_libro(request):
    """
    Vista para mostrar el modal de confirmación
    Actualizada para manejar múltiples ejemplares
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
    return render(request, 'materiales/formularios_altas/confirmaciones_alta/confirmacion_alta_material.html', {
        'form_data': form_data,
        'ejemplares': form_data.get('ejemplares', [])
    })


def guardar_libro_confirmado(request):
    """
    Vista para guardar definitivamente después de confirmar en el modal
    Actualizada para manejar múltiples ejemplares y datos editados
    """
    print("💾 Llegó a guardar_libro_confirmado")  # Debug
    
    if request.method == 'POST':
        try:
            # Verificar si hay datos editados en el POST
            if any(key in request.POST for key in ['titulo', 'autor', 'editorial', 'ejemplares_data']):
                print("📝 Procesando datos editados desde el frontend")  # Debug
                
                # Obtener datos editados del POST
                titulo = request.POST.get('titulo', '')
                autor = request.POST.get('autor', '')
                editorial = request.POST.get('editorial', '')
                descripcion = request.POST.get('descripcion', '')
                siglas_autor_titulo = request.POST.get('siglas_autor_titulo', '')
                clasificacion_cdu = request.POST.get('clasificacion_cdu', '')
                etiqueta_palabra_clave = request.POST.get('etiqueta_palabra_clave', '')
                
                # Obtener datos de ejemplares editados
                ejemplares_json = request.POST.get('ejemplares_data', '[]')
                ejemplares = json.loads(ejemplares_json)
                
                # Obtener imagen de la sesión si existe
                libro_data_session = request.session.get('libro_data', {})
                img_url = libro_data_session.get('img', '') or ''
                
                print(f"📦 Datos editados a guardar: titulo={titulo}, autor={autor}, ejemplares={len(ejemplares)}")  # Debug
                
            elif 'libro_data' in request.session:
                print("📦 Procesando datos originales de la sesión")  # Debug
                
                # Obtener datos de la sesión (datos originales)
                libro_data = request.session['libro_data']
                print(f"📦 Datos a guardar: {libro_data}")  # Debug
                
                # Obtener datos comunes para todos los ejemplares
                titulo = libro_data.get('titulo', '')
                autor = libro_data.get('autor', '')
                editorial = libro_data.get('editorial', '')
                descripcion = libro_data.get('descripcion', '')
                siglas_autor_titulo = libro_data.get('siglas_autor_titulo', '')
                clasificacion_cdu = libro_data.get('clasificacion_cdu', '')
                etiqueta_palabra_clave = libro_data.get('etiqueta_palabra_clave', '')
                img_url = libro_data.get('img', '') or ''
                
                # Obtener la lista de ejemplares
                ejemplares = libro_data.get('ejemplares', [])
            else:
                print("❌ No hay datos para procesar")  # Debug
                messages.error(request, 'No hay datos para guardar.')
                return redirect('formulario_libro')
            
            num_ejemplares = len(ejemplares)
            libros_guardados = []
            
            # Crear un libro por cada ejemplar
            for i, ejemplar_data in enumerate(ejemplares):
                # Crear el libro en base de datos
                libro = Libro(
                    estado='Disponible',
                    titulo=titulo,
                    autor=autor,
                    editorial=editorial,
                    descripcion=descripcion,
                    siglas_autor_titulo=siglas_autor_titulo,
                    clasificacion_cdu=clasificacion_cdu,
                    etiqueta_palabra_clave=etiqueta_palabra_clave,
                    sede=ejemplar_data.get('sede', ''),
                    disponibilidad=ejemplar_data.get('disponibilidad', ''),
                    observaciones=ejemplar_data.get('observaciones', ''),
                    num_ejemplar=ejemplar_data.get('numero', i + 1),  # Número de ejemplar
                    img=img_url  # Misma imagen para todos los ejemplares
                )
                
                # GUARDAR EN BASE DE DATOS
                libro.save()
                libros_guardados.append(libro)
                print(f"✅ Ejemplar {i+1}/{num_ejemplares} guardado con ID: {libro.id_libro}")  # Debug
            
            print(f"📷 URL de imagen guardada: '{img_url}'")  # Debug
            print(f"✅ Total de ejemplares guardados: {len(libros_guardados)}")  # Debug
            
            # Limpiar sesión
            del request.session['libro_data']
            
            # messages.success(request, f'✅ {num_ejemplares} ejemplares del libro "{titulo}" registrados exitosamente.')
            return redirect('confirmacion_carga_exitosa')
            
        except Exception as e:
            print(f"❌ Error al guardar: {e}")  # Debug
            import traceback
            traceback.print_exc()
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
    return redirect('alta_materiales')

def modificacion_materiales(request):
    """
    Vista para mostrar la página de modificación de materiales
    Muestra todos los materiales disponibles para modificar
    """
    # Obtener todos los materiales (disponibles y no disponibles)
    libros = Libro.objects.all().order_by('-id_libro')
    mapas = Mapas.objects.all().order_by('-id_mapa')
    multimedia = Multimedia.objects.all().order_by('-id_multi')
    notebooks = Notebook.objects.all().order_by('-id_not')
    proyectores = Proyector.objects.all().order_by('-id_proyector')
    varios = Varios.objects.all().order_by('-id_varios')
    programas = Programa.objects.all().order_by('-id_programa')
    
    return render(request, 'materiales/formularios_editar/modificacion_materiales.html', {
        'libros': libros,
        'mapas': mapas,
        'multimedia': multimedia,
        'notebooks': notebooks,
        'proyectores': proyectores,
        'varios': varios,
        'programas': programas
    })


@require_POST
def dar_alta_libro(request):
    """Vista para dar de alta un libro (cambiar estado a disponible)"""
    try:
        libro_id = request.POST.get('libro_id')
        sede = request.POST.get('sede', 'LA PLATA')
        disponibilidad = request.POST.get('disponibilidad', 'Domicilio')  # Cambio aquí
        observaciones = request.POST.get('observaciones', '')
        
        if not libro_id:
            return JsonResponse({
                'success': False, 
                'error': 'ID de libro requerido'
            }, status=400)
        
        # Obtener el libro
        libro = get_object_or_404(Libro, id_libro=libro_id)
        
        # Verificar que esté dado de baja
        if libro.estado != 'No disponible':
            return JsonResponse({
                'success': False, 
                'error': 'El libro no está dado de baja'
            }, status=400)
        
        # Actualizar el libro
        libro.estado = 'Disponible'
        libro.sede = sede
        libro.disponibilidad = disponibilidad  # Usar el campo correcto del modelo
        
        # Agregar observaciones si las hay
        if observaciones:
            libro.observaciones = observaciones
        
        # Limpiar motivo de baja al reactivar
        libro.motivo_baja = ''
        # NO borrar la imagen_rota - mantenerla como historial
        
        libro.save()
        
        print(f"✅ Libro '{libro.titulo}' dado de alta - Disponibilidad: {disponibilidad}")
        
        return JsonResponse({
            'success': True,
            'message': f'Libro "{libro.titulo}" dado de alta correctamente',
            'libro_id': libro_id,
            'nuevo_estado': 'Disponible'
        })
        
    except Exception as e:
        print(f"❌ Error en dar_alta_libro: {e}")
        return JsonResponse({
            'success': False,
            'error': f'Error interno: {str(e)}'
        }, status=500)
@require_POST
def obtener_informe_baja_mapa(request):
    """Vista para obtener el informe de baja de un mapa específico"""
    try:
        data = json.loads(request.body)
        mapa_id = data.get('mapa_id')
        
        print(f"🗺️ Obteniendo informe de baja para mapa ID: {mapa_id}")
        
        # Obtener el mapa - CORREGIDO: usar id_mapa en lugar de id
        mapa = get_object_or_404(Mapas, id_mapa=mapa_id)
        
        # Verificar que el mapa esté dado de baja
        if mapa.estado != 'No disponible':
            return JsonResponse({
                'success': False,
                'error': 'El mapa no está dado de baja'
            }, status=400)
        
        # Construir URL de la imagen si existe
        imagen_baja_url = None
        if mapa.imagen_rota:
            imagen_baja_url = request.build_absolute_uri(mapa.imagen_rota.url)
        
        # Obtener los datos reales de la baja desde el modelo
        informe_data = {
            'motivo': mapa.motivo_baja if mapa.motivo_baja else 'Motivo no registrado',
            'fecha_baja': '30/10/2024',  # Puedes agregar este campo al modelo si lo necesitas
            'imagen_baja': imagen_baja_url,  # URL completa o None
            'usuario_baja': 'Admin',  # Puedes agregar este campo al modelo si lo necesitas
            'descripcion': mapa.descripcion if mapa.descripcion else '',
        }
        
        print(f"📋 Datos del informe de mapa enviados: {informe_data}")
        
        return JsonResponse({
            'success': True,
            'informe': informe_data
        })
        
    except Exception as e:
        print(f"❌ Error en obtener_informe_baja_mapa: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'error': f'Error: {str(e)}'
        }, status=500)

@require_POST
def dar_alta_mapa(request):
    """Vista para dar de alta un mapa (cambiar estado a disponible)"""
    try:
        mapa_id = request.POST.get('mapa_id')
        sede = request.POST.get('sede', 'LA PLATA')
        observaciones = request.POST.get('observaciones', '')
        
        if not mapa_id:
            return JsonResponse({
                'success': False, 
                'error': 'ID de mapa requerido'
            }, status=400)
        
        # Obtener el mapa
        mapa = get_object_or_404(Mapas, id_mapa=mapa_id)
        
        # Verificar que esté dado de baja
        if mapa.estado != 'No disponible':
            return JsonResponse({
                'success': False, 
                'error': 'El mapa no está dado de baja'
            }, status=400)
        
        # Actualizar el mapa
        mapa.estado = 'Disponible'
        mapa.sede = sede
        
        # Agregar observaciones si las hay
        if observaciones:
            mapa.descripcion = observaciones  # Usar descripcion para observaciones en mapas
        
        # Limpiar motivo de baja al reactivar
        mapa.motivo_baja = ''
        # NO borrar la imagen_rota - mantenerla como historial
        
        mapa.save()
        
        print(f"✅ Mapa '{mapa.tipo}' dado de alta - Sede: {sede}")
        
        return JsonResponse({
            'success': True,
            'message': f'Mapa "{mapa.tipo}" dado de alta correctamente',
            'mapa_id': mapa_id,
            'nuevo_estado': 'Disponible'
        })
    
    except Exception as e:
        print(f"❌ Error al dar de alta mapa: {str(e)}")
        return JsonResponse({
            'success': False, 
            'error': f'Error interno del servidor: {str(e)}'
        }, status=500)

# ===== FUNCIONES PARA MULTIMEDIA =====

@login_required
@require_POST
def obtener_informe_baja_multimedia(request):
    """
    Vista para obtener información de baja de un multimedia específico
    """
    print(f"🔍 DEBUG: Usuario autenticado: {request.user.is_authenticated}")
    print(f"🔍 DEBUG: Usuario: {request.user}")
    print(f"🔍 DEBUG: Método de request: {request.method}")
    print(f"🔍 DEBUG: POST data: {request.POST}")
    
    try:
        multimedia_id = request.POST.get('multimedia_id')
        print(f"🔍 DEBUG: multimedia_id recibido: {multimedia_id}")
        
        if not multimedia_id:
            print("❌ DEBUG: No se recibió multimedia_id")
            return JsonResponse({
                'success': False, 
                'error': 'ID de multimedia requerido'
            }, status=400)
        
        # Obtener el multimedia
        multimedia = get_object_or_404(Multimedia, id_multi=multimedia_id)
        print(f"🔍 DEBUG: Multimedia encontrado: {multimedia.titulo_contenido}, Estado: {multimedia.estado}")
        
        # Verificar que esté dado de baja
        if multimedia.estado != 'No disponible':
            print(f"❌ DEBUG: Multimedia no está dado de baja. Estado actual: {multimedia.estado}")
            return JsonResponse({
                'success': False, 
                'error': 'El multimedia no está dado de baja'
            }, status=400)
        
        # Preparar datos del informe
        informe_data = {
            'titulo_contenido': multimedia.titulo_contenido or 'Sin título',
            'profesor': multimedia.profesor or 'Sin especificar',
            'carrera': multimedia.carrera or 'Sin especificar',
            'materia': multimedia.materia or 'Sin especificar',
            'motivo_baja': multimedia.motivo_baja or 'Sin motivo especificado',
            'fecha_baja': '15/01/2025',  # Fecha hardcodeada como en los otros casos
            'usuario_baja': 'Admin Sistema',  # Usuario hardcodeado
            'enlace': multimedia.ingresar_enlace or 'Sin enlace',
            'sede': 'No especificado'  # Multimedia no tiene campo sede
        }
        
        # Agregar URL de imagen si existe
        if hasattr(multimedia, 'imagen_rota') and multimedia.imagen_rota:
            informe_data['imagen_url'] = multimedia.imagen_rota.url
        
        print(f"✅ DEBUG: Enviando respuesta exitosa con datos: {informe_data}")
        return JsonResponse({
            'success': True,
            'informe': informe_data
        })
        
    except Exception as e:
        print(f"❌ Error al obtener informe de baja multimedia: {str(e)}")
        import traceback
        print(f"❌ Traceback completo: {traceback.format_exc()}")
        return JsonResponse({
            'success': False, 
            'error': f'Error al cargar: {str(e)}'
        }, status=500)

@login_required
@require_POST
def dar_alta_multimedia(request):
    """
    Vista para reactivar un multimedia dado de baja
    """
    try:
        multimedia_id = request.POST.get('multimedia_id')
        sede = request.POST.get('sede', 'LA PLATA')
        observaciones = request.POST.get('observaciones', '')
        
        if not multimedia_id:
            return JsonResponse({
                'success': False, 
                'error': 'ID de multimedia requerido'
            }, status=400)
        
        # Obtener el multimedia
        multimedia = get_object_or_404(Multimedia, id_multi=multimedia_id)
        
        # Verificar que esté dado de baja
        if multimedia.estado != 'No disponible':
            return JsonResponse({
                'success': False, 
                'error': 'El multimedia no está dado de baja'
            }, status=400)
        
        # Actualizar el multimedia
        multimedia.estado = 'Disponible'
        multimedia.sede = sede
        
        # Agregar observaciones si las hay (usar un campo apropiado)
        if observaciones:
            # Para multimedia, podemos usar el campo profesor para observaciones adicionales
            multimedia.profesor = f"{multimedia.profesor} - {observaciones}" if multimedia.profesor else observaciones
        
        # Limpiar motivo de baja al reactivar
        multimedia.motivo_baja = ''
        # NO borrar la imagen_rota - mantenerla como historial
        
        multimedia.save()
        
        print(f"✅ Multimedia '{multimedia.titulo_contenido}' dado de alta - Sede: {sede}")
        
        return JsonResponse({
            'success': True,
            'message': f'Multimedia "{multimedia.titulo_contenido}" dado de alta correctamente',
            'multimedia_id': multimedia_id,
            'nuevo_estado': 'Disponible'
        })
    
    except Exception as e:
        print(f"❌ Error al dar de alta multimedia: {str(e)}")
        return JsonResponse({
            'success': False, 
            'error': f'Error interno del servidor: {str(e)}'
        }, status=500)
        
    except Exception as e:
        print(f"❌ Error en dar_alta_mapa: {e}")
        return JsonResponse({
            'success': False,
            'error': f'Error interno: {str(e)}'
        }, status=500)

@require_POST  

def obtener_informe_baja(request):
    """Vista para obtener los datos del informe de baja"""
    try:
        libro_id = request.POST.get('libro_id')
        
        print(f"🔍 Obteniendo informe para libro ID: {libro_id}")
        
        if not libro_id:
            return JsonResponse({
                'success': False,
                'error': 'ID de libro requerido'
            }, status=400)
        
        libro = get_object_or_404(Libro, id_libro=libro_id)
        
        print(f"📚 Libro encontrado: {libro.titulo}")
        print(f"📝 Motivo de baja: {libro.motivo_baja}")
        print(f"🖼️ Imagen rota: {libro.imagen_rota}")
        
        # Construir URL de imagen si existe
        imagen_baja_url = None
        if libro.imagen_rota:
            # IMPORTANTE: Construir la URL completa
            imagen_baja_url = libro.imagen_rota.url
            print(f"✅ URL de imagen construida: {imagen_baja_url}")
        else:
            print("❌ No hay imagen de baja")
        
        # Obtener los datos reales de la baja desde tu modelo
        informe_data = {
            'motivo': libro.motivo_baja if libro.motivo_baja else 'Motivo no registrado',
            'fecha_baja': '30/10/2024',  # Puedes agregar este campo a tu modelo si lo necesitas
            'imagen_baja': imagen_baja_url,  # URL completa o None
            'usuario_baja': 'Admin',  # Puedes agregar este campo a tu modelo si lo necesitas
            'descripcion': libro.descripcion if libro.descripcion else '',
        }
        
        print(f"📋 Datos del informe enviados: {informe_data}")
        
        return JsonResponse({
            'success': True,
            'informe': informe_data
        })
        
    except Exception as e:
        print(f"❌ Error en obtener_informe_baja: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'error': f'Error: {str(e)}'
        }, status=500)

# NUEVA VISTA para ver detalles del material (modal con imagen)
def ver_detalles_material(request, libro_id):
    """Vista para obtener detalles completos del material"""
    try:
        # Obtener el tipo de material desde los parámetros de consulta
        tipo = request.GET.get('tipo', 'libro')
        
        if tipo == 'libro':
            material = get_object_or_404(Libro, id_libro=libro_id)
            detalles = {
                'detalle_num_inventario': material.num_ejemplar,
                'detalle_titulo': material.titulo,
                'detalle_autor': material.autor,
                'detalle_editorial': material.editorial,
                'detalle_cdu': material.clasificacion_cdu,
                'detalle_siglas': material.siglas_autor_titulo,
                'detalle_sede': material.sede,
                'detalle_disponibilidad': material.disponibilidad,
                'detalle_estado': material.estado,
                'detalle_descripcion': material.descripcion,
                'detalle_observaciones': material.observaciones,
                'detalle_imagen': material.img if material.img else None,
                'detalle_etiquetas': material.etiqueta_palabra_clave.split(',') if material.etiqueta_palabra_clave else [],
            }
            
        elif tipo == 'mapa':
            material = get_object_or_404(Mapas, id_mapa=libro_id)
            detalles = {
                'detalle_mapa_id': material.id_mapa,
                'detalle_mapa_num_registro': material.num_registro,
                'detalle_mapa_tipo': material.tipo,
                'detalle_mapa_sede': material.sede,
                'detalle_mapa_denominacion': material.denominacion,
                'detalle_mapa_estado': 'Activo',
            }
            
        elif tipo == 'programa':
            material = get_object_or_404(Programa, id_programa=libro_id)
            detalles = {
                'detalle_programa_id': material.id_programa,
                'detalle_programa_profesor': material.profesor,
                'detalle_programa_carrera': material.carrera,
                'detalle_programa_materia': material.materia,
                'detalle_programa_enlace': material.ingresar_enlace,
                'detalle_programa_ciclo': material.ciclo_lectivo,
                'detalle_programa_sede': material.sede,
                'detalle_programa_disponibilidad': material.disponibilidad,
                'detalle_programa_observaciones': material.observaciones,
                'detalle_programa_img': material.img if material.img else None,
                'detalle_programa_num_registro': 'N/A',
                'detalle_programa_denominacion': f"{material.materia} - {material.carrera}",
            }
            
        elif tipo == 'multimedia':
            material = get_object_or_404(Multimedia, id_multi=libro_id)
            detalles = {
                'detalle_multimedia_id': material.id_multi,
                'detalle_multimedia_profesor': material.profesor,
                'detalle_multimedia_carrera': material.carrera,
                'detalle_multimedia_materia': material.materia,
                'detalle_multimedia_enlace': material.ingresar_enlace,
                'detalle_multimedia_titulo_contenido': material.titulo_contenido,
                'detalle_multimedia_num_registro': 'N/A',
                'detalle_multimedia_sede': 'N/A',
                'detalle_multimedia_denominacion': material.titulo_contenido,
                'detalle_multimedia_estado': 'Activo',
            }
            
        elif tipo == 'notebook':
            material = get_object_or_404(Notebook, id_not=libro_id)
            detalles = {
                'detalle_notebook_id': material.id_not,
                'detalle_notebook_num_registro': material.num_registro,
                'detalle_notebook_sede': material.sede,
                'detalle_notebook_modelo': material.modelo_not,
                'detalle_notebook_estado': material.estado,
                'detalle_notebook_denominacion': material.modelo_not,
            }
            
        elif tipo == 'proyector':
            material = get_object_or_404(Proyector, id_proyector=libro_id)
            detalles = {
                'detalle_proyector_id': material.id_proyector,
                'detalle_proyector_num_registro': material.num_registro,
                'detalle_proyector_sede': material.sede,
                'detalle_proyector_modelo': material.modelo_pro,
                'detalle_proyector_marca': 'N/A',
                'detalle_proyector_estado': material.estado,
                'detalle_proyector_denominacion': f"Proyector {material.modelo_pro}",
            }
            
        elif tipo == 'varios':
            material = get_object_or_404(Varios, id_varios=libro_id)
            detalles = {
                'detalle_varios_id': material.id_varios,
                'detalle_varios_tipo': material.tipo,
                'detalle_varios_sede': material.sede,
                'detalle_varios_num_registro': 'N/A',
                'detalle_varios_denominacion': f"Material varios - {material.tipo}",
                'detalle_varios_estado': 'Activo',
                'detalle_varios_cantidad': material.cantidad,
                'detalle_varios_cantidad_disponible': material.cantidad_disponible,
            }
            
        else:
            return JsonResponse({
                'success': False,
                'error': f'Tipo de material no válido: {tipo}'
            }, status=400)
        
        return JsonResponse({
            'success': True,
            'detalles': detalles
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error: {str(e)}'
        }, status=500)
    
    

def reactivar_libro_mejorado(request, libro_id):
    """
    Función mejorada para reactivar libros que integra con el sistema de obleas
    """
    if request.method == 'POST':
        libro = get_object_or_404(Libro, id_libro=libro_id)
        
        # Verificar que esté dado de baja
        if libro.estado != 'No disponible':
            messages.error(request, f'El libro "{libro.titulo}" no está dado de baja.')
            return redirect('modificacion_materiales')
        
        # Actualizar estado
        libro.estado = 'Disponible'
        libro.motivo_baja = ''  # Limpiar motivo de baja
        
        # Mantener otros datos como están
        libro.save()
        
        # messages.success(request, f'✅ El libro "{libro.titulo}" ha sido reactivado exitosamente.')
        return redirect('modificacion_materiales')
    
    return redirect('modificacion_materiales')   

# Agregar decoradores similares a todas las vistas de alta de material
#@user_passes_test(es_bibliotecaria)
def alta_mapa(request):
    return render(request, 'materiales/formularios_altas/alta_mapa.html')

#@user_passes_test(es_bibliotecaria)
def formulario_multimedia(request):
    """
    Vista para mostrar el formulario de alta de multimedia (solo GET)
    """
    print("🎬 LLEGÓ A formulario_multimedia")  # DEBUG
    form = MultimediaForm()
    return render(request, 'materiales/formularios_altas/alta_multimedia.html', {'form': form})

#@user_passes_test(es_bibliotecaria)
def alta_multimedia(request):
    """
    Vista para procesar el envío del formulario de alta de multimedia
    """
    print(f"🔥🔥🔥 INICIO alta_multimedia")
    print(f"🔥 Método: {request.method}")
    print(f"🔥 URL: {request.path}")
    print(f"🔥 POST data keys: {list(request.POST.keys()) if request.method == 'POST' else 'No POST'}")
    
    if request.method == 'POST':
        print("🔥 POST recibido en alta_multimedia - procesando para modal")
        
        # Verificar si hay datos en POST
        if not request.POST:
            print("❌ POST está vacío!")
            messages.error(request, 'No se recibieron datos del formulario.')
            return redirect('formulario_multimedia')
            
        form = MultimediaForm(request.POST)
        print(f"🔍 Formulario MultimediaForm creado. Es válido? {form.is_valid()}")
        
        if not form.is_valid():
            print(f"❌ Errores del formulario: {form.errors}")
            # Mostrar errores en la página
            return render(request, 'materiales/formularios_altas/alta_multimedia.html', {
                'form': form,
                'error': 'Por favor corrige los errores en el formulario.'
            })
        
        if form.is_valid():
            print("✅ Formulario válido - guardando en sesión")
            try:
                # Obtener la URL de imagen del formulario
                img_url = form.cleaned_data.get('img', '').strip()
                print(f"📷 URL de imagen recibida: '{img_url}'")
                
                # Procesar datos básicos del formulario
                form_data = {
                    'profesor': form.cleaned_data.get('profesor', ''),
                    'carrera': form.cleaned_data.get('carrera', ''),
                    'materia': form.cleaned_data.get('materia', ''),
                    'ingresar_enlace': form.cleaned_data.get('ingresar_enlace', ''),
                    'titulo_contenido': form.cleaned_data.get('titulo_contenido', ''),
                }
                
                # Procesar datos dinámicos de multimedia
                multimedia_list = []
                material_counter = 1  # Contador para la numeración secuencial
                
                # Procesar elementos dinámicos primero
                grupos_multimedia_json = request.POST.get('gruposMultimedia', '[]')
                print(f"📦 Datos dinámicos recibidos: {grupos_multimedia_json}")
                print(f"📦 Tipo de datos recibidos: {type(grupos_multimedia_json)}")
                print(f"📦 Longitud de datos recibidos: {len(grupos_multimedia_json)}")
                
                elementos_dinamicos_validos = []
                
                try:
                    grupos_multimedia = json.loads(grupos_multimedia_json)
                    print(f"📦 Grupos multimedia parseados: {grupos_multimedia}")
                    print(f"📦 Tipo de grupos parseados: {type(grupos_multimedia)}")
                    print(f"📦 Cantidad de grupos parseados: {len(grupos_multimedia)}")
                    
                    for i, grupo in enumerate(grupos_multimedia):
                        print(f"📋 Grupo {i} completo: {grupo}")
                        print(f"📋 Tipo del grupo {i}: {type(grupo)}")
                        print(f"📋 Claves del grupo {i}: {list(grupo.keys()) if isinstance(grupo, dict) else 'No es dict'}")
                        
                        # Obtener datos directamente del JSON parseado
                        titulo = grupo.get('titulo', '').strip()
                        enlace = grupo.get('url', '').strip()
                        
                        print(f"📋 Procesando grupo {i}: titulo='{titulo}', enlace='{enlace}'")
                        
                        # SOLUCIÓN DEFINITIVA: Validación más estricta pero inclusiva
                        # Aceptar elementos que tengan al menos título O enlace (no ambos vacíos)
                        if titulo or enlace:
                            multimedia_item = {
                                'titulo_contenido': titulo,
                                'ingresar_enlace': enlace,
                                'tipo': f'Material {material_counter}'
                            }
                            elementos_dinamicos_validos.append(multimedia_item)
                            material_counter += 1  # Incrementar contador para el siguiente material
                            print(f"✅ Elemento dinámico válido encontrado: {multimedia_item}")
                        else:
                            print(f"❌ Grupo {i} no agregado - ambos campos vacíos")
                            
                except json.JSONDecodeError as e:
                    print(f"❌ Error al parsear JSON de grupos multimedia: {e}")
                
                # SOLUCIÓN DEFINITIVA FINAL: Lógica simplificada y correcta
                print(f"🔍 Elementos dinámicos válidos encontrados: {len(elementos_dinamicos_validos)}")
                print(f"🔍 Datos formulario principal: titulo='{form_data['titulo_contenido']}', enlace='{form_data['ingresar_enlace']}'")
                
                if elementos_dinamicos_validos:
                    # CASO 1: Hay elementos dinámicos válidos
                    # El frontend SIEMPRE incluye el formulario principal como primer elemento
                    # Por lo tanto, usar TODOS los elementos dinámicos
                    multimedia_list = elementos_dinamicos_validos
                    print(f"✅ CASO 1: Usando TODOS los {len(multimedia_list)} elementos dinámicos (frontend incluye principal)")
                    
                elif form_data['titulo_contenido'].strip() or form_data['ingresar_enlace'].strip():
                    # CASO 2: Solo formulario principal, sin elementos dinámicos
                    multimedia_list.append({
                        'titulo_contenido': form_data['titulo_contenido'],
                        'ingresar_enlace': form_data['ingresar_enlace'],
                        'tipo': 'Material 1'
                    })
                    print(f"✅ CASO 2: Usando solo formulario principal como Material 1")
                    
                else:
                    # CASO 3: No hay datos válidos
                    print(f"❌ CASO 3: No hay datos válidos ni en formulario principal ni en elementos dinámicos")
                
                # Renumerar todos los elementos secuencialmente
                for i, elemento in enumerate(multimedia_list, 1):
                    elemento['tipo'] = f'Material {i}'
                
                print(f"✅ Lista final con {len(multimedia_list)} elementos renumerados secuencialmente")
                
                # Verificar que hay al menos un elemento
                if not multimedia_list:
                    print(f"❌ No hay datos válidos ni en formulario principal ni en elementos dinámicos")
                
                # Agregar la lista de multimedia a form_data
                form_data['multimedia_list'] = multimedia_list
                print(f"📦 Lista final de multimedia: {multimedia_list}")
                
                # Guardar en sesión
                request.session['multimedia_data'] = form_data
                print(f"📦 Datos guardados en sesión: {form_data}")
                
                # Redirigir al modal de confirmación
                print("🚀 Redirigiendo a confirmar_alta_multimedia")
                return redirect('confirmar_alta_multimedia')
                
            except Exception as e:
                print(f"❌ Error al procesar: {e}")
                import traceback
                traceback.print_exc()
                messages.error(request, f'Error al procesar el multimedia: {str(e)}')
                return render(request, 'materiales/formularios_altas/alta_multimedia.html', {
                    'form': form,
                    'error': f'Error al procesar: {str(e)}'
                })
    else:
        # Si es GET, mostrar formulario vacío
        print("🔄 GET recibido en alta_multimedia, mostrando formulario")
        form = MultimediaForm()
        return render(request, 'materiales/formularios_altas/alta_multimedia.html', {'form': form})

def confirmar_alta_multimedia(request):
    """
    Vista para mostrar el modal de confirmación de alta de multimedia
    """
    print("🎯 Llegó a confirmar_alta_multimedia")
    
    # Obtener datos de la sesión
    multimedia_data = request.session.get('multimedia_data', {})
    print(f"📋 Datos de sesión: {multimedia_data}")
    
    if not multimedia_data:
        print("❌ No hay datos de multimedia en sesión")
        messages.error(request, 'No se encontraron datos del multimedia. Por favor, completa el formulario nuevamente.')
        return redirect('formulario_multimedia')
    
    # Limpiar valores None para evitar problemas en JavaScript
    def clean_none_values(data):
        if isinstance(data, dict):
            return {k: clean_none_values(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [clean_none_values(item) for item in data]
        elif data is None:
            return ""
        else:
            return data
    
    cleaned_data = clean_none_values(multimedia_data)
    print(f"📋 Datos limpiados: {cleaned_data}")
    
    return render(request, 'materiales/formularios_altas/confirmaciones_alta/confirmacion_alta_multimedia.html', {
        'form_data': cleaned_data
    })

def guardar_alta_multimedia(request):
    """
    Vista para guardar definitivamente el multimedia en la base de datos
    """
    print("💾 Llegó a guardar_alta_multimedia")  # Debug
    
    if request.method == 'POST' and 'multimedia_data' in request.session:
        print("✅ POST recibido y datos en sesión")  # Debug
        
        try:
            # Obtener datos de la sesión
            form_data = request.session['multimedia_data']
            print(f"📋 Datos de sesión: {form_data}")  # Debug
            
            # Obtener datos comunes (usar valores editados si existen)
            profesor = request.POST.get('profesor_editado', form_data.get('profesor', ''))
            carrera = request.POST.get('carrera_editada', form_data.get('carrera', ''))
            materia = request.POST.get('materia_editada', form_data.get('materia', ''))
            
            print(f"📝 Datos finales - Profesor: {profesor}, Carrera: {carrera}, Materia: {materia}")
            
            # Obtener lista de multimedia
            multimedia_list = form_data.get('multimedia_list', [])
            print(f"📦 Lista de multimedia a guardar: {multimedia_list}")
            
            multimedia_guardados = []
            
            if multimedia_list:
                # Guardar cada elemento de la lista
                for i, multimedia_data in enumerate(multimedia_list):
                    contador = i + 1
                    print(f"💾 Guardando elemento {contador}: {multimedia_data}")
                    
                    # Usar valores editados si existen, sino usar los originales
                    titulo_editado = request.POST.get(f'titulo_editado_{contador}')
                    enlace_editado = request.POST.get(f'enlace_editado_{contador}')
                    
                    titulo_final = titulo_editado if titulo_editado else multimedia_data.get('titulo_contenido', '')
                    enlace_final = enlace_editado if enlace_editado else multimedia_data.get('ingresar_enlace', '')
                    
                    print(f"📝 Elemento {contador} - Título: {titulo_final}, Enlace: {enlace_final}")
                    
                    multimedia = Multimedia(
                        estado='Disponible',
                        profesor=profesor,
                        carrera=carrera,
                        materia=materia,
                        ingresar_enlace=enlace_final,
                        titulo_contenido=titulo_final
                    )
                    
                    # GUARDAR EN BASE DE DATOS
                    multimedia.save()
                    multimedia_guardados.append(multimedia)
                    print(f"✅ Multimedia {contador} guardado en BD con ID: {multimedia.id_multi}")
            else:
                # Fallback: guardar datos básicos si no hay lista
                print("⚠️ No hay multimedia_list, guardando datos básicos")
                multimedia = Multimedia(
                    estado='Disponible',
                    profesor=profesor,
                    carrera=carrera,
                    materia=materia,
                    ingresar_enlace=form_data.get('ingresar_enlace', ''),
                    titulo_contenido=form_data.get('titulo_contenido', '')
                )
                multimedia.save()
                multimedia_guardados.append(multimedia)
                print(f"✅ Multimedia básico guardado en BD con ID: {multimedia.id_multi}")
            
            # Limpiar sesión
            del request.session['multimedia_data']
            
            # Mensaje de éxito
            if len(multimedia_guardados) > 1:
                messages.success(request, f'✅ {len(multimedia_guardados)} elementos multimedia registrados exitosamente.')
            else:
                messages.success(request, f'✅ Multimedia "{multimedia_guardados[0].titulo_contenido}" registrado exitosamente.')
            
            return redirect('confirmacion_carga_exitosa')
            
        except Exception as e:
            print(f"❌ Error al guardar: {e}")  # Debug
            import traceback
            traceback.print_exc()
            messages.error(request, f'❌ Error al guardar el multimedia: {str(e)}')
            return redirect('confirmacion_carga_exitosa')
    else:
        print("❌ No hay datos o método incorrecto")  # Debug
        messages.error(request, 'No hay datos para guardar.')
        return redirect('confirmacion_carga_exitosa')

def cancelar_alta_multimedia(request):
    """
    Vista para cancelar la alta y limpiar datos de sesión
    """
    print("🔴 Cancelando alta de multimedia")  # Debug
    
    if 'multimedia_data' in request.session:
        del request.session['multimedia_data']
        print("🗑️ Datos de sesión eliminados")  # Debug
    
    messages.info(request, 'Operación cancelada.')
    return redirect('alta_materiales')

# Comentando esta función duplicada para evitar conflictos
'''
#@user_passes_test(es_bibliotecaria)
def alta_notebook(request):
    # ... código existente ...
    pass
'''

#@user_passes_test(es_bibliotecaria)
def alta_proyector(request):
    # ... código existente ...
    pass

#@user_passes_test(es_bibliotecaria)
def alta_varios(request):
    # ... código existente ...
    pass

def confirmacion_alta_varios(request):
    """
    Vista para mostrar el modal de confirmación para varios
    """
    print("🎯 Llegó a confirmacion_alta_varios")  # Debug
    
    if request.method == 'POST':
        # 🔥 LOGS DE DEPURACIÓN DETALLADOS
        print("🔥 === DATOS POST COMPLETOS RECIBIDOS ===")
        print(f"🔥 Todas las claves POST: {list(request.POST.keys())}")
        print(f"🔥 Todos los valores POST: {dict(request.POST)}")
        print("🔥 =====================================")
        
        # Obtener datos básicos
        cant_ejemplares = request.POST.get('cant_ejemplares')
        sede_varios = request.POST.get('sede_varios')
        tipo_varios = request.POST.get('tipo_varios')
        
        print(f"🔍 Datos básicos extraídos:")
        print(f"  - cant_ejemplares: '{cant_ejemplares}'")
        print(f"  - sede_varios: '{sede_varios}'")
        print(f"  - tipo_varios: '{tipo_varios}'")
        
        # Mapeo de sede
        sede_mapping = {
            'sede1': 'La Plata',
            'sede2': 'Abasto'
        }
        sede_texto = sede_mapping.get(sede_varios, sede_varios)
        
        # CORREGIDO: Obtener los tipos de varios desde gruposTiposVariosNuevo JSON
        tipos_varios = []
        grupos_tipos_json = request.POST.get('gruposTiposVariosNuevo', '[]')
        
        print(f"🔍 gruposTiposVariosNuevo JSON recibido: '{grupos_tipos_json}'")  # Debug
        print(f"🔍 Tipo de dato recibido: {type(grupos_tipos_json)}")
        print(f"🔍 Longitud del string JSON: {len(grupos_tipos_json) if grupos_tipos_json else 0}")  # Debug
        
        try:
            grupos_tipos_data = json.loads(grupos_tipos_json) if grupos_tipos_json else []
        except json.JSONDecodeError as e:
            print(f"❌ Error al decodificar JSON de gruposTiposVariosNuevo: {e}")  # Debug
            grupos_tipos_data = []
        
        print(f"📋 Grupos tipos data decodificados: {grupos_tipos_data}")  # Debug
        
        # CORRECCIÓN DEFINITIVA PARA VARIOS: Procesar TODOS los elementos (principal + dinámicos)
        elementos_todos = grupos_tipos_data if grupos_tipos_data else []
        print(f"🔄 Procesando TODOS los elementos de VARIOS: {elementos_todos}")  # Debug
        
        # Procesar cada grupo de tipos (principal + dinámicos)
        for grupo_idx, grupo_data in enumerate(elementos_todos):
            tipo_grupo = grupo_data.get('tipo', '')
            cantidad_grupo = grupo_data.get('cantidad', 0)
            
            print(f"🔄 Procesando grupo {grupo_idx}: tipo='{tipo_grupo}', cantidad={cantidad_grupo}")  # Debug
            
            ejemplares = []
            
            # Buscar ejemplares para este grupo
            for ejemplar_idx in range(int(cantidad_grupo)):
                # Usar el índice directo del array (ya no aplicamos slice)
                registro_key = f'varios_{grupo_idx}_{ejemplar_idx}_registro'
                denominacion_key = f'varios_{grupo_idx}_{ejemplar_idx}_denominacion'
                descripcion_key = f'varios_{grupo_idx}_{ejemplar_idx}_descripcion'
                
                registro = request.POST.get(registro_key, '')
                denominacion = request.POST.get(denominacion_key, '')
                descripcion = request.POST.get(descripcion_key, '')
                
                print(f"  📝 Ejemplar {ejemplar_idx}: registro='{registro}', denominacion='{denominacion}', descripcion='{descripcion}' (grupo: {grupo_idx})")  # Debug
                
                if registro or denominacion or descripcion:
                    ejemplares.append({
                        'registro': registro,
                        'denominacion': denominacion,
                        'descripcion': descripcion,
                        'sede': sede_texto,
                        'disponibilidad': 'Disponible'
                    })
            
            # Si no se encontraron ejemplares específicos, crear uno básico usando los datos de gruposTiposVariosNuevo
            if not ejemplares and cantidad_grupo > 0:
                print(f"  ⚠️ No se encontraron ejemplares específicos para grupo {grupo_idx}, creando básicos")  # Debug
                # Usar los datos de gruposTiposVariosNuevo para crear los tipos
                for i in range(int(cantidad_grupo)):
                    ejemplares.append({
                        'registro': '',
                        'denominacion': '',
                        'descripcion': '',
                        'sede': sede_texto,
                        'disponibilidad': 'Disponible'
                    })
            
            if ejemplares:
                tipos_varios.append({
                    'tipo': tipo_grupo,
                    'ejemplares': ejemplares
                })
        
        # Fallback si no hay datos de gruposTiposVariosNuevo
        if not tipos_varios and tipo_varios:
            print("🔄 Fallback: usando datos básicos del formulario")  # Debug
            ejemplares = []
            for i in range(int(cant_ejemplares or 1)):
                ejemplares.append({
                    'registro': '',
                    'denominacion': '',
                    'descripcion': '',
                    'sede': sede_texto,
                    'disponibilidad': 'Disponible'
                })
            
            tipos_varios.append({
                'tipo': tipo_varios,
                'ejemplares': ejemplares
            })
        
        print(f"📤 Datos finales para template: {tipos_varios}")  # Debug
        
        # Guardar en sesión
        request.session['varios_data'] = {
            'cant_ejemplares': cant_ejemplares,
            'sede_varios': sede_varios,
            'sede_texto': sede_texto,
            'tipo_varios': tipo_varios,
            'tipos_varios': tipos_varios
        }
        
        # Preparar datos para el template
        form_data = {
            'cant_ejemplares': cant_ejemplares,
            'sede_texto': sede_texto,
            'tipo_varios': tipo_varios,
            'tipos_varios': tipos_varios
        }
        
        return render(request, 'materiales/formularios_altas/confirmaciones_alta/confirmacion_alta_varios.html', {
            'form_data': form_data
        })
    else:
        # Si no es POST, redirigir al formulario
        messages.error(request, 'Método no permitido. Por favor, complete el formulario correctamente.')
        return redirect('alta_varios')

def cancelar_alta_varios(request):
    """
    Vista para cancelar el alta de varios
    """
    # Limpiar datos de sesión si existen
    if 'varios_data' in request.session:
        del request.session['varios_data']
    
    messages.info(request, 'Se ha cancelado el registro del material varios.')
    return redirect('alta_materiales')

def guardar_alta_varios(request):
    """
    Vista para guardar definitivamente después de confirmar en el modal
    """
    print("💾 Guardando material varios confirmado")  # Debug
    
    if request.method == 'POST':
        # Recuperar datos de la sesión
        varios_data = request.session.get('varios_data', None)
        
        if varios_data:
            try:
                # Obtener los tipos de varios de la sesión
                tipos_varios = varios_data.get('tipos_varios', [])
                
                if not tipos_varios:
                    messages.error(request, 'No se encontraron tipos de materiales para guardar.')
                    return redirect('alta_materiales')
                
                materiales_creados = []
                
                # Crear un registro Varios por cada tipo (agrupado por cantidad)
                for tipo_data in tipos_varios:
                    tipo = tipo_data.get('tipo', '')
                    ejemplares = tipo_data.get('ejemplares', [])
                    cantidad_total = len(ejemplares)
                    sede = ejemplares[0].get('sede', 'La Plata') if ejemplares else 'La Plata'
                    
                    if cantidad_total > 0:
                        # 🔍 VERIFICAR SI YA EXISTE UN MATERIAL CON EL MISMO TIPO Y SEDE
                        varios_existente = Varios.objects.filter(
                            tipo=tipo,
                            sede=sede,
                            estado='Disponible'
                        ).first()
                        
                        if varios_existente:
                            # ✅ SI EXISTE: ACTUALIZAR CANTIDADES
                            varios_existente.cantidad += cantidad_total
                            varios_existente.cantidad_disponible += cantidad_total
                            varios_existente.save()
                            materiales_creados.append(varios_existente)
                            print(f"🔄 Material varios actualizado: {varios_existente} - Nueva cantidad total: {varios_existente.cantidad}")  # Debug
                        else:
                            # ➕ SI NO EXISTE: CREAR NUEVO REGISTRO
                            varios = Varios(
                                tipo=tipo,
                                estado='Disponible',
                                descripcion=ejemplares[0].get('descripcion', '') if ejemplares else '',
                                num_ejemplar=1,  # Mantener para compatibilidad
                                sede=sede,
                                cantidad=cantidad_total,
                                cantidad_disponible=cantidad_total
                            )
                            varios.save()
                            materiales_creados.append(varios)
                            print(f"✅ Material varios creado: {varios} con cantidad: {cantidad_total}")  # Debug
                
                # Limpiar la sesión
                if 'varios_data' in request.session:
                    del request.session['varios_data']
                
                # messages.success(request, f'Se han guardado exitosamente {len(materiales_creados)} tipos de materiales varios.')
                return redirect('confirmacion_carga_exitosa')
                
            except Exception as e:
                print(f"❌ Error al guardar varios: {e}")  # Debug
                messages.error(request, f'Error al guardar los materiales: {str(e)}')
                return redirect('alta_materiales')
        else:
            messages.error(request, 'No se encontraron datos para guardar. Por favor, complete el formulario nuevamente.')
            return redirect('alta_materiales')
    
    # Si no es POST, redirigir
    return redirect('alta_materiales')


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
        tipo_usuario = request.POST.get('tipo_usuario', 'estudiante')
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
        
        # messages.success(request, f"Has solicitado el préstamo del libro '{libro.titulo}'. La biblioteca revisará tu solicitud.")
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


# AGREGAR ESTAS VISTAS COMPLETAS a tu views.py

# AGREGAR ESTAS VISTAS COMPLETAS a tu views.py

def formulario_programa(request):
    """
    Vista para mostrar el formulario de alta de programa (solo GET)
    IMPORTANTE: Esta vista debe existir y funcionar
    """
    print("🎓 LLEGÓ A formulario_programa")  # DEBUG
    form = ProgramaForm()
    return render(request, 'materiales/formularios_altas/formulario_programa.html', {'form': form})

def alta_programa(request):
    """
    Vista para procesar el envío del formulario de alta de programa
    IMPORTANTE: Esta es la vista que recibe el POST del formulario
    """
    print(f"🔥🔥🔥 INICIO alta_programa")
    print(f"🔥 Método: {request.method}")
    print(f"🔥 URL: {request.path}")
    print(f"🔥 POST data keys: {list(request.POST.keys()) if request.method == 'POST' else 'No POST'}")
    
    if request.method == 'POST':
        print("🔥 POST recibido en alta_programa - procesando para modal")
        
        # Verificar si hay datos en POST
        if not request.POST:
            print("❌ POST está vacío!")
            messages.error(request, 'No se recibieron datos del formulario.')
            return redirect('formulario_programa')
            
        form = ProgramaForm(request.POST)
        print(f"🔍 Formulario ProgramaForm creado. Es válido? {form.is_valid()}")
        
        if not form.is_valid():
            print(f"❌ Errores del formulario: {form.errors}")
            # Mostrar errores en la página
            return render(request, 'materiales/formularios_altas/formulario_programa.html', {
                'form': form,
                'error': 'Por favor corrige los errores en el formulario.'
            })
        
        if form.is_valid():
            print("✅ Formulario válido - guardando en sesión")
            try:
                # Obtener la URL de imagen del formulario
                img_url = form.cleaned_data.get('img', '').strip()
                print(f"📷 URL de imagen recibida: '{img_url}'")
                
                # NO guardar en base de datos, solo en sesión - CAMPOS SIMPLIFICADOS
                form_data = {
                    'profesor': form.cleaned_data.get('profesor', ''),
                    'carrera': form.cleaned_data.get('carrera', ''),
                    'materia': form.cleaned_data.get('materia', ''),
                    'ingresar_enlace': form.cleaned_data.get('ingresar_enlace', ''),
                    'ciclo_lectivo': form.cleaned_data.get('ciclo_lectivo', ''),
                }
                
                # Guardar en sesión
                request.session['programa_data'] = form_data
                print(f"📦 Datos guardados en sesión: {form_data}")
                
                # Redirigir al modal de confirmación
                print("🚀 Redirigiendo a confirmar_alta_programa")
                return redirect('confirmar_alta_programa')
                
            except Exception as e:
                print(f"❌ Error al procesar: {e}")
                import traceback
                traceback.print_exc()
                messages.error(request, f'Error al procesar el programa: {str(e)}')
                return render(request, 'materiales/formularios_altas/formulario_programa.html', {
                    'form': form,
                    'error': f'Error al procesar: {str(e)}'
                })
    else:
        # Si es GET, mostrar formulario vacío
        print("🔄 GET recibido en alta_programa, mostrando formulario")
        form = ProgramaForm()
        return render(request, 'materiales/formularios_altas/formulario_programa.html', {'form': form})

def confirmar_alta_programa(request):
    """
    Vista para mostrar el modal de confirmación para programa
    """
    print("🎯 Llegó a confirmar_alta_programa")  # Debug
    
    # Verificar que existan datos en la sesión
    if 'programa_data' not in request.session:
        print("❌ No hay datos en sesión")  # Debug
        messages.error(request, 'No hay datos para confirmar. Por favor, complete el formulario nuevamente.')
        return redirect('formulario_programa')
    
    # Obtener datos de la sesión
    form_data = request.session['programa_data']
    print(f"📋 Datos de sesión: {form_data}")  # Debug
    
    # Renderizar página con modal automático
    return render(request, 'materiales/formularios_altas/confirmaciones_alta/confirmacion_alta_programa.html', {
        'form_data': form_data
    })

def guardar_programa_confirmado(request):
    """
    Vista para guardar definitivamente después de confirmar en el modal
    """
    print("💾 Llegó a guardar_programa_confirmado")  # Debug
    
    if request.method == 'POST':
        try:
            # Verificar si hay datos editados enviados por POST
            if 'profesor' in request.POST:
                # Datos editados enviados desde el frontend
                print("📝 Procesando datos editados desde POST")
                programa_data = {
                    'profesor': request.POST.get('profesor', ''),
                    'carrera': request.POST.get('carrera', ''),
                    'materia': request.POST.get('materia', ''),
                    'ingresar_enlace': request.POST.get('ingresar_enlace', ''),
                    'ciclo_lectivo': request.POST.get('ciclo_lectivo', '')
                }
                print(f"📦 Datos editados a guardar: {programa_data}")
            elif 'programa_data' in request.session:
                # Datos originales de la sesión
                print("📦 Procesando datos originales desde sesión")
                programa_data = request.session['programa_data']
                print(f"📦 Datos originales a guardar: {programa_data}")
            else:
                print("❌ No hay datos para guardar")
                messages.error(request, 'No hay datos para guardar.')
                return redirect('formulario_programa')
            
            # Crear el programa en base de datos
            programa = Programa(
                estado='Disponible',
                profesor=programa_data.get('profesor', ''),
                carrera=programa_data.get('carrera', ''),
                materia=programa_data.get('materia', ''),
                ingresar_enlace=programa_data.get('ingresar_enlace', ''),
                ciclo_lectivo=programa_data.get('ciclo_lectivo', ''),
                # Valores por defecto para campos no incluidos en el formulario
                disponibilidad='Disponible',  # Valor por defecto
                descripcion='',  # Vacío
                observaciones='',  # Vacío
                num_ejemplar=1,  # Valor por defecto
                img=''  # Campo img sí existe en el modelo Programa
            )
            
            # GUARDAR EN BASE DE DATOS
            programa.save()
            print(f"✅ Programa guardado en BD con ID: {programa.id_programa}")  # Debug
            print(f"📷 URL de imagen guardada: '{programa.img}'")  # Debug
            
            # Limpiar sesión si existe
            if 'programa_data' in request.session:
                del request.session['programa_data']
            
            # messages.success(request, f'✅ Programa "{programa.materia}" registrado exitosamente.')
            return redirect('confirmacion_carga_exitosa')
            
        except Exception as e:
            print(f"❌ Error al guardar: {e}")  # Debug
            import traceback
            traceback.print_exc()
            messages.error(request, f'❌ Error al guardar el programa: {str(e)}')
            return redirect('confirmacion_carga_exitosa')
    else:
        print("❌ Método incorrecto")  # Debug
        messages.error(request, 'Método no permitido.')
        return redirect('confirmacion_carga_exitosa')

def cancelar_alta_programa(request):
    """
    Vista para cancelar la alta y limpiar datos de sesión
    """
    print("🔴 Cancelando alta de programa")  # Debug
    
    if 'programa_data' in request.session:
        del request.session['programa_data']
        print("🗑️ Datos de sesión eliminados")  # Debug
    
    messages.info(request, 'Operación cancelada.')
    return redirect('formulario_programa')

# OPCIONAL: Vista para listar programas
def lista_programas(request):
    """
    Vista para listar todos los programas disponibles
    """
    programas = Programa.objects.filter(estado='Disponible')
    return render(request, 'materiales/programas/lista_programas.html', {'programas': programas})

def confirmacion_alta_notebook(request):
    """
    Vista para mostrar el modal de confirmación para notebook
    """
    print("🎯 Llegó a confirmacion_alta_notebook")  # Debug
    
    if request.method == 'POST':
        # Obtener datos básicos del formulario
        cant_ejemplares = int(request.POST.get('cant_ejemplares', 1))
        sede = request.POST.get('sede', '')
        num_registro = request.POST.get('num_registro', '')
        modelo_not = request.POST.get('modelo_not', '')
        
        # Mapeo de valores de sede
        sede_mapping = {
            'sede1': 'La Plata',
            'sede2': 'Abasto'
        }
        
        # Crear lista de ejemplares
        ejemplares = []
        for i in range(cant_ejemplares):
            sede_value = request.POST.get(f'sede_{i+1}', sede)
            sede_texto = sede_mapping.get(sede_value, sede_value)
            
            ejemplar = {
                'sede': sede_texto,  # Usar el nombre real de la sede
                'num_registro': request.POST.get(f'num_registro_{i+1}', num_registro),
                'modelo_not': request.POST.get(f'modelo_not_{i+1}', modelo_not),
                'disponibilidad': 'Disponible'
            }
            ejemplares.append(ejemplar)
        
        # Guardar los datos del formulario en la sesión
        notebook_data = {
            'cant_ejemplares': cant_ejemplares,
            'sede': sede,
            'sede_texto': sede_mapping.get(sede, sede),  # Agregar el nombre legible de la sede
            'num_registro': num_registro,
            'modelo_not': modelo_not,
            'ejemplares': ejemplares,
            'estado': 'Disponible',  # Valor por defecto
        }
        
        # Guardar en sesión
        request.session['notebook_data'] = notebook_data
        print(f"📋 Datos guardados en sesión: {notebook_data}")  # Debug

        # Renderizar página con modal automático
        return render(request, 'materiales/formularios_altas/confirmaciones_alta/confirmacion_alta_notebook.html', {
            'form_data': notebook_data,
            'ejemplares': ejemplares
        })
    else:
        # Si no es POST, redirigir al formulario
        messages.error(request, 'Método no permitido. Por favor, complete el formulario correctamente.')
        return redirect('alta_notebook')

def guardar_alta_notebook(request):
    """
    Vista para guardar definitivamente después de confirmar en el modal
    """
    print("💾 Guardando notebook confirmado")  # Debug
    
    if request.method == 'POST':
        # Recuperar datos de la sesión como base
        notebook_data = request.session.get('notebook_data', {})
        
        if not notebook_data:
            messages.error(request, 'No se encontraron datos del notebook en la sesión.')
            return redirect('alta_materiales')
        
        try:
            # NUEVO: Procesar datos editados del modal si existen
            sede_editada = request.POST.get('sede')
            
            # Crear lista de ejemplares actualizada
            ejemplares_actualizados = []
            ejemplares_originales = notebook_data.get('ejemplares', [])
            
            for i, ejemplar_original in enumerate(ejemplares_originales):
                # Buscar datos editados para este ejemplar
                num_registro_editado = request.POST.get(f'ejemplares[{i}][num_registro]')
                modelo_editado = request.POST.get(f'ejemplares[{i}][modelo_not]')
                
                # Crear ejemplar actualizado con datos editados o originales
                ejemplar_actualizado = {
                    'sede': sede_editada if sede_editada else ejemplar_original.get('sede'),
                    'num_registro': num_registro_editado if num_registro_editado else ejemplar_original.get('num_registro'),
                    'modelo_not': modelo_editado if modelo_editado else ejemplar_original.get('modelo_not'),
                    'disponibilidad': ejemplar_original.get('disponibilidad', 'Disponible')
                }
                ejemplares_actualizados.append(ejemplar_actualizado)
                
                print(f"📝 Ejemplar {i+1} actualizado: {ejemplar_actualizado}")  # Debug
            
            # Crear múltiples notebooks con los datos actualizados
            notebooks_creados = []
            
            for ejemplar in ejemplares_actualizados:
                # Crear notebook con los campos correctos del modelo
                notebook = Notebook.objects.create(
                    num_registro=ejemplar.get('num_registro'),
                    modelo_not=ejemplar.get('modelo_not'),
                    sede=ejemplar.get('sede'),
                    estado=ejemplar.get('disponibilidad', 'Disponible')
                )
                notebooks_creados.append(notebook)
                print(f"✅ Notebook guardada en BD con ID: {notebook.id_not}")  # Debug
            
            # Limpiar datos de sesión
            if 'notebook_data' in request.session:
                del request.session['notebook_data']
            
            cantidad = len(notebooks_creados)
            # messages.success(request, f'Notebook(s) registrado(s) exitosamente: {cantidad} ejemplar(es)')
            return redirect('confirmacion_carga_exitosa')
            
        except Exception as e:
            print(f"❌ Error al guardar notebook: {str(e)}")  # Debug
            messages.error(request, f'Error al guardar el notebook: {str(e)}')
            return redirect('alta_materiales')
    else:
        messages.error(request, 'Método no permitido.')
        return redirect('alta_materiales')

def cancelar_alta_notebook(request):
    """
    Vista para cancelar el alta de notebook
    """
    # Limpiar datos de sesión si existen
    if 'notebook_data' in request.session:
        del request.session['notebook_data']
    
    messages.info(request, 'Se ha cancelado el registro del notebook.')
    return redirect('alta_materiales')

def cancelar_alta_notebook(request):
    """
    Vista para cancelar la alta y limpiar datos de sesión
    """
    print("🔴 Cancelando alta de notebook")  # Debug
    
    if 'notebook_data' in request.session:
        del request.session['notebook_data']
        print("🗑️ Datos de sesión eliminados")  # Debug
    
    messages.info(request, 'Operación cancelada.')
    return redirect('alta_materiales')

# Vistas para la confirmación de alta de proyector
def confirmacion_alta_proyector(request):
    """
    Vista para mostrar el modal de confirmación para proyector
    """
    print("🎯 Llegó a confirmacion_alta_proyector")  # Debug
    
    if request.method == 'POST':
        # Obtener cantidad de ejemplares
        cant_ejemplares = int(request.POST.get('cant_ejemplares', 1))
        
        # Mapeo de valores de sede
        sede_mapping = {
            'sede1': 'La Plata',
            'sede2': 'Abasto'
        }
        
        # Construir lista de ejemplares
        ejemplares = []
        for i in range(1, cant_ejemplares + 1):
            sede_value = request.POST.get('sede', '')
            sede_texto = sede_mapping.get(sede_value, sede_value)
            
            ejemplar = {
                'sede': sede_texto,  # Usar el nombre real de la sede
                'num_registro': request.POST.get(f'num_registro_{i}', ''),
                'modelo_pro': request.POST.get(f'modelo_pro_{i}', ''),
            }
            ejemplares.append(ejemplar)
        
        # Guardar los datos del formulario en la sesión
        sede_value = request.POST.get('sede', '')
        proyector_data = {
            'cant_ejemplares': cant_ejemplares,
            'sede': sede_value,
            'sede_texto': sede_mapping.get(sede_value, sede_value),  # Agregar el nombre legible de la sede
            'num_registro': request.POST.get('num_registro', ''),
            'modelo_pro': request.POST.get('modelo_pro', ''),
            'estado': 'Disponible',  # Valor por defecto
        }
        
        # Guardar en sesión
        request.session['proyector_data'] = proyector_data
        request.session['ejemplares_proyector'] = ejemplares
        print(f"📋 Datos guardados en sesión: {proyector_data}")  # Debug
        print(f"📋 Ejemplares: {ejemplares}")  # Debug
        
        # Renderizar página con modal automático
        return render(request, 'materiales/formularios_altas/confirmaciones_alta/confirmacion_alta_proyector.html', {
            'form_data': proyector_data,
            'ejemplares': ejemplares
        })
    else:
        # Si no es POST, redirigir al formulario
        messages.error(request, 'Método no permitido. Por favor, complete el formulario correctamente.')
        return redirect('alta_proyector')

# Vistas para la confirmación de alta de mapa
def confirmacion_alta_mapa(request):
    """
    Vista para mostrar el modal de confirmación para mapa
    """
    print("🎯 Llegó a confirmacion_alta_mapa")  # Debug
    
    if request.method == 'POST':
        # Obtener los datos básicos del formulario
        sede_value = request.POST.get('sede_mapa', '')
        
        # Convertir el valor de sede a texto legible
        sede_mapping = {
            'sede1': 'La Plata',
            'sede2': 'Abasto'
        }
        sede_texto = sede_mapping.get(sede_value, sede_value)
        
        print(f"📋 Datos POST recibidos: {dict(request.POST)}")  # Debug
        
        # CORREGIDO: Obtener los tipos de mapa desde gruposTiposMapa JSON
        tipos_mapa = []
        grupos_tipos_json = request.POST.get('gruposTiposMapa', '[]')
        
        # Obtener el tipo seleccionado del dropdown como fallback
        tipo_dropdown = request.POST.get('input-nuevo-tipo-mapa', 'GENERAL')
        
        print(f"🔍 gruposTiposMapa JSON recibido: '{grupos_tipos_json}'")  # Debug
        print(f"🔍 tipo_dropdown recibido: '{tipo_dropdown}'")  # Debug
        
        try:
            grupos_tipos_data = json.loads(grupos_tipos_json) if grupos_tipos_json else []
            print(f"📋 Grupos tipos data parseado: {grupos_tipos_data}")  # Debug
        except json.JSONDecodeError as e:
            grupos_tipos_data = []
            print(f"❌ Error al decodificar JSON de gruposTiposMapa: {e}")  # Debug
        
        # Crear un mapeo de índice de grupo a tipo
        tipo_por_grupo = {}
        for idx, grupo in enumerate(grupos_tipos_data):
            tipo_por_grupo[str(idx)] = grupo.get('tipo', tipo_dropdown)
        
        print(f"📋 Mapeo tipo por grupo: {tipo_por_grupo}")  # Debug
        
        # Procesar datos de ejemplares dinámicos
        for key, value in request.POST.items():
            if key.startswith('n_registro_'):
                # Extraer índice del campo (ej: "n_registro_0_1" -> "0_1")
                idx = key.replace('n_registro_', '')
                
                # Validar que el índice tenga el formato correcto
                if '_' not in idx:
                    continue
                    
                try:
                    grupo_idx, ejemplar_idx = idx.split('_')
                except ValueError:
                    continue
                
                # Buscar o crear el grupo de tipo
                grupo_encontrado = None
                for grupo in tipos_mapa:
                    if grupo['grupo_idx'] == grupo_idx:
                        grupo_encontrado = grupo
                        break
                
                if not grupo_encontrado:
                    # CORREGIDO: Obtener el tipo desde el mapeo creado
                    tipo_grupo = tipo_por_grupo.get(grupo_idx, tipo_dropdown)
                    
                    print(f"📋 Tipo para grupo {grupo_idx}: {tipo_grupo}")  # Debug
                    
                    grupo_encontrado = {
                        'grupo_idx': grupo_idx,
                        'tipo': tipo_grupo,
                        'ejemplares': []
                    }
                    tipos_mapa.append(grupo_encontrado)
                
                # Agregar ejemplar al grupo
                ejemplar = {
                    'idx': idx,
                    'n_registro': value,
                    'denominacion': request.POST.get(f'denominacion_{idx}', ''),
                    'descripcion': request.POST.get(f'descripcion_{idx}', '')
                }
                grupo_encontrado['ejemplares'].append(ejemplar)
        
        # Si no se encontraron ejemplares dinámicos, crear uno básico usando los datos de gruposTiposMapa
        if not tipos_mapa and grupos_tipos_data:
            print(f"🔧 Creando tipos_mapa desde grupos_tipos_data")  # Debug
            # Usar los datos de gruposTiposMapa para crear los tipos
            for idx, grupo in enumerate(grupos_tipos_data):
                tipo_grupo = grupo.get('tipo', tipo_dropdown)
                cantidad_grupo = grupo.get('cantidad', 1)
                
                print(f"🔧 Procesando grupo {idx}: tipo='{tipo_grupo}', cantidad={cantidad_grupo}")  # Debug
                
                # Crear ejemplares para este tipo
                ejemplares = []
                for ej_idx in range(cantidad_grupo):
                    ejemplares.append({
                        'idx': f'{idx}_{ej_idx}',
                        'n_registro': request.POST.get('num_registro', ''),
                        'denominacion': f'Mapa {tipo_grupo}',
                        'descripcion': ''
                    })
                
                tipos_mapa.append({
                    'grupo_idx': str(idx),
                    'tipo': tipo_grupo,
                    'ejemplares': ejemplares
                })
        elif not tipos_mapa:
            # Fallback si no hay datos de gruposTiposMapa
            tipo_basico = request.POST.get('input-nuevo-tipo-mapa', tipo_dropdown)
            cantidad_basica = int(request.POST.get('input-nueva-cant-mapa', 1))
            
            tipos_mapa.append({
                'grupo_idx': '0',
                'tipo': tipo_basico,
                'ejemplares': [{
                    'idx': '0_0',
                    'n_registro': request.POST.get('num_registro', ''),
                    'denominacion': f'Mapa {tipo_basico}',
                    'descripcion': ''
                }]
            })
        
        # Calcular cantidad por tipo y obtener el primer n_registro
        primer_n_registro = ""
        for grupo in tipos_mapa:
            grupo['cantidad'] = len(grupo['ejemplares'])
            # Obtener el primer n_registro si no lo tenemos aún
            if grupo['ejemplares'] and not primer_n_registro:
                primer_n_registro = grupo['ejemplares'][0]['n_registro']
        
        # Guardar los datos en la sesión
        mapa_data = {
            'sede': sede_value,  # Guardamos el valor original para el procesamiento
            'sede_texto': sede_texto,  # Guardamos el texto para mostrar
            'n_registro': primer_n_registro,
            'tipos_mapa': tipos_mapa
        }
        
        # Guardar en sesión
        request.session['mapa_data'] = mapa_data
        print(f"📋 Datos de mapa guardados en sesión: {mapa_data}")  # Debug
        print(f"🎯 tipos_mapa final enviado al template: {tipos_mapa}")  # Debug
        
        # Renderizar la página de confirmación con los datos procesados
        return render(request, 'materiales/formularios_altas/confirmaciones_alta/confirmacion_alta_mapa.html', {
            'mapa_data': mapa_data,
            'tipos_mapa': tipos_mapa,
            'form_data': {
                'sede_texto': sede_texto
            }
        })
    else:
        # Si no es POST, redirigir al formulario
        messages.error(request, 'Método no permitido. Por favor, complete el formulario correctamente.')
        return redirect('alta_materiales')

def confirmar_mapa_final(request):
    """
    Vista para procesar la confirmación final del mapa desde el modal
    """
    print("🎯 Llegó a confirmar_mapa_final")  # Debug
    
    if request.method == 'POST':
        try:
            # Obtener la sede del formulario
            sede = request.POST.get('sede', 'LA PLATA')
            print(f"📍 Sede recibida: {sede}")
            
            # Obtener los datos de los ejemplares del formulario
            ejemplares_data = []
            index = 0
            
            # Extraer datos de ejemplares del POST
            while f'ejemplares[{index}][n_registro]' in request.POST:
                ejemplar = {
                    'n_registro': request.POST.get(f'ejemplares[{index}][n_registro]', ''),
                    'denominacion': request.POST.get(f'ejemplares[{index}][denominacion]', ''),
                    'descripcion': request.POST.get(f'ejemplares[{index}][descripcion]', ''),
                    'tipo': request.POST.get(f'ejemplares[{index}][tipo]', 'GENERAL')
                }
                ejemplares_data.append(ejemplar)
                print(f"📝 Ejemplar {index + 1}: {ejemplar}")
                index += 1
            
            # Si no hay ejemplares en el formato esperado, intentar obtener de la sesión
            if not ejemplares_data and 'mapa_data' in request.session:
                mapa_data = request.session.get('mapa_data', {})
                tipos_mapa = mapa_data.get('tipos_mapa', [])
                
                for tipo_grupo in tipos_mapa:
                    tipo = tipo_grupo.get('tipo', 'GENERAL')
                    ejemplares = tipo_grupo.get('ejemplares', [])
                    
                    for ejemplar in ejemplares:
                        ejemplar_data = {
                            'n_registro': ejemplar.get('n_registro', ''),
                            'denominacion': ejemplar.get('denominacion', ''),
                            'descripcion': ejemplar.get('descripcion', ''),
                            'tipo': tipo
                        }
                        ejemplares_data.append(ejemplar_data)
                        print(f"📝 Ejemplar de sesión: {ejemplar_data}")
            
            # Guardar cada ejemplar en la base de datos
            mapas_creados = []
            for ejemplar in ejemplares_data:
                # Crear el registro en la tabla Mapas con el mapeo correcto
                mapa = Mapas.objects.create(
                    # Campos heredados de Inventario
                    estado='Disponible',
                    descripcion=ejemplar.get('descripcion', ''),  # descripcion -> descripcion
                    num_ejemplar=1,
                    # Campos específicos de Mapas
                    sede=sede,                                    # sede -> sede
                    tipo=ejemplar.get('tipo', 'GENERAL'),        # tipo -> tipo
                    num_registro=ejemplar.get('n_registro', ''), # n_registro -> num_registro
                    denominacion=ejemplar.get('denominacion', '') # denominacion -> denominacion
                )
                mapas_creados.append(mapa)
                print(f"✅ Mapa guardado: ID={mapa.id_mapa}, Sede={mapa.sede}, Tipo={mapa.tipo}, Registro={mapa.num_registro}, Denominación={mapa.denominacion}")
            
            # Limpiar datos de sesión
            if 'mapa_data' in request.session:
                del request.session['mapa_data']
                print("🧹 Datos de sesión limpiados")
            
            # Mensaje de éxito
            cantidad_total = len(mapas_creados)
            # messages.success(request, f'✅ Se han registrado exitosamente {cantidad_total} mapa(s) en la base de datos.')
            return redirect('confirmacion_carga_exitosa')
            
        except Exception as e:
            print(f"❌ Error al guardar mapas: {str(e)}")
            messages.error(request, f'Error al guardar los mapas: {str(e)}')
            return redirect('confirmacion_carga_exitosa')
    else:
        # Si no es POST, redirigir al formulario
        messages.error(request, 'Método no permitido.')
        return redirect('confirmacion_carga_exitosa')

def guardar_alta_mapa(request):
    """
    Vista para guardar el mapa confirmado en la base de datos
    """
    print("🎯 Llegó a guardar_alta_mapa")  # Debug
    
    if request.method != 'POST':
        print("❌ Método no permitido: " + request.method)  # Debug
        messages.error(request, 'Método no permitido.')
        return redirect('alta_materiales')
    
    # Verificar que existan datos en la sesión
    if 'mapa_data' not in request.session:
        print("❌ No hay datos de mapa en la sesión")  # Debug
        messages.error(request, 'No se encontraron datos para guardar. Por favor, complete el formulario nuevamente.')
        return redirect('alta_materiales')
    
    try:
        # Recuperar datos de la sesión
        mapa_data = request.session.get('mapa_data', {})
        tipos_mapa = mapa_data.get('tipos_mapa', [])
        
        print(f"📋 Procesando datos: {mapa_data}")  # Debug
        
        # CORREGIDO: Mapear correctamente el valor de sede
        sede_value = mapa_data.get('sede', '')
        sede_mapping = {
            'sede1': 'La Plata',
            'sede2': 'Abasto'
        }
        sede_final = sede_mapping.get(sede_value, sede_value)
        print(f"📋 Sede original: {sede_value}, Sede final: {sede_final}")  # Debug
        
        if tipos_mapa:
            # Crear registros individuales para cada ejemplar
            mapas_creados = []
            
            for tipo_grupo in tipos_mapa:
                tipo = tipo_grupo.get('tipo', 'GENERAL')
                ejemplares = tipo_grupo.get('ejemplares', [])
                
                for ejemplar in ejemplares:
                    # CORREGIDO: Solo usar campos que existen en el modelo Mapas
                    mapa = Mapas.objects.create(
                        # Campos heredados de Inventario
                        estado='Disponible',
                        descripcion=ejemplar.get('descripcion', ''),  # Usar el campo heredado
                        num_ejemplar=1,  # Campo heredado
                        # Campos específicos de Mapas
                        sede=sede_final,  # CORREGIDO: Usar el valor mapeado
                        num_registro=ejemplar.get('n_registro', ''),
                        denominacion=ejemplar.get('denominacion', f'Mapa {tipo}'),
                        tipo=tipo
                    )
                    mapas_creados.append(mapa)
                    print(f"✅ Mapa creado: {mapa.num_registro} - {mapa.denominacion} - Sede: {mapa.sede}")
            
            # Mensaje de éxito
            cantidad_total = len(mapas_creados)
            # messages.success(request, f'Se han registrado exitosamente {cantidad_total} mapa(s).')
            
        else:
            # Fallback: crear un registro simple si no hay tipos específicos
            mapa = Mapas.objects.create(
                # Campos heredados de Inventario
                estado='Disponible',
                num_ejemplar=1,
                # Campos específicos de Mapas
                sede=sede_final,  # CORREGIDO: Usar el valor mapeado
                num_registro=mapa_data.get('n_registro', ''),
                denominacion='Mapa General',
                tipo='GENERAL'
            )
            # messages.success(request, 'Mapa registrado exitosamente.')
            print(f"✅ Mapa simple creado: {mapa.num_registro} - Sede: {mapa.sede}")
        
        # Limpiar datos de sesión
        if 'mapa_data' in request.session:
            del request.session['mapa_data']
            print("🧹 Datos de sesión limpiados")
        
        # CORREGIDO: Redirigir a una URL válida
        return redirect('confirmacion_carga_exitosa')
        
    except Exception as e:
        print(f"❌ Error al guardar mapa: {str(e)}")  # Debug
        messages.error(request, f'Error al guardar el mapa: {str(e)}')
        return redirect('alta_materiales')

def guardar_alta_proyector(request):
    """
    Vista para guardar definitivamente después de confirmar en el modal
    """
    print("💾 Guardando proyector confirmado")  # Debug
    
    if request.method == 'POST':
        # Recuperar datos de la sesión como base
        proyector_data = request.session.get('proyector_data', {})
        ejemplares_originales = request.session.get('ejemplares_proyector', [])
        
        if not proyector_data:
            messages.error(request, 'No se encontraron datos del proyector en la sesión.')
            return redirect('alta_materiales')
        
        try:
            # NUEVO: Procesar datos editados del modal si existen
            sede_editada = request.POST.get('sede')
            
            # Crear lista de ejemplares actualizada
            ejemplares_actualizados = []
            
            if ejemplares_originales:
                # Si hay ejemplares múltiples, procesarlos
                for i, ejemplar_original in enumerate(ejemplares_originales):
                    # Buscar datos editados para este ejemplar
                    num_registro_editado = request.POST.get(f'ejemplares[{i}][num_registro]')
                    modelo_editado = request.POST.get(f'ejemplares[{i}][modelo_pro]')
                    
                    # Crear ejemplar actualizado con datos editados o originales
                    ejemplar_actualizado = {
                        'sede': sede_editada if sede_editada else ejemplar_original.get('sede'),
                        'num_registro': num_registro_editado if num_registro_editado else ejemplar_original.get('num_registro'),
                        'modelo_pro': modelo_editado if modelo_editado else ejemplar_original.get('modelo_pro'),
                    }
                    ejemplares_actualizados.append(ejemplar_actualizado)
                    
                    print(f"📝 Ejemplar {i+1} actualizado: {ejemplar_actualizado}")  # Debug
            else:
                # Si no hay ejemplares múltiples, usar datos generales
                ejemplar_unico = {
                    'sede': sede_editada if sede_editada else proyector_data.get('sede_texto'),
                    'num_registro': request.POST.get('ejemplares[0][num_registro]') or proyector_data.get('num_registro'),
                    'modelo_pro': request.POST.get('ejemplares[0][modelo_pro]') or proyector_data.get('modelo_pro'),
                }
                ejemplares_actualizados.append(ejemplar_unico)
                print(f"📝 Ejemplar único actualizado: {ejemplar_unico}")  # Debug
            
            # Crear múltiples proyectores con los datos actualizados
            proyectores_creados = []
            
            for i, ejemplar in enumerate(ejemplares_actualizados):
                # Crear el proyector para este ejemplar
                proyector = Proyector.objects.create(
                    num_registro=ejemplar.get('num_registro'),
                    modelo_pro=ejemplar.get('modelo_pro'),
                    sede=ejemplar.get('sede'),
                    estado=proyector_data.get('estado', 'Disponible')
                )
                proyectores_creados.append(proyector)
                print(f"✅ Proyector {i+1} creado con éxito: {proyector}")
                
            print(f"✅ Total de proyectores creados: {len(proyectores_creados)}")  # Debug
            
            # Limpiar datos de sesión
            if 'proyector_data' in request.session:
                del request.session['proyector_data']
            if 'ejemplares_proyector' in request.session:
                del request.session['ejemplares_proyector']
            
            # messages.success(request, f'Se han guardado {len(proyectores_creados)} proyector(es) correctamente.')
            return redirect('confirmacion_carga_exitosa')
            
        except Exception as e:
            print(f"❌ Error al guardar proyector: {str(e)}")  # Debug
            messages.error(request, f'Error al guardar el proyector: {str(e)}')
            return redirect('alta_materiales')
    else:
        messages.error(request, 'Método no permitido.')
        return redirect('alta_materiales')

def cancelar_alta_proyector(request):
    """
    Vista para cancelar el alta de proyector
    """
    # Limpiar datos de sesión si existen
    if 'proyector_data' in request.session:
        del request.session['proyector_data']
    
    messages.info(request, 'Se ha cancelado el registro del proyector.')
    return redirect('alta_materiales')

def cancelar_alta_mapa(request):
    """
    Vista para cancelar el alta de mapa
    """
    # Limpiar datos de sesión si existen
    if 'mapa_data' in request.session:
        del request.session['mapa_data']
    
    messages.info(request, 'Se ha cancelado el registro del mapa.')
    return redirect('alta_materiales')

def editar_programa(request, programa_id):
    """
    Vista para editar un programa existente
    """
    programa = get_object_or_404(Programa, id_programa=programa_id)
    
    if request.method == 'POST':
        print(f"🔍 [DEBUG] POST data recibida: {dict(request.POST)}")
        
        # Crear una copia mutable de POST data
        post_data = request.POST.copy()
        
        # Verificar y corregir campos vacíos requeridos
        if not post_data.get('carrera'):
            post_data['carrera'] = 'No especificado'
            print(f"⚠️ [DEBUG] Campo 'carrera' vacío, asignando valor por defecto")
            
        if not post_data.get('materia'):
            post_data['materia'] = 'No especificado'
            print(f"⚠️ [DEBUG] Campo 'materia' vacío, asignando valor por defecto")
            
        if not post_data.get('profesor'):
            post_data['profesor'] = 'No especificado'
            print(f"⚠️ [DEBUG] Campo 'profesor' vacío, asignando valor por defecto")
            
        if not post_data.get('ciclo_lectivo'):
            post_data['ciclo_lectivo'] = '2024'
            print(f"⚠️ [DEBUG] Campo 'ciclo_lectivo' vacío, asignando valor por defecto")
        
        print(f"🔧 [DEBUG] POST data después de correcciones: {dict(post_data)}")
        
        # Crear el formulario con los datos corregidos
        form = ProgramaForm(post_data, instance=programa)
        
        print(f"📋 [DEBUG] Formulario válido: {form.is_valid()}")
        if not form.is_valid():
            print(f"❌ [DEBUG] Errores del formulario: {form.errors}")
            print(f"❌ [DEBUG] Errores no de campo: {form.non_field_errors()}")
        
        if form.is_valid():
            try:
                print(f"💾 [DEBUG] Programa antes de guardar:")
                print(f"    - ID: {programa.id_programa}")
                print(f"    - Carrera: {programa.carrera}")
                print(f"    - Materia: {programa.materia}")
                print(f"    - Profesor: {programa.profesor}")
                print(f"    - Ciclo Lectivo: {programa.ciclo_lectivo}")
                print(f"    - Enlace: {programa.ingresar_enlace}")
                
                programa_guardado = form.save()
                
                print(f"✅ [DEBUG] Programa después de guardar:")
                print(f"    - ID: {programa_guardado.id_programa}")
                print(f"    - Carrera: {programa_guardado.carrera}")
                print(f"    - Materia: {programa_guardado.materia}")
                print(f"    - Profesor: {programa_guardado.profesor}")
                print(f"    - Ciclo Lectivo: {programa_guardado.ciclo_lectivo}")
                print(f"    - Enlace: {programa_guardado.ingresar_enlace}")
                
                messages.success(request, 'Programa editado exitosamente.')
                return redirect('modificacion_materiales')
                
            except Exception as e:
                print(f"💥 [ERROR] Error al guardar programa: {str(e)}")
                messages.error(request, f'Error al guardar el programa: {str(e)}')
        else:
            messages.error(request, 'Error al editar el programa. Verifique los datos.')
    else:
        form = ProgramaForm(instance=programa)
    
    return render(request, 'materiales/formularios_editar/editar_programa.html', {
        'form': form,
        'programa': programa
    })

def actualizar_sesion_varios(request):
    """
    Vista AJAX para actualizar la sesión con datos editados de varios
    """
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            import json
            
            # Obtener datos del POST
            data = json.loads(request.body)
            print(f"🔄 Datos recibidos para actualizar sesión: {data}")
            
            # Verificar que existan datos de varios en la sesión
            if 'varios_data' not in request.session:
                return JsonResponse({'success': False, 'error': 'No hay datos de varios en la sesión'})
            
            # Obtener datos actuales de la sesión
            varios_data = request.session['varios_data']
            
            # Actualizar los datos con los valores editados
            if 'sede' in data:
                sede_mapping = {
                    'sede1': 'La Plata',
                    'sede2': 'Abasto'
                }
                varios_data['sede_texto'] = sede_mapping.get(data['sede'], data['sede'])
                varios_data['sede_varios'] = data['sede']
            
            if 'tipo_registrar' in data:
                varios_data['tipo_varios'] = data['tipo_registrar']
            
            if 'cantidad_ejemplares' in data:
                varios_data['cant_ejemplares'] = data['cantidad_ejemplares']
            
            # Actualizar materiales dinámicos
            if 'materiales' in data and data['materiales']:
                tipos_varios_actualizados = []
                for material in data['materiales']:
                    # Crear ejemplares para cada material
                    ejemplares = []
                    cantidad = int(material.get('cantidad', 1))
                    for i in range(cantidad):
                        ejemplares.append({
                            'registro': '',
                            'denominacion': '',
                            'descripcion': '',
                            'sede': varios_data['sede_texto'],
                            'disponibilidad': 'Disponible'
                        })
                    
                    tipos_varios_actualizados.append({
                        'tipo': material['tipo'],
                        'ejemplares': ejemplares
                    })
                
                varios_data['tipos_varios'] = tipos_varios_actualizados
            
            # Guardar los datos actualizados en la sesión
            request.session['varios_data'] = varios_data
            request.session.modified = True
            
            print(f"✅ Sesión actualizada con: {varios_data}")
            
            return JsonResponse({'success': True, 'message': 'Sesión actualizada correctamente'})
            
        except Exception as e:
            print(f"❌ Error al actualizar sesión: {str(e)}")
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@login_required
def confirmacion_carga_exitosa(request):
    """
    Vista para mostrar la pantalla de confirmación de carga exitosa.
    Esta vista se muestra después de que se haya guardado exitosamente cualquier material.
    """
    return render(request, 'materiales/formularios_altas/confirmaciones_alta/confirmacion_carga_exitosa.html')


# ===== FUNCIONES DE EDICIÓN Y BAJA MEJORADAS DESDE SEBA =====

def editar_libro_mejorado(request, libro_id):
    """Función de edición de libro mejorada desde seba"""
    libro = get_object_or_404(Libro, id_libro=libro_id)
    
    if request.method == 'POST':
        print(f"🔥 POST recibido para editar libro ID: {libro_id}")
        print(f"🔥 Datos POST: {dict(request.POST)}")
        
        # Crear una copia mutable de POST para modificar
        post_data = request.POST.copy()
        
        # ARREGLAR: Manejar URL de imagen ANTES de crear el formulario
        url_input = post_data.get('url_input', '').strip()
        if url_input and not request.FILES.get('img'):
            print(f"🔗 Procesando URL de imagen: {url_input}")
            # Si hay URL pero no archivo, guardar la URL directamente en el libro
            libro.img = url_input
            # Remover el campo img del formulario para que no sea requerido
            post_data['img'] = url_input
        
        # ARREGLAR: Verificar campos requeridos vacíos
        if not post_data.get('sede'):
            print("⚠️ Sede vacía, usando valor actual del libro")
            post_data['sede'] = libro.sede or 'CENTRAL'  # Valor por defecto
            
        if not post_data.get('disponibilidad'):
            print("⚠️ Disponibilidad vacía, usando valor actual del libro")
            post_data['disponibilidad'] = libro.disponibilidad or 'DOMICILIO'  # Valor por defecto
        
        print(f"🔧 Datos POST corregidos: {dict(post_data)}")
        
        # Crear formulario con datos corregidos
        form = LibroForm(post_data, request.FILES, instance=libro)
        
        if form.is_valid():
            print("✅ Formulario válido - guardando...")
            
            try:
                # Guardar el formulario
                libro_actualizado = form.save()
                
                # Si había URL de imagen, asegurar que se guarde
                if url_input and not request.FILES.get('img'):
                    libro_actualizado.img = url_input
                    libro_actualizado.save()
                
                print(f"✅ Libro actualizado: {libro_actualizado.titulo}")
                print(f"📋 Imagen final: {libro_actualizado.img}")
                
                # messages.success(request, f'✅ Libro "{libro_actualizado.titulo}" actualizado exitosamente.')
                return redirect('modificacion_materiales')
                
            except Exception as e:
                print(f"❌ Error al guardar: {e}")
                import traceback
                traceback.print_exc()
                messages.error(request, f'❌ Error al actualizar el libro: {str(e)}')
        else:
            print(f"❌ Formulario TODAVÍA inválido!")
            print(f"❌ Errores: {form.errors}")
            
            # Mostrar errores específicos
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error en {field}: {error}')
                    print(f"❌ Error en {field}: {error}")
    else:
        form = LibroForm(instance=libro)
    
    return render(request, 'materiales/formularios_editar/editar_libro.html', {
        'form': form, 
        'libro': libro
    })


def baja_libro_mejorada(request):
    """Función de baja de libro mejorada"""
    if request.method == 'POST':
        libro_id = request.POST.get('libro_id')
        motivo_baja = request.POST.get('motivo_baja')
        imagen_rota = request.FILES.get('imagen_rota')

        # Obtener el libro
        libro = get_object_or_404(Libro, id_libro=libro_id)
        
        # Cambiar estado
        libro.estado = 'No disponible'
        libro.motivo_baja = motivo_baja
        
        # Guardar la fecha real de baja
        try:
            from django.utils import timezone
            libro.fecha_baja = timezone.now()
        except Exception:
            pass
        
        # Guardar imagen en el campo imagen_rota del modelo
        if imagen_rota:
            libro.imagen_rota = imagen_rota
        
        libro.save()

        return redirect('modificacion_materiales')

    return redirect('modificacion_materiales')


def baja_mapa_mejorada(request):
    """Función de baja de mapa mejorada desde seba"""
    if request.method == 'POST':
        mapa_id = request.POST.get('mapa_id')
        motivo_baja = request.POST.get('motivo_baja')
        imagen_rota = request.FILES.get('imagen_rota')

        # Obtener el mapa
        mapa = get_object_or_404(Mapas, id_mapa=mapa_id)
        
        # Cambiar estado
        mapa.estado = 'No disponible'
        mapa.motivo_baja = motivo_baja
        # Guardar la fecha real de baja
        try:
            from django.utils import timezone
            mapa.fecha_baja = timezone.now()
        except Exception:
            pass
        
        # Guardar imagen en el campo imagen_rota del modelo
        if imagen_rota:
            mapa.imagen_rota = imagen_rota
        
        mapa.save()

        # messages.success(request, f'Mapa "{mapa.tipo}" dado de baja exitosamente.')
        return redirect('modificacion_materiales')

    return redirect('modificacion_materiales')


def editar_mapa_mejorado(request, mapa_id):
    """Función de edición de mapa mejorada desde seba"""
    mapa = get_object_or_404(Mapas, id_mapa=mapa_id)

    if request.method == 'POST':
        form = MapaForm(request.POST, instance=mapa)
        if form.is_valid():
            form.save()
            return redirect('modificacion_materiales')
    else:
        form = MapaForm(instance=mapa)

    return render(request, 'materiales/formularios_editar/editar_mapa.html', {'form': form, 'mapa': mapa})


def baja_multimedia_mejorada(request):
    """Función de baja de multimedia mejorada desde seba"""
    if request.method == 'POST':
        multi_id = request.POST.get('id_inventario')
        motivo_baja = request.POST.get('motivo_baja')
        imagen_rota = request.FILES.get('imagen_rota')

        # Lógica para actualizar el estado del multimedia
        multimedia = get_object_or_404(Multimedia, id_inventario=multi_id)
        multimedia.estado = 'No disponible'
        multimedia.motivo_baja = motivo_baja
        multimedia.fecha_baja = timezone.now()  # Guardar la fecha actual de baja
        if imagen_rota:
            multimedia.imagen_rota = imagen_rota
        multimedia.save()

        # messages.success(request, f'Multimedia "{multimedia.titulo_contenido}" dado de baja correctamente.')
        return redirect('modificacion_materiales')

    return redirect('modificacion_materiales')


def editar_multimedia_mejorado(request, multi_id):
    """Función de edición de multimedia mejorada desde seba"""
    multimedia = get_object_or_404(Multimedia, id_multi=multi_id)

    if request.method == 'POST':
        form = MultimediaForm(request.POST, instance=multimedia)
        if form.is_valid():
            form.save()
            return redirect('modificacion_materiales')
    else:
        form = MultimediaForm(instance=multimedia)

    return render(request, 'materiales/formularios_editar/editar_multimedia.html', {'form': form, 'multimedia': multimedia})


def baja_notebook_mejorada(request):
    """Función de baja de notebook mejorada desde seba"""
    if request.method == 'POST':
        not_id = request.POST.get('not_id')
        motivo_baja = request.POST.get('motivo_baja')
        imagen_rota = request.FILES.get('imagen_rota')

        # Lógica para actualizar el estado del notebook
        notebook = get_object_or_404(Notebook, id_not=not_id)
        notebook.estado = 'No disponible'
        notebook.motivo_baja = motivo_baja
        notebook.fecha_baja = timezone.now()
        if imagen_rota:
            notebook.imagen_rota = imagen_rota
        notebook.save()

        return redirect('modificacion_materiales')

    return redirect('modificacion_materiales')


def editar_notebook_mejorado(request, not_id):
    """Función de edición de notebook mejorada desde seba"""
    notebook = get_object_or_404(Notebook, id_not=not_id)

    if request.method == 'POST':
        form = NotebookForm(request.POST, instance=notebook)
        if form.is_valid():
            form.save()
            return redirect('modificacion_materiales')
    else:
        form = NotebookForm(instance=notebook)

    return render(request, 'materiales/formularios_editar/editar_notebook.html', {'form': form, 'notebook': notebook})


def baja_proyector_mejorada(request):
    """Función de baja de proyector mejorada desde seba"""
    if request.method == 'POST':
        proyector_id = request.POST.get('proyector_id')
        motivo_baja = request.POST.get('motivo_baja')
        imagen_rota = request.FILES.get('imagen_rota')

        # Lógica para actualizar el estado del proyector
        proyector = get_object_or_404(Proyector, id_proyector=proyector_id)
        proyector.estado = 'No disponible'
        proyector.motivo_baja = motivo_baja
        proyector.fecha_baja = timezone.now()
        if imagen_rota:
            proyector.imagen_rota = imagen_rota
        proyector.save()

        return redirect('modificacion_materiales')

    return redirect('modificacion_materiales')


def editar_proyector_mejorado(request, proyector_id):
    """Función de edición de proyector mejorada desde seba"""
    proyector = get_object_or_404(Proyector, id_proyector=proyector_id)

    if request.method == 'POST':
        form = ProyectorForm(request.POST, instance=proyector)
        if form.is_valid():
            form.save()
            return redirect('modificacion_materiales')
    else:
        form = ProyectorForm(instance=proyector)

    return render(request, 'materiales/formularios_editar/editar_proyector.html', {'form': form, 'proyector': proyector})


def baja_varios_mejorada(request):
    """Función de baja de varios mejorada desde seba"""
    if request.method == 'POST':
        varios_id = request.POST.get('varios_id')
        motivo_baja = request.POST.get('motivo_baja')
        imagen_rota = request.FILES.get('imagen_rota')

        # Obtener el objeto varios
        varios = get_object_or_404(Varios, id_varios=varios_id)
        
        # Cambiar estado
        varios.estado = 'No disponible'
        varios.motivo_baja = motivo_baja
        # Guardar fecha de baja real
        varios.fecha_baja = timezone.now()
        
        # IMPORTANTE: Guardar imagen en el campo imagen_rota del modelo
        if imagen_rota:
            varios.imagen_rota = imagen_rota
        
        varios.save()

        # messages.success(request, f'Varios "{varios.tipo}" dado de baja exitosamente.')
        return redirect('modificacion_materiales')

    return redirect('modificacion_materiales')


def editar_varios_mejorado(request, varios_id):
    """Función de edición de varios mejorada desde seba"""
    varios = get_object_or_404(Varios, id_varios=varios_id)

    if request.method == 'POST':
        form = VariosForm(request.POST, instance=varios)
        if form.is_valid():
            form.save()
            return redirect('modificacion_materiales')
    else:
        form = VariosForm(instance=varios)

    return render(request, 'materiales/formularios_editar/editar_varios.html', {'form': form, 'varios': varios})


def baja_programa_mejorada(request):
    """Función de baja de programa mejorada desde seba"""
    if request.method == 'POST':
        programa_id = request.POST.get('programa_id')
        motivo_baja = request.POST.get('motivo_baja')
        imagen_rota = request.FILES.get('imagen_rota')

        # Lógica para actualizar el estado del programa
        programa = get_object_or_404(Programa, id_programa=programa_id)
        programa.estado = 'No disponible'
        programa.motivo_baja = motivo_baja
        programa.fecha_baja = timezone.now()
        if imagen_rota:
            programa.imagen_rota = imagen_rota
        programa.save()

        return redirect('modificacion_materiales')

    return redirect('modificacion_materiales')


def editar_programa_mejorado(request, programa_id):
    """Función de edición de programa mejorada desde seba"""
    programa = get_object_or_404(Programa, id_programa=programa_id)
    
    if request.method == 'POST':
        form = ProgramaForm(request.POST, instance=programa)
        if form.is_valid():
            form.save()
            # messages.success(request, f'Programa "{programa.nombre}" actualizado correctamente.')
            return redirect('modificacion_materiales')
    else:
        form = ProgramaForm(instance=programa)
    
    return render(request, 'materiales/formularios_editar/editar_programa.html', {
        'form': form,
        'programa': programa
    })


# ===== FUNCIONES DE REACTIVACIÓN MEJORADAS =====

def reactivar_multimedia_mejorado(request, multimedia_id):
    """Función de reactivación de multimedia mejorada desde seba"""
    if request.method == 'POST':
        multimedia = get_object_or_404(Multimedia, id_inventario=multimedia_id)
        multimedia.estado = 'Disponible'
        multimedia.motivo_baja = ''  # Opcional: limpiar el motivo de baja
        multimedia.fecha_baja = None
        multimedia.save()
        # messages.success(request, f'El multimedia "{multimedia.titulo_contenido}" ha sido reactivado exitosamente.')
        return redirect('registro_de_bajas_multimedia')
    return redirect('registro_de_bajas_multimedia')


def reactivar_notebook_mejorado(request, notebook_id):
    """Función de reactivación de notebook mejorada desde seba"""
    if request.method == 'POST':
        notebook = get_object_or_404(Notebook, id_not=notebook_id)
        notebook.estado = 'Disponible'
        notebook.motivo_baja = ''  # Opcional: limpiar el motivo de baja
        notebook.fecha_baja = None
        notebook.save()
        # messages.success(request, f'El notebook "{notebook.modelo_not}" ha sido reactivado exitosamente.')
        return redirect('modificacion_materiales')
    return redirect('modificacion_materiales')


def reactivar_proyector_mejorado(request, proyector_id):
    """Función de reactivación de proyector mejorada desde seba"""
    if request.method == 'POST':
        proyector = get_object_or_404(Proyector, id_proyector=proyector_id)
        proyector.estado = 'Disponible'
        proyector.motivo_baja = ''
        proyector.fecha_baja = None
        proyector.save()
        return redirect('modificacion_materiales')
    return redirect('modificacion_materiales')


def reactivar_varios_mejorado(request, varios_id):
    """Función de reactivación de varios mejorada desde seba"""
    if request.method == 'POST':
        varios = get_object_or_404(Varios, id_varios=varios_id)
        varios.estado = 'Disponible'
        varios.motivo_baja = ''
        varios.fecha_baja = None
        varios.save()
        return redirect('modificacion_materiales')
    return redirect('modificacion_materiales')


def reactivar_mapa_mejorado(request, mapa_id):
    """Función de reactivación de mapa mejorada desde seba"""
    if request.method == 'POST':
        mapa = get_object_or_404(Mapas, id_mapa=mapa_id)
        mapa.estado = 'Disponible'
        mapa.motivo_baja = ''
        mapa.fecha_baja = None
        mapa.save()
        return redirect('modificacion_materiales')
    return redirect('modificacion_materiales')


def reactivar_programa_mejorado(request, programa_id):
    """Función de reactivación de programa mejorada desde seba"""
    if request.method == 'POST':
        programa = get_object_or_404(Programa, id_programa=programa_id)
        programa.estado = 'Disponible'
        programa.motivo_baja = ''
        programa.fecha_baja = None
        programa.save()
        return redirect('modificacion_materiales')
    return redirect('modificacion_materiales')


# ===== FUNCIONES DE REGISTRO DE BAJAS =====

def registro_bajas_multimedia(request):
    """Vista para mostrar el registro de multimedia dados de baja"""
    multimedia_no_disponible = Multimedia.objects.filter(estado='No disponible')
    return render(request, 'materiales/registros/registro_bajas_multimedia.html', {
        'multimedia_no_disponible': multimedia_no_disponible
    })


def registro_bajas_notebook(request):
    """Vista para mostrar el registro de notebooks dados de baja"""
    notebooks_no_disponible = Notebook.objects.filter(estado='No disponible').order_by('-id_not')
    return render(request, 'materiales/registro_bajas_notebook.html', {
        'notebooks': notebooks_no_disponible
    })


def registro_bajas_programa(request):
    """Vista para mostrar el registro de programas dados de baja"""
    programas_no_disponible = Programa.objects.filter(estado='No disponible').order_by('-id_programa')
    return render(request, 'materiales/registro_bajas_programa.html', {
        'programas': programas_no_disponible
    })


def registro_bajas_mapas(request):
    """Vista para mostrar el registro de mapas dados de baja"""
    mapas_no_disponible = Mapas.objects.filter(estado='No disponible').order_by('-id_mapa')
    return render(request, 'materiales/registro_bajas_mapas.html', {
        'mapas': mapas_no_disponible
    })


def registro_bajas_proyectores(request):
    """Vista para mostrar el registro de proyectores dados de baja"""
    proyectores_no_disponible = Proyector.objects.filter(estado='No disponible').order_by('-id_proyector')
    return render(request, 'materiales/registro_bajas_proyectores.html', {
        'proyectores': proyectores_no_disponible
    })


def registro_bajas_varios_mejorado(request):
    """Vista para mostrar el registro de varios dados de baja"""
    varios_no_disponible = Varios.objects.filter(estado='No disponible').order_by('-id_varios')
    return render(request, 'materiales/registro_bajas_varios.html', {
        'varios': varios_no_disponible
    })


# ===== FUNCIONES FALTANTES DESDE SEBA =====

def baja_programa(request):
    """
    Vista para dar de baja un programa
    """
    if request.method == 'POST':
        programa_id = request.POST.get('programa_id')
        motivo_baja = request.POST.get('motivo_baja')
        imagen_rota = request.FILES.get('imagen_rota')

        # Lógica para actualizar el estado del programa
        programa = get_object_or_404(Programa, id_programa=programa_id)
        programa.estado = 'No disponible'
        programa.motivo_baja = motivo_baja
        if imagen_rota:
            programa.imagen_rota = imagen_rota
        programa.save()

        return redirect('modificacion_materiales')

    return redirect('modificacion_materiales')


@login_required
@require_POST
def dar_alta_programa(request):
    """
    Vista para reactivar un programa (cambiar estado a Disponible)
    """
    try:
        programa_id = request.POST.get('programa_id')
        programa = get_object_or_404(Programa, id_programa=programa_id)
        
        # Cambiar el estado a Disponible
        programa.estado = 'Disponible'
        programa.motivo_baja = None  # Limpiar el motivo de baja
        programa.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Programa "{programa.materia} - {programa.carrera}" reactivado correctamente'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@require_POST
def obtener_informe_baja_programa(request):
    """Vista para obtener los datos del informe de baja de programa - CORREGIDO"""
    try:
        programa_id = request.POST.get('programa_id')
        
        print(f"🔍 Obteniendo informe para programa ID: {programa_id}")
        
        if not programa_id:
            return JsonResponse({
                'success': False,
                'error': 'ID de programa requerido'
            }, status=400)
        
        programa = get_object_or_404(Programa, id_programa=programa_id)
        
        print(f"📚 Programa encontrado: {programa.materia} - {programa.profesor}")
        print(f"📝 Motivo de baja: {programa.motivo_baja}")
        print(f"🖼️ Imagen rota: {programa.imagen_rota}")
        
        # Construir URL de imagen si existe
        imagen_baja_url = None
        if programa.imagen_rota:
            imagen_baja_url = programa.imagen_rota.url
            print(f"✅ URL de imagen construida: {imagen_baja_url}")
        else:
            print("❌ No hay imagen de baja")
        
        # Obtener los datos reales de la baja desde el modelo - IGUAL QUE EN LIBROS
        informe_data = {
            'motivo_baja': programa.motivo_baja if programa.motivo_baja else 'Motivo no registrado',
            'fecha_baja': '30/10/2024',  # Puedes agregar este campo a tu modelo si lo necesitas
            'imagen_baja': imagen_baja_url,  # URL completa o None
            'usuario_baja': 'Admin',  # Puedes agregar este campo a tu modelo si lo necesitas
            'descripcion': programa.descripcion if programa.descripcion else '',
        }
        
        print(f"📋 Datos del informe enviados: {informe_data}")
        
        return JsonResponse({
            'success': True,
            'informe': informe_data
        })
        
    except Exception as e:
        print(f"❌ Error en obtener_informe_baja_programa: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'error': f'Error: {str(e)}'
        }, status=500)


@require_POST
def obtener_informe_baja_notebook(request):
    """Vista para obtener los datos del informe de baja de notebook - APLICANDO LÓGICA DE LIBROS"""
    try:
        notebook_id = request.POST.get('notebook_id')
        
        print(f"🔍 Obteniendo informe para notebook ID: {notebook_id}")
        
        if not notebook_id:
            return JsonResponse({
                'success': False,
                'error': 'ID de notebook requerido'
            }, status=400)
        
        notebook = get_object_or_404(Notebook, id_not=notebook_id)
        
        print(f"💻 Notebook encontrado: {notebook.modelo_not}")
        print(f"📝 Motivo de baja: {notebook.motivo_baja}")
        print(f"🖼️ Imagen rota: {notebook.imagen_rota}")
        
        # Construir URL de imagen si existe
        imagen_baja_url = None
        if notebook.imagen_rota:
            # IMPORTANTE: Construir la URL completa
            imagen_baja_url = notebook.imagen_rota.url
            print(f"✅ URL de imagen construida: {imagen_baja_url}")
        else:
            print("❌ No hay imagen de baja")
        
        # Obtener los datos reales de la baja desde el modelo - IGUAL QUE EN LIBROS
        informe_data = {
            'motivo_baja': notebook.motivo_baja if notebook.motivo_baja else 'Motivo no registrado',
            'fecha_baja': '30/10/2024',  # Puedes agregar este campo a tu modelo si lo necesitas
            'imagen_baja': imagen_baja_url,  # URL completa o None
            'usuario_baja': 'Admin',  # Puedes agregar este campo a tu modelo si lo necesitas
            'descripcion': notebook.descripcion if notebook.descripcion else '',
        }
        
        print(f"📋 Datos del informe enviados: {informe_data}")
        
        return JsonResponse({
            'success': True,
            'informe': informe_data
        })
        
    except Exception as e:
        print(f"❌ Error en obtener_informe_baja_notebook: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'error': f'Error: {str(e)}'
        }, status=500)


def dar_alta_notebook(request):
    """
    Vista para reactivar un notebook dado de baja
    """
    try:
        notebook_id = request.POST.get('notebook_id')
        sede = request.POST.get('sede', 'LA PLATA')
        observaciones = request.POST.get('observaciones', '')
        
        if not notebook_id:
            return JsonResponse({
                'success': False, 
                'error': 'ID de notebook requerido'
            }, status=400)
        
        # Obtener el notebook
        notebook = get_object_or_404(Notebook, id_not=notebook_id)
        
        # Verificar que esté dado de baja
        if notebook.estado != 'No disponible':
            return JsonResponse({
                'success': False, 
                'error': 'El notebook no está dado de baja'
            }, status=400)
        
        # Actualizar el notebook
        notebook.estado = 'Disponible'
        notebook.sede = sede
        
        # Agregar observaciones si las hay
        if observaciones:
            notebook.descripcion = f"{notebook.descripcion} - {observaciones}" if notebook.descripcion else observaciones
        
        # Limpiar motivo de baja al reactivar
        notebook.motivo_baja = ''
        notebook.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Notebook "{notebook.modelo_not}" reactivado correctamente'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


def obtener_informe_baja_proyector(request):
    """
    Vista para obtener información de baja de un proyector específico
    """
    try:
        proyector_id = request.POST.get('proyector_id')
        
        if not proyector_id:
            return JsonResponse({
                'success': False, 
                'error': 'ID de proyector requerido'
            }, status=400)
        
        # Obtener el proyector
        proyector = get_object_or_404(Proyector, id_proyector=proyector_id)
        
        # Verificar que esté dado de baja
        if proyector.estado != 'No disponible':
            return JsonResponse({
                'success': False, 
                'error': 'El proyector no está dado de baja'
            }, status=400)
        
        # Preparar datos del informe
        from datetime import datetime
        
        return JsonResponse({
            'success': True,
            'motivo': proyector.motivo_baja or 'Sin motivo especificado',
            'fecha_baja': proyector.fecha_baja.strftime('%d/%m/%Y') if hasattr(proyector, 'fecha_baja') and proyector.fecha_baja else datetime.now().strftime('%d/%m/%Y')
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'error': f'Error al cargar: {str(e)}'
        })


def dar_alta_proyector(request):
    """
    Vista para reactivar un proyector dado de baja
    """
    try:
        proyector_id = request.POST.get('proyector_id')
        sede = request.POST.get('sede', 'LA PLATA')
        observaciones = request.POST.get('observaciones', '')
        
        if not proyector_id:
            return JsonResponse({
                'success': False, 
                'error': 'ID de proyector requerido'
            }, status=400)
        
        # Obtener el proyector
        proyector = get_object_or_404(Proyector, id_proyector=proyector_id)
        
        # Verificar que esté dado de baja
        if proyector.estado != 'No disponible':
            return JsonResponse({
                'success': False, 
                'error': 'El proyector no está dado de baja'
            }, status=400)
        
        # Actualizar el proyector
        proyector.estado = 'Disponible'
        proyector.sede = sede
        
        # Agregar observaciones si las hay
        if observaciones:
            proyector.descripcion = f"{proyector.descripcion} - {observaciones}" if proyector.descripcion else observaciones
        
        # Limpiar motivo de baja al reactivar
        proyector.motivo_baja = ''
        proyector.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Proyector reactivado correctamente'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


def obtener_informe_baja_varios(request):
    """Vista para obtener el informe de baja de varios específico"""
    try:
        import json
        data = json.loads(request.body)
        varios_id = data.get('varios_id')
        
        # Obtener el objeto varios
        varios = get_object_or_404(Varios, id_varios=varios_id)
        
        # Verificar que esté dado de baja
        if varios.estado != 'No disponible':
            return JsonResponse({
                'success': False,
                'error': 'El material varios no está dado de baja'
            }, status=400)
        
        # Construir URL de imagen si existe
        imagen_baja_url = None
        if varios.imagen_rota:
            imagen_baja_url = varios.imagen_rota.url
        
        # Obtener los datos reales de la baja
        from datetime import datetime
        fecha_baja_str = varios.fecha_baja.strftime('%d/%m/%Y') if getattr(varios, 'fecha_baja', None) else datetime.now().strftime('%d/%m/%Y')
        informe_data = {
            'motivo': varios.motivo_baja if varios.motivo_baja else 'Motivo no registrado',
            'fecha_baja': fecha_baja_str,
            'imagen_baja': imagen_baja_url,
            'usuario_baja': str(request.user) if request.user.is_authenticated else 'Admin',
            'descripcion': varios.descripcion if hasattr(varios, 'descripcion') and varios.descripcion else '',
        }
        
        return JsonResponse({
            'success': True,
            'informe': informe_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error: {str(e)}'
        }, status=500)


@require_POST
def dar_alta_varios(request):
    """Vista para dar de alta varios (cambiar estado a disponible)"""
    try:
        varios_id = request.POST.get('varios_id')
        sede = request.POST.get('sede', 'LA PLATA')
        disponibilidad = request.POST.get('disponibilidad', 'Domicilio')
        observaciones = request.POST.get('observaciones', '')
        
        if not varios_id:
            return JsonResponse({
                'success': False, 
                'error': 'ID de varios requerido'
            }, status=400)
        
        # Obtener el objeto varios
        varios = get_object_or_404(Varios, id_varios=varios_id)
        
        # Verificar que esté dado de baja
        if varios.estado != 'No disponible':
            return JsonResponse({
                'success': False, 
                'error': 'El material varios no está dado de baja'
            }, status=400)
        
        # Actualizar el varios
        varios.estado = 'Disponible'
        varios.sede = sede
        varios.disponibilidad = disponibilidad
        
        # Agregar observaciones si las hay
        if observaciones:
            varios.descripcion = f"{varios.descripcion} - {observaciones}" if varios.descripcion else observaciones
        
        # Limpiar motivo de baja al reactivar
        varios.motivo_baja = ''
        varios.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Material varios reactivado correctamente'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })