from django.contrib import admin
from .models import Inventario  # Importa tu modelo
from .models import Libro
from .models import Mapas
from .models import Multimedia
from .models import Notebook
from .models import Proyector
from .models import Varios

admin.site.register(Inventario)
admin.site.register(Libro)
admin.site.register(Mapas)
admin.site.register(Multimedia)
admin.site.register(Notebook)
admin.site.register(Proyector)
admin.site.register(Varios)
