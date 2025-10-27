# Generated manually to update existing data

from django.db import migrations

def update_alumno_to_estudiante(apps, schema_editor):
    """
    Actualiza todos los registros existentes que tengan 'alumno' por 'estudiante'
    """
    Usuario = apps.get_model('materiales', 'Usuario')
    Prestamo = apps.get_model('materiales', 'Prestamo')
    
    # Actualizar usuarios con perfil 'alumno' a 'estudiante'
    Usuario.objects.filter(perfil='alumno').update(perfil='estudiante')
    
    # Actualizar préstamos con tipo_usuario 'alumno' a 'estudiante'
    Prestamo.objects.filter(tipo_usuario='alumno').update(tipo_usuario='estudiante')

def reverse_update_estudiante_to_alumno(apps, schema_editor):
    """
    Función reversa para deshacer los cambios si es necesario
    """
    Usuario = apps.get_model('materiales', 'Usuario')
    Prestamo = apps.get_model('materiales', 'Prestamo')
    
    # Revertir usuarios con perfil 'estudiante' a 'alumno'
    Usuario.objects.filter(perfil='estudiante').update(perfil='alumno')
    
    # Revertir préstamos con tipo_usuario 'estudiante' a 'alumno'
    Prestamo.objects.filter(tipo_usuario='estudiante').update(tipo_usuario='alumno')

class Migration(migrations.Migration):

    dependencies = [
        ('materiales', '0020_alter_prestamo_tipo_usuario_alter_usuario_perfil'),
    ]

    operations = [
        migrations.RunPython(
            update_alumno_to_estudiante,
            reverse_update_estudiante_to_alumno
        ),
    ]