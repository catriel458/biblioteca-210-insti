# materiales/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # URL principal - Home
    path('', views.home, name='home'),
    
    # URLs de autenticación
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('cambiar-password/', views.cambiar_password, name='cambiar_password'),
    
    # URLs de libros
    path('libros/', views.lista_libros, name='lista_libros'),
    path('alta-libro/', views.alta_libro, name='alta_libro'),
    path('baja-libro/', views.baja_libro, name='baja_libro'),
    path('editar-libro/<int:libro_id>/', views.editar_libro, name='editar_libro'),
    path('buscar-libros/', views.buscar_libros, name='buscar_libros'),
    path('borrar-libros/', views.borrar_libros, name='borrar_libros'),
    
    # URLs de mapas
    path('mapas/', views.mapas_view, name='mapas'),
    path('alta-mapa/', views.alta_mapa, name='alta_mapa'),
    path('baja-mapa/', views.baja_mapa, name='baja_mapa'),
    path('editar-mapa/<int:mapa_id>/', views.editar_mapa, name='editar_mapa'),
    path('buscar-mapas/', views.buscar_mapas, name='buscar_mapas'),
    
    # URLs de multimedia
    path('multimedia/', views.multimedia_view, name='multimedia'),
    path('alta-multimedia/', views.alta_multimedia, name='alta_multimedia'),
    path('baja-multimedia/', views.baja_multimedia, name='baja_multimedia'),
    path('editar-multimedia/<int:multi_id>/', views.editar_multimedia, name='editar_multimedia'),
    path('buscar-multimedia/', views.buscar_multimedia, name='buscar_multimedia'),
    
    # URLs de notebooks
    path('notebook/', views.notebook_view, name='notebook'),
    path('alta-notebook/', views.alta_notebook, name='alta_notebook'),
    path('baja-notebook/', views.baja_notebook, name='baja_notebook'),
    path('editar-notebook/<int:not_id>/', views.editar_notebook, name='editar_notebook'),
    path('buscar-notebooks/', views.buscar_notebooks, name='buscar_notebooks'),
    
    # URLs de proyectores
    path('proyector/', views.proyector_view, name='proyector'),
    path('alta-proyector/', views.alta_proyector, name='alta_proyector'),
    path('baja-proyector/', views.baja_proyector, name='baja_proyector'),
    path('editar-proyector/<int:proyector_id>/', views.editar_proyector, name='editar_proyector'),
    path('buscar-proyectores/', views.buscar_proyectores, name='buscar_proyectores'),
    
    # URLs de varios
    path('varios/', views.varios_view, name='varios'),
    path('alta-varios/', views.alta_varios, name='alta_varios'),
    path('baja-varios/', views.baja_varios, name='baja_varios'),
    path('editar-varios/<int:varios_id>/', views.editar_varios, name='editar_varios'),
    path('buscar-varios/', views.buscar_varios, name='buscar_varios'),
    
    # URLs de préstamos
    path('solicitar-prestamo/<int:libro_id>/', views.solicitar_prestamo, name='solicitar_prestamo'),
    path('prestamos-solicitados/', views.prestamos_solicitados, name='prestamos_solicitados'),
    path('gestionar-prestamos/', views.gestionar_prestamos, name='gestionar_prestamos'),
    path('aprobar-prestamo/<int:prestamo_id>/', views.aprobar_prestamo, name='aprobar_prestamo'),
    path('rechazar-prestamo/<int:prestamo_id>/', views.rechazar_prestamo, name='rechazar_prestamo'),
    path('finalizar-prestamo/<int:prestamo_id>/', views.finalizar_prestamo, name='finalizar_prestamo'),
    path('aprobar-solicitud-prestamo/<int:prestamo_id>/', views.aprobar_solicitud_prestamo, name='aprobar_solicitud_prestamo'),
    path('cancelar-reserva-usuario/<int:prestamo_id>/', views.cancelar_reserva_usuario, name='cancelar_reserva_usuario'),
    path('confirmar-retiro-libro/<int:prestamo_id>/', views.confirmar_retiro_libro, name='confirmar_retiro_libro'),
    path('marcar-no-retiro/<int:prestamo_id>/', views.marcar_no_retiro, name='marcar_no_retiro'),
    
    # URLs de gestión
    path('registro-de-bajas/', views.registro_bajas, name='registro_de_bajas'),
    path('reactivar-libro/<int:libro_id>/', views.reactivar_libro, name='reactivar_libro'),
    path('cargar-csv/', views.cargar_csv, name='cargar_csv'),
    path('success/', views.success_view, name='success_url'),
    path('formulario/libro/', views.formulario_libro, name='formulario_libro'),

    # URL principal para alta de materiales
    path('alta/', views.alta_materiales, name='alta_materiales'),
    path('confirmar-alta-libro/', views.confirmar_alta_libro, name='confirmar_alta_libro'),
    path('guardar-libro-confirmado/', views.guardar_libro_confirmado, name='guardar_libro_confirmado'),
    path('cancelar-alta-libro/', views.cancelar_alta_libro, name='cancelar_alta_libro'),

    # Lista y modificación de materiales:

    path('modificacion/', views.modificacion_materiales, name='modificacion_materiales'),

    # URLs para sistema de obleas y dar de alta libros REACTIVADOS

    path('dar-alta-libro/', views.dar_alta_libro, name='dar_alta_libro'),
    path('obtener-informe-baja/', views.obtener_informe_baja, name='obtener_informe_baja'),
    path('ver-detalles-material/<int:libro_id>/', views.ver_detalles_material, name='ver_detalles_material'),
    path('reactivar-libro-mejorado/<int:libro_id>/', views.reactivar_libro_mejorado, name='reactivar_libro_mejorado'),



     # URLs para programas
    # URLs para programas - AGREGAR ESTAS LÍNEAS
    path('programas/', views.lista_programas, name='lista_programas'),
    path('formulario/programa/', views.formulario_programa, name='formulario_programa'),
    path('alta-programa/', views.alta_programa, name='alta_programa'),
    path('confirmar-alta-programa/', views.confirmar_alta_programa, name='confirmar_alta_programa'),
    path('guardar-programa-confirmado/', views.guardar_programa_confirmado, name='guardar_programa_confirmado'),
    path('cancelar-alta-programa/', views.cancelar_alta_programa, name='cancelar_alta_programa'),

]

