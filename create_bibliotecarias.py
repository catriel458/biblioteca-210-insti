#!/usr/bin/env python
"""
Script para crear usuarios bibliotecarias iniciales
Replica la funcionalidad del backend para el frontend
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biblioteca_digital.settings')
django.setup()

from materiales.models import Usuario

def crear_bibliotecarias():
    """
    Crea dos usuarios bibliotecarias:
    1. Bibliotecaria principal (del sistema back)
    2. Nicolas Caprio (del sistema insti)
    """
    
    # Usuario 1: Bibliotecaria principal (del backend)
    dni_bibliotecaria = '35135884'
    if not Usuario.objects.filter(dni=dni_bibliotecaria).exists():
        bibliotecaria = Usuario.objects.create_user(
            dni=dni_bibliotecaria,
            password='Biblioteca210',
            nombre='Bibliotecaria',
            apellido='Principal',
            email='biblioteca@insti.edu.ar',
            perfil='bibliotecaria'
        )
        print(f"✓ Usuario bibliotecaria principal creado: {bibliotecaria.dni}")
    else:
        print(f"✓ Usuario bibliotecaria principal ya existe: {dni_bibliotecaria}")
    
    # Usuario 2: Nicolas Caprio (del sistema insti)
    dni_nicolas = '41293236'
    if not Usuario.objects.filter(dni=dni_nicolas).exists():
        nicolas = Usuario.objects.create_user(
            dni=dni_nicolas,
            password='12345678',
            nombre='Nicolas',
            apellido='Caprio',
            email='nicocaprio@outlook.com',
            perfil='bibliotecaria'
        )
        print(f"✓ Usuario Nicolas Caprio creado: {nicolas.dni}")
    else:
        print(f"✓ Usuario Nicolas Caprio ya existe: {dni_nicolas}")

if __name__ == '__main__':
    print("Creando usuarios bibliotecarias...")
    crear_bibliotecarias()
    print("¡Proceso completado!")