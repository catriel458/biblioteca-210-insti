from django.core.management.base import BaseCommand
from materiales.models import Usuario

class Command(BaseCommand):
    help = 'Crea usuarios bibliotecarias iniciales'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Fuerza la recreación de usuarios existentes',
        )

    def handle(self, *args, **options):
        self.stdout.write('Creando usuarios bibliotecarias...')
        
        # Usuario 1: Bibliotecaria principal (del sistema back)
        dni_bibliotecaria = '35135884'
        if options['force'] and Usuario.objects.filter(dni=dni_bibliotecaria).exists():
            Usuario.objects.filter(dni=dni_bibliotecaria).delete()
            self.stdout.write(f'Usuario existente eliminado: {dni_bibliotecaria}')
        
        if not Usuario.objects.filter(dni=dni_bibliotecaria).exists():
            bibliotecaria = Usuario.objects.create_user(
                dni=dni_bibliotecaria,
                password='Biblioteca210',
                nombre='Bibliotecaria',
                apellido='Principal',
                email='biblioteca@insti.edu.ar',
                perfil='bibliotecaria'
            )
            self.stdout.write(
                self.style.SUCCESS(f'✓ Usuario bibliotecaria principal creado: {bibliotecaria.dni}')
            )
        else:
            self.stdout.write(f'✓ Usuario bibliotecaria principal ya existe: {dni_bibliotecaria}')
        
        # Usuario 2: Nicolas Caprio (del sistema insti)
        dni_nicolas = '41293236'
        if options['force'] and Usuario.objects.filter(dni=dni_nicolas).exists():
            Usuario.objects.filter(dni=dni_nicolas).delete()
            self.stdout.write(f'Usuario existente eliminado: {dni_nicolas}')
        
        if not Usuario.objects.filter(dni=dni_nicolas).exists():
            nicolas = Usuario.objects.create_user(
                dni=dni_nicolas,
                password='12345678',
                nombre='Nicolas',
                apellido='Caprio',
                email='nicocaprio@outlook.com',
                perfil='bibliotecaria'
            )
            self.stdout.write(
                self.style.SUCCESS(f'✓ Usuario Nicolas Caprio creado: {nicolas.dni}')
            )
        else:
            self.stdout.write(f'✓ Usuario Nicolas Caprio ya existe: {dni_nicolas}')
        
        self.stdout.write(self.style.SUCCESS('¡Proceso completado!'))