from django.shortcuts import render

def home(request):
    return render(request, 'home.html', {'header_class': 'header-home'})

def alta_material(request):
    return render(request, 'materiales/alta_material.html', {'header_class': 'header-pantalla'})

def modificacion_editar_material(request):
    return render(request, 'components/modificacion_materiales/modificacion_editar_material.html', {'header_class': 'header-pantalla'})
    