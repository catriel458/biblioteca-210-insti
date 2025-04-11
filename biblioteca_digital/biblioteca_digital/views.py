from django.shortcuts import render

def home(request):
    return render(request, 'home.html', {'header_class': 'header-home'})

def alta_material(request):
    return render(request, 'materiales/alta_material.html', {'header_class': 'header-pantalla'})
