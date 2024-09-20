from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_libros, name='lista_libros'),  # Página principal o listado de libros
    path('alta-inventario/', views.alta_inventario, name='alta_inventario'),  # Ruta para dar de alta en inventario
    path('alta-libro/', views.alta_libro, name='alta_libro'),  # Ruta para dar de alta un libro
]
