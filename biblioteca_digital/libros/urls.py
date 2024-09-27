from django.urls import path
from . import views
from .views import lista_libros, baja_libro, editar_libro
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path  
from .views import mapas_view, alta_mapa, baja_mapa, editar_mapa
from .views import (
    lista_libros,
    alta_inventario,
    alta_libro,
    baja_libro,
    editar_libro,
    mapas_view,
    baja_mapa, 
    alta_mapa, # Asegúrate de importar esta vista
)

urlpatterns = [
    path('', views.pantalla_principal, name='pantalla_principal'),  # Página principal
    path('libros/', views.lista_libros, name='lista_libros'),
    path('mapas/', views.mapas_view, name='mapas'),
    path('multimedia/', views.multimedia_view, name='multimedia'),
    path('notebook/', views.notebook_view, name='notebook'),
    path('proyector/', views.proyector_view, name='proyector'),
    path('varios/', views.varios_view, name='varios'),
    path('alta-inventario/', views.alta_inventario, name='alta_inventario'),
    path('alta-libro/', views.alta_libro, name='alta_libro'),
    path('libros/baja/', views.baja_libro, name='baja_libro'),
    path('mapas/baja/', baja_mapa, name='baja_mapa'),  # Añadir esta línea
    path('alta-mapa/', alta_mapa, name='alta_mapa'),  # Ruta para el alta de mapas
    path('editar-mapa/<int:mapa_id>/', editar_mapa, name='editar_mapa'), 
    path('editar-libro/<int:libro_id>/', views.editar_libro, name='editar_libro')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)