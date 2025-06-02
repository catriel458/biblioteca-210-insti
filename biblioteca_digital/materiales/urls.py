from django.urls import path
from . import views
from .views import lista_libros, baja_libro, editar_libro
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import cargar_csv
from .views import buscar_libros
from .views import buscar_mapas  
from .views import buscar_multimedia
from .views import buscar_notebooks
from .views import buscar_proyectores
from .views import buscar_varios
from .views import registro_bajas

from .views import (
    mapas_view,
    alta_mapa,
    baja_mapa,
    editar_mapa,
    multimedia_view,
    alta_multimedia,
    baja_multimedia,
    editar_multimedia,
    lista_libros,
    alta_inventario,
    alta_libro,
    baja_libro,
    editar_libro,
    notebook_view,
    alta_notebook,
    baja_notebook,
    editar_notebook,
    proyector_view,
    alta_proyector,
    baja_proyector,
    editar_proyector,
    varios_view,
    alta_varios,
    baja_varios,
    editar_varios,
)

urlpatterns = [

    # =========================
    # VISTAS PRINCIPALES
    # =========================
    path('materiales/', views.lista_libros, name='lista_libros'),
    path('mapas/', views.mapas_view, name='mapas'),
    path('multimedia/', views.multimedia_view, name='multimedia'),
    path('notebook/', views.notebook_view, name='notebook'),
    path('proyector/', views.proyector_view, name='proyector'),
    path('varios/', views.varios_view, name='varios'),
    # =========================
    # ALTAS
    # =========================
    path('alta-inventario/', views.alta_inventario, name='alta_inventario'),
    path('alta_libro/', views.alta_libro, name='alta_libro'),
    # =========================
    # BAJAS
    # =========================
    path('materiales/baja/', views.baja_libro, name='baja_libro'),
    path('mapas/baja/', baja_mapa, name='baja_mapa'),
    path('alta-mapa/', alta_mapa, name='alta_mapa'),
    path('editar-mapa/<int:mapa_id>/', editar_mapa, name='editar_mapa'),
    # =========================
    # EDICIÓN
    # =========================
    path('editar-libro/<int:libro_id>/', views.editar_libro, name='editar_libro'),
    path('multimedia/baja/', baja_multimedia, name='baja_multimedia'),
    path('alta-multimedia/', alta_multimedia, name='alta_multimedia'),
    path('editar-multimedia/<int:multi_id>/', editar_multimedia, name='editar_multimedia'),
    path('alta-notebook/', alta_notebook, name='alta_notebook'),
    path('editar-notebook/<int:not_id>/', views.editar_notebook, name='editar_notebook'),
    path('baja_notebook/', baja_notebook, name='baja_notebook'),
    path('alta-proyector/', alta_proyector, name='alta_proyector'),
    path('editar-proyector/<int:proyector_id>/', views.editar_proyector, name='editar_proyector'),
    path('baja_proyector/', baja_proyector, name='baja_proyector'),
    path('baja_varios/', baja_varios, name='baja_varios'),
    path('alta-varios/', alta_varios, name='alta_varios'),
    path('editar-varios/<int:varios_id>/', views.editar_varios, name='editar_varios'),
    path('cargar-csv/', views.cargar_csv, name='cargar_csv'),
    path('success/', views.success_view, name='success_url'),
    path('borrar-materiales/', views.borrar_libros, name='borrar_libros'),
    # =========================
    # BÚSQUEDAS
    # =========================
    path('buscar_materiales/', buscar_libros, name='buscar_libros'),
    path('buscar_mapas/', buscar_mapas, name='buscar_mapas'),
    path('buscar_multimedia/', buscar_multimedia, name='buscar_multimedia'),
    path('buscar_notebook/', buscar_notebooks, name='buscar_notebooks'),
    path('buscar_proyectores/', buscar_proyectores, name='buscar_proyectores'),
    path('buscar_varios/', buscar_varios, name='buscar_varios'),
    # =========================
    # UTILIDADES Y OTRAS FUNCIONES
    # =========================
    path('registro_bajas/', views.registro_bajas, name='registro_de_bajas'),
    path('modificacion-material/', views.modificacion_materiales, name='modificacion_materiales'),
    path('prestamos/', views.prestamos, name='prestamos'),
    # Ruta para obtener templates de materiales
    path('get_material_template/<str:tipo>/', views.get_material_template, name='get_material_template'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)