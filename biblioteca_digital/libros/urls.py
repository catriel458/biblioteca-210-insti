# libros/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # URLs de autenticación
    path('', views.login_view, name='login'),  # Página principal es el login
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('cambiar-password/', views.cambiar_password, name='cambiar_password'),
    
    # URLs principales (requieren autenticación)
    path('home/', views.pantalla_principal, name='pantalla_principal'),
    
    # URLs de libros
    path('libros/', views.lista_libros, name='lista_libros'),
    path('alta-libro/', views.alta_libro, name='alta_libro'),
    path('baja-libro/', views.baja_libro, name='baja_libro'),
    path('editar-libro/<int:libro_id>/', views.editar_libro, name='editar_libro'),
    path('buscar-libros/', views.buscar_libros, name='buscar_libros'),
    path('borrar-libros/', views.borrar_libros, name='borrar_libros'),
    path('marcar-libro-devuelto/<int:sancion_id>/', views.marcar_libro_devuelto, name='marcar_libro_devuelto'),
    
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


    # URLs para gestión de usuarios (AGREGAR AL FINAL)
    path('gestion-usuarios/', views.gestion_usuarios, name='gestion_usuarios'),
    path('buscar-usuarios/', views.buscar_usuarios, name='buscar_usuarios'),
    path('crear-usuario/', views.crear_usuario, name='crear_usuario'),
    path('editar-usuario/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar-usuario/', views.eliminar_usuario, name='eliminar_usuario'),
    path('exportar-usuarios-excel/', views.exportar_usuarios_excel, name='exportar_usuarios_excel'),
    
    # URLs para gestión de sanciones
    path('gestionar-sanciones/', views.gestionar_sanciones, name='gestionar_sanciones'),
    path('confirmar-sancion/<int:sancion_id>/', views.confirmar_sancion, name='confirmar_sancion'),
    path('cancelar-sancion/<int:sancion_id>/', views.cancelar_sancion_con_modal, name='cancelar_sancion'),
    path('devolver-libro-catalogo/<int:sancion_id>/', views.devolver_libro_catalogo, name='devolver_libro_catalogo'),  # NUEVA
    path('marcar-libro-devuelto/<int:sancion_id>/', views.marcar_libro_devuelto, name='marcar_libro_devuelto'),
    path('mis-sanciones/', views.mis_sanciones, name='mis_sanciones'),


]