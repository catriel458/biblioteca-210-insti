# management/commands/verificar_vencimientos.py
from django.core.management.base import BaseCommand
from libros.views import verificar_y_notificar_vencimientos

class Command(BaseCommand):
    help = 'Verifica préstamos próximos a vencer y envía notificaciones'

    def handle(self, *args, **options):
        verificar_y_notificar_vencimientos()
        self.stdout.write(
            self.style.SUCCESS('Verificación de vencimientos completada')
        )