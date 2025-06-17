# create_bibliotecaria.py
# UBICACIÓN: En la raíz del proyecto, al mismo nivel que manage.py
# Ejecutar este script después de hacer las migraciones

import os
import sys
import django

# Agregar el directorio actual al path de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configurar Django (ajustar el nombre del módulo si es diferente)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biblioteca_digital.settings')
django.setup()

from libros.models import Usuario

def crear_bibliotecaria():
    """Crear la cuenta de la bibliotecaria si no existe"""
    
    dni_bibliotecaria = '35135884'
    
    # Verificar si ya existe
    if Usuario.objects.filter(dni=dni_bibliotecaria).exists():
        print(f"La bibliotecaria con DNI {dni_bibliotecaria} ya existe.")
        return
    
    # Crear la bibliotecaria
    bibliotecaria = Usuario.objects.create_user(
        dni=dni_bibliotecaria,
        password='Biblioteca210',
        nombre='Bibliotecaria',
        apellido='Principal',
        email='biblioteca@isfd210.edu.ar',
        perfil='bibliotecaria',
        is_staff=True
    )
    
    print(f"✅ Bibliotecaria creada exitosamente:")
    print(f"   DNI: {bibliotecaria.dni}")
    print(f"   Nombre: {bibliotecaria.get_full_name()}")
    print(f"   Email: {bibliotecaria.email}")
    print(f"   Perfil: {bibliotecaria.get_perfil_display()}")
    print(f"   Contraseña: Biblioteca210")

if __name__ == '__main__':
    crear_bibliotecaria()