from django.core.management.base import BaseCommand
from django.apps import apps


class Command(BaseCommand):
    help = (
        "Elimina cualquier tipo de material por su clave primaria (pk). "
        "Usar --tipo para indicar el modelo y --id para el valor de pk."
    )

    # Mapeo de nombres amigables a nombres de modelos reales en la app 'materiales'
    MODEL_MAP = {
        'libro': 'Libro',
        'mapa': 'Mapas',
        'mapas': 'Mapas',
        'multimedia': 'Multimedia',
        'notebook': 'Notebook',
        'proyector': 'Proyector',
        'varios': 'Varios',
        'programa': 'Programa',
        'inventario': 'Inventario',
    }

    def add_arguments(self, parser):
        parser.add_argument(
            '--tipo',
            type=str,
            required=True,
            help=(
                "Tipo de material a eliminar. Opciones: "
                "libro, mapa(s), multimedia, notebook, proyector, varios, programa, inventario"
            ),
        )
        parser.add_argument(
            '--id',
            type=int,
            required=True,
            help='Valor de la clave primaria (pk) del registro a eliminar',
        )

    def handle(self, *args, **options):
        tipo = options['tipo'].strip().lower()
        pk_value = options['id']

        # Resolver nombre de modelo
        model_name = self.MODEL_MAP.get(tipo)
        if not model_name:
            disponibles = ', '.join(sorted(self.MODEL_MAP.keys()))
            self.stdout.write(self.style.ERROR(
                f"Tipo '{tipo}' no reconocido. Tipos disponibles: {disponibles}"
            ))
            return

        # Obtener el modelo dinámicamente
        try:
            Model = apps.get_model('materiales', model_name)
        except LookupError:
            self.stdout.write(self.style.ERROR(
                f"No se pudo resolver el modelo '{model_name}' en la app 'materiales'"
            ))
            return

        # Usamos 'pk' para que funcione con cualquier nombre de campo de clave primaria
        qs = Model.objects.filter(pk=pk_value)

        before = qs.count()
        if before == 0:
            self.stdout.write(self.style.WARNING(
                f"No existe {model_name} con pk={pk_value}"
            ))
            return

        result = qs.delete()  # (num_deleted, details)
        exists_after = Model.objects.filter(pk=pk_value).exists()

        self.stdout.write(self.style.SUCCESS(
            f"Eliminación realizada para {model_name}. Antes={before}, Resultado={result}, ExisteLuego={exists_after}"
        ))