from django.urls import path
from . import views
from .views import lista_libros, baja_libro

urlpatterns = [
    path('', views.lista_libros, name='lista_libros'),  # Página principal o listado de libros
    path('alta-inventario/', views.alta_inventario, name='alta_inventario'),  # Ruta para dar de alta en inventario
    path('alta-libro/', views.alta_libro, name='alta_libro'),  # Ruta para dar de alta un libro
    path('libros/baja/', baja_libro, name='baja_libro'),  # Nueva ruta
]
