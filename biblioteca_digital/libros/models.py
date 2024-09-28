# libros/models.py
from django.db import models


class Inventario(models.Model):
    # Este es el ID principal que usamos para dar de baja, modificar
    id_inventario = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=255, null=True, default="Disponible")
    motivo_baja = models.CharField(max_length=255, null=True)
    descripcion = models.TextField(null=True)
    num_ejemplar = models.IntegerField(null=True)
    imagen_rota = models.ImageField(
        upload_to='imagenes_rota/', null=True, blank=True)  # Nuevo campo

    def __str__(self):
        return f"id_libro: {self.id_inventario}, estado: {self.estado}, motivo_baja: {self.motivo_baja}, descripcion: {self.descripcion}, numero ejemplar: {self.num_ejemplar} "


class Libro(Inventario):
    id_libro = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    editorial = models.CharField(max_length=255)
    edicion = models.IntegerField(null=False, default=1999)
    codigo_materia = models.CharField(max_length=255, null=False, default=1)
    siglas_autor_titulo = models.CharField(
        max_length=255, null=False, default='ABC')
    num_inventario = models.IntegerField(null=False, default=1)
    resumen = models.TextField()
    img = models.URLField()

    def __str__(self):
        return f"id_libro: {self.id_libro}, titulo: {self.titulo}, autor: {self.autor}, editorial: {self.editorial}, codigo_materia: {self.codigo_materia}, siglas_autor_titulo: {self.siglas_autor_titulo}, num_inventario {self.num_inventario} resumen: {self.resumen}, imagen: {self.img} "


class Mapas(Inventario):
    # ¿Puede ser autofield (autoincremental)?
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
