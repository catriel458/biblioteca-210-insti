# libros/models.py
from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator


# PRIMERO: Manager personalizado para el Usuario
class CustomUserManager(BaseUserManager):
    def create_user(self, dni, password=None, **extra_fields):
        if not dni:
            raise ValueError('El DNI es obligatorio')
        
        user = self.model(dni=dni, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, dni, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('perfil', 'bibliotecaria')
        
        return self.create_user(dni, password, **extra_fields)


# SEGUNDO: Modelo de Usuario personalizado (ANTES que los demás)
class Usuario(AbstractBaseUser, PermissionsMixin):
    PERFIL_CHOICES = (
        ('alumno', 'Alumno'),
        ('bibliotecaria', 'Bibliotecaria'),
    )
    
    dni_validator = RegexValidator(
        regex=r'^\d{7,8}$',
        message='El DNI debe tener entre 7 y 8 dígitos.'
    )
    
    dni = models.CharField(max_length=8, unique=True, validators=[dni_validator])
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    perfil = models.CharField(max_length=20, choices=PERFIL_CHOICES, default='alumno')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'dni'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'email']
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} (DNI: {self.dni})"
    
    def get_full_name(self):
        return f"{self.nombre} {self.apellido}"
    
    def es_bibliotecaria(self):
        return self.perfil == 'bibliotecaria'


# TERCERO: Resto de modelos (Inventario y sus subclases)
class Inventario(models.Model):
    # Este es el ID principal que usamos para dar de baja, modificar
    id_inventario = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=255, null=True, default="Disponible")
    motivo_baja = models.CharField(max_length=255, null=True)
    descripcion = models.TextField(null=True)
    num_ejemplar = models.IntegerField(null=True)
    imagen_rota = models.ImageField(
        upload_to='imagenes_rota/', null=True, blank=True)

    def __str__(self):
        return f"id_inventario: {self.id_inventario}, estado: {self.estado}, motivo_baja: {self.motivo_baja}, descripcion: {self.descripcion}, numero ejemplar: {self.num_ejemplar}"


class Libro(Inventario):
    id_libro = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    editorial = models.CharField(max_length=255)
    clasificacion_cdu = models.CharField(max_length=255, null=False, default='Sin clasificar')
    siglas_autor_titulo = models.CharField(max_length=255, null=False, default='ABC')
    num_inventario = models.IntegerField(null=False, default=1)
    resumen = models.TextField()
    etiqueta_palabra_clave = models.TextField(default='Roma,Historia,Clasica')
    sede = models.TextField(default='La Plata')
    disponibilidad = models.CharField(max_length=255, null=True, default="Disponible")
    observaciones = models.TextField(default='Esta es una observación')
    img = models.URLField()

    def __str__(self):
        return f"{self.titulo} - {self.autor}"


class Mapas(Inventario):
    id_mapa = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=255)
    
    def __str__(self):
        return f"id_mapa: {self.id_mapa}, tipo: {self.tipo}"


class Multimedia(Inventario):
    id_multi = models.AutoField(primary_key=True)
    materia = models.CharField(max_length=255)
    contenido = models.CharField(max_length=255)
    
    def __str__(self):
        return f"id_multi: {self.id_multi}, materia: {self.materia}, contenido: {self.contenido}"


class Notebook(Inventario):
    id_not = models.AutoField(primary_key=True)
    marca_not = models.CharField(max_length=255)
    modelo_not = models.CharField(max_length=255)
    
    def __str__(self):
        return f"id_not: {self.id_not}, marca_not: {self.marca_not}, modelo_not: {self.modelo_not}"


class Proyector(Inventario):
    id_proyector = models.AutoField(primary_key=True)
    marca_pro = models.CharField(max_length=255)
    modelo_pro = models.CharField(max_length=255)
    
    def __str__(self):
        return f"id_proyector: {self.id_proyector}, marca_pro: {self.marca_pro}, modelo_pro: {self.modelo_pro}"


class Varios(Inventario):
    id_varios = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=255)

    def __str__(self):
        return f"id: {self.id_varios}, tipo: {self.tipo}"


# CUARTO: Modelo de Préstamos (DESPUÉS del Usuario y Libro)
class Prestamo(models.Model):
    ESTADO_CHOICES = (
        ('solicitado', 'Reserva Solicitada'),
        ('aprobado_reserva', 'Reserva Aprobada'),
        ('aprobado', 'Préstamo Activo'),
        ('rechazado', 'Reserva Rechazada'),
        ('finalizado', 'Finalizado'),
        ('vencido', 'Vencido'),
    )
    
    TIPO_CHOICES = (
        ('domicilio', 'Préstamo a Domicilio'),
        ('aula', 'Préstamo en Aula'),
    )
    
    TIPO_USUARIO_CHOICES = (
        ('alumno', 'Alumno'),
        ('profesor', 'Profesor'),
    )
    
    id_prestamo = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='prestamos_usuario', null=True, blank=True)
    nombre_usuario = models.CharField(max_length=255)
    email_usuario = models.EmailField()
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='prestamos')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_aprobacion = models.DateTimeField(null=True, blank=True)
    fecha_devolucion_programada = models.DateTimeField(null=True, blank=True)
    fecha_devolucion_real = models.DateTimeField(null=True, blank=True)
    fecha_limite_reserva = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='solicitado')
    tipo_prestamo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='domicilio')
    tipo_usuario = models.CharField(max_length=10, choices=TIPO_USUARIO_CHOICES, default='alumno')
    motivo_rechazo = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    fecha_retiro_real = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Préstamo {self.id_prestamo} - {self.libro.titulo} - {self.nombre_usuario} - {self.estado}"
    
    def dias_restantes(self):
        if self.estado != 'aprobado' or not self.fecha_devolucion_programada:
            return 0
        
        now = timezone.now()
        delta = self.fecha_devolucion_programada - now
        return max(0, delta.days)
    
    def esta_vencido(self):
        if self.estado != 'aprobado' or not self.fecha_devolucion_programada:
            return False
        
        return timezone.now() > self.fecha_devolucion_programada