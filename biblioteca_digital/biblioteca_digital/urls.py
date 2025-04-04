"""
URL configuration for biblioteca_digital project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.http import HttpResponseRedirect
from django.conf import settings
from django.conf.urls.static import static
from . import views  # Importamos las vistas del proyecto principal


urlpatterns = [
    path('admin/', admin.site.urls),
    # Rutas principales del sitio
    path('', views.home, name='home'),  # Nueva ruta para el home principal
    path('alta_material/', views.alta_material, name='alta_material'),  # Nueva ruta para alta_material
    # Rutas de la app libros
    path('libros/', include('libros.urls')),

    # Ruta opcional para redirigir a /libros/
    path('redirigir_libros/', lambda request: HttpResponseRedirect('/libros/')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
