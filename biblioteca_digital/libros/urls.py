from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_libros, name='lista_libros'),
    path('', views.alta_inventario, name = 'alta_inventario')
]