import json
from django.shortcuts import render
from collections import Counter

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
    # Leer el archivo JSON
    with open('/home/usuario210/Escritorio/prueba/biblioteca-210/biblioteca_digital/libros/fixtures/cant_ejemplares.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Suponiendo que solo hay un objeto en la lista, toma el primero
    if data:
        base_libros = data[0].get('base_ejemplares', [])
    else:
        base_libros = []

    # Crear una lista de libros a partir de los datos JSON
    libros = [
        {
            'titulo': item.get('titulo', 'Título no disponible'),
            'codigo': item.get('signatura', 'código no disponible'),
            'autor': item.get('autor', 'Autor no disponible'),
            'Editorial': item.get('Editorial', 'Editorial no disponible'),
            'resumen': item.get('resumen', 'Resumen no disponible'),
            'img': item.get('img', '')
        }
        for item in base_libros
    ]
    
    # Contar las ocurrencias de cada título
    titulos = [libro['titulo'] for libro in libros]
    conteo_titulos = Counter(titulos)
    
    # Crear una lista para almacenar solo un ejemplar de cada libro
    libros_unicos = {}
    
    # Agregar el conteo y las cantidades disponibles a cada libro
    for libro in libros:
        if libro['titulo'] not in libros_unicos:
            cantidad_total = conteo_titulos[libro['titulo']]
            cantidad_lectura_sala = 1
            cantidad_prestamo = max(cantidad_total - cantidad_lectura_sala, 0)  # Resta 1 para lectura en sala
            
            libros_unicos[libro['titulo']] = {
                'titulo': libro['titulo'],
                'codigo': libro['codigo'],
                'autor': libro['autor'],
                'Editorial': libro['Editorial'],
                'resumen': libro['resumen'],
                'img': libro['img'],
                'cantidad_total': cantidad_total,
                'cantidad_lectura_sala': cantidad_lectura_sala,
                'cantidad_prestamo': cantidad_prestamo
            }
    
    # Convertir el diccionario a una lista
    libros_unicos_list = list(libros_unicos.values())
    
    # Renderizar el template con la lista de libros únicos
    return render(request, 'libros/lista_libros.html', {'libros': libros_unicos_list})

from .forms import LibroForm


def alta_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            id_libro = form.cleaned_data['id_libro']
            
            # Verificar si el libro ya existe
            if Libro.objects.filter(id_libro=id_libro).exists():
                return render(request, 'alta_libro.html', {'form': form, 'error': 'El libro ya existe.'})
            else:
                # Guardar el nuevo libro
                form.save()
                return render(request, 'alta_libro.html', {'form': form, 'success': 'Libro registrado exitosamente.'})
        else:
            return render(request, 'alta_libro.html', {'form': form, 'error': 'Por favor complete todos los campos obligatorios.'})
    else:
        form = LibroForm()
    
    return render(request, 'alta_libro.html', {'form': form})