# libros/models.py
from django.db import models

class Inventario(models.Model):
    id_inventario = models.IntegerField(primary_key=True)
    estado = models.CharField(max_length=255)
    motivo_baja = models.CharField(max_length=255)
    descripcion = models.TextField()
    num_ejemplar = models.IntegerField()

    def __str__(self):
        return f"id_libro: {self.id_inventario}, estado: {self.estado}, motivo_baja: {self.motivo_baja}, descripcion: {self.descripcion}, numero ejemplar: {self.num_ejemplar} "


class Libro(Inventario):
    id_libro = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    editorial = models.CharField(max_length=255)
    cdu = models.CharField(max_length=255)
    resumen = models.TextField()
    img = models.URLField()

    def __str__(self):
        return f"id_libro: {self.id_libro}, titulo: {self.titulo}, autor: {self.autor}, editorial: {self.editorial}, cdu: {self.cdu}, resumen: {self.resumen}, imagen: {self.img} "


class Mapas(Inventario):
    id_mapa = models.IntegerField(primary_key=True)
    tipo = models.CharField(max_length=255)

    def __str__(self):
        return f"id: {self.id_mapa}, tipo: {self.tipo}"

class Multimedia(Inventario):
    id_multi = models.IntegerField(primary_key=True)
    materia = models.CharField(max_length=255)
    contenido = models.CharField(max_length=255)

    def __str__(self):
        return f"id: {self.id_multi}, materia: {self.materia}, contenido: {self.contenido}"

class Notebook(Inventario):
    id_not = models.IntegerField(primary_key=True)
    marca_not = models.CharField(max_length=255)
    modelo_not = models.CharField(max_length=255)

    def __str__(self):
        return f"id: {self.id_not}, marca: {self.marca_not}, modelo: {self.modelo_not}"

class Proyector(Inventario):
    id_proyector = models.IntegerField(primary_key=True)
    marca_pro = models.CharField(max_length=255)
    modelo_pro = models.CharField(max_length=255)

    def __str__(self):
        return f"id: {self.id_proyector}, marca: {self.marca_pro}, modelo: {self.modelo_pro}"

class Varios(Inventario):
    id_varios = models.IntegerField(primary_key=True)
    tipo = models.CharField(max_length=255)

    def __str__(self):
        return f"id: {self.id_varios}, tipo: {self.tipo}"
        
