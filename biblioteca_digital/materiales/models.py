# materiales/models.py

from django.db import models

class Libro(models.Model):
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    editorial = models.CharField(max_length=255)
    descripcion = models.TextField(null=True, blank=True)
    siglas_autor_titulo = models.CharField(max_length=255, null=True, blank=True)
    clasificacion_cdu = models.CharField(max_length=255, null=True, blank=True)
    palabras_clave = models.CharField(max_length=255, null=True, blank=True)
    imagen = models.ImageField(upload_to='libros/', null=True, blank=True)  # <--- NUEVO

    def __str__(self):
        return f"{self.titulo} - {self.autor}"

class Ejemplar(models.Model):
    libro = models.ForeignKey(Libro, related_name='ejemplares', on_delete=models.CASCADE)
    numero_ejemplar = models.IntegerField()
    sede = models.CharField(max_length=255)
    disponibilidad = models.CharField(max_length=50)
    observaciones = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Ejemplar {self.numero_ejemplar} de {self.libro.titulo} ({self.sede})"
            
class Mapas(models.Model):
    sede = models.CharField(max_length=255)
    # Otros campos generales si los necesitas

    def __str__(self):
        return f"Mapa en sede: {self.sede}"

class TipoMapa(models.Model):
    mapa = models.ForeignKey(Mapas, related_name='tipos', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)  # Ej: "FISICO", "DIGITAL"

    def __str__(self):
        return f"{self.nombre} ({self.mapa})"

class EjemplarMapa(models.Model):
    tipo_mapa = models.ForeignKey(TipoMapa, related_name='ejemplares', on_delete=models.CASCADE)
    n_registro = models.CharField(max_length=100)
    denominacion = models.CharField(max_length=255)
    descripcion = models.TextField()

    def __str__(self):
        return f"Ejemplar {self.n_registro} - {self.tipo_mapa.nombre}"
    
class Multimedia(models.Model):
    id_multi = models.AutoField(primary_key=True)
    profesor = models.CharField(max_length=255)
    url = models.URLField(max_length=500)
    carrera = models.CharField(max_length=255)
    materia = models.CharField(max_length=255)
    titulo = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.titulo} - {self.materia} - {self.profesor}"

class Notebook(models.Model):
    id_not = models.AutoField(primary_key=True)
    marca_not = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.marca_not} (ID: {self.id_not})"

class EjemplarNotebook(models.Model):
    notebook = models.ForeignKey(Notebook, related_name='ejemplares', on_delete=models.CASCADE)
    registro = models.CharField(max_length=100)
    modelo = models.CharField(max_length=255)

    def __str__(self):
        return f"Registro: {self.registro} - Modelo: {self.modelo}"

class Programa(models.Model):
    profesor = models.CharField(max_length=255)
    url = models.URLField(max_length=500)
    carrera = models.CharField(max_length=255)
    materia = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.materia} - {self.profesor}"

class Proyector(models.Model):
    id_proyector = models.AutoField(primary_key=True)
    marca_pro = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.marca_pro} (ID: {self.id_proyector})"

class EjemplarProyector(models.Model):
    proyector = models.ForeignKey(Proyector, related_name='ejemplares', on_delete=models.CASCADE)
    registro = models.CharField(max_length=100)
    modelo = models.CharField(max_length=255)

    def __str__(self):
        return f"Registro: {self.registro} - Modelo: {self.modelo}"

class Varios(models.Model):
    sede = models.CharField(max_length=255)
    # Otros campos generales si los necesitas

    def __str__(self):
        return f"Varios en sede: {self.sede}"

class TipoVarios(models.Model):
    varios = models.ForeignKey(Varios, related_name='tipos', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)  # Ej: "Silla", "Mesa", etc.

    def __str__(self):
        return f"{self.nombre} ({self.varios})"

class EjemplarVarios(models.Model):
    tipo_varios = models.ForeignKey(TipoVarios, related_name='ejemplares', on_delete=models.CASCADE)
    registro = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"Registro: {self.registro} - {self.tipo_varios.nombre}"