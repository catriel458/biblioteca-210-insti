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
        ('docente', 'Docente'),
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
        
    def tiene_sanciones_activas(self):
        """Verifica si el usuario tiene sanciones activas"""
        return self.sanciones.filter(estado='confirmada').exists()
    
    def get_sanciones_activas(self):
        """Obtiene las sanciones activas del usuario"""
        return self.sanciones.filter(estado='confirmada')
    
    def puede_solicitar_prestamo(self):
        """Verifica si el usuario puede solicitar préstamos"""
        # Verificar sanciones activas
        sanciones_activas = self.sanciones.filter(estado='confirmada')
    
        for sancion in sanciones_activas:
            # Para alumnos: si tiene sanción confirmada, no puede (lógica existente)
            if sancion.tipo_usuario_sancion == 'alumno':
                return False
        
        # Para docentes: verificar si la suspensión está vigente
            elif sancion.tipo_usuario_sancion == 'docente':
                if sancion.fecha_suspension_hasta and timezone.now() < sancion.fecha_suspension_hasta:
                    return False
    
        return True

    def tiene_sanciones_criticas(self):
        """Verifica si el docente tiene 3 o más sanciones"""
        if self.perfil != 'bibliotecaria':  # Solo verificar para usuarios normales
            sanciones_docente = self.sanciones.filter(
                tipo_usuario_sancion='docente',
                estado='confirmada'
            ).count()
            return sanciones_docente >= 3
        return False

    # En la clase Usuario, agrega estos métodos
    def get_prestamos_activos(self):
        """Obtiene los préstamos activos del usuario"""
        return self.prestamos_usuario.filter(estado__in=['aprobado', 'aprobado_reserva'])

    def puede_solicitar_mas_prestamos(self):
        """Verifica si el usuario puede solicitar más préstamos (máximo 3)"""
        prestamos_activos = self.get_prestamos_activos().count()
        return prestamos_activos < 3

    def get_prestamos_disponibles(self):
        """Retorna cuántos préstamos más puede solicitar"""
        prestamos_activos = self.get_prestamos_activos().count()
        return max(0, 3 - prestamos_activos)

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

     # NUEVOS CAMPOS
    extension_solicitada = models.BooleanField(default=False)
    fecha_extension = models.DateTimeField(null=True, blank=True)
    motivo_extension = models.TextField(blank=True, null=True)
    
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
    
    def tiene_sancion_pendiente(self):
        """Verifica si el préstamo tiene una sanción pendiente"""
        return self.sanciones.filter(estado='pendiente').exists()
    
    def crear_sancion_por_vencimiento(self):
        """Crea una sanción automática por vencimiento (método mejorado)"""
        if self.estado == 'vencido' and self.usuario:
            from .models import Sancion  # Import aquí para evitar circular import
            
            # Verificar que no exista ya una sanción para este préstamo
            sancion_existente = Sancion.objects.filter(prestamo=self).first()
            
            if not sancion_existente:
                fecha_vencimiento = self.fecha_devolucion_programada
                ahora = timezone.now()
                
                # Calcular tiempo de retraso
                if fecha_vencimiento:
                    retraso = ahora - fecha_vencimiento
                    dias_retraso = retraso.days
                    horas_retraso = retraso.seconds // 3600
                    minutos_retraso = (retraso.seconds % 3600) // 60
                    
                    if dias_retraso > 0:
                        tiempo_retraso = f"{dias_retraso} días y {horas_retraso} horas"
                    elif horas_retraso > 0:
                        tiempo_retraso = f"{horas_retraso} horas y {minutos_retraso} minutos"
                    else:
                        tiempo_retraso = f"{minutos_retraso} minutos"
                    
                    motivo_detallado = f'Préstamo vencido del libro "{self.libro.titulo}". Venció el {fecha_vencimiento.strftime("%d/%m/%Y a las %H:%M:%S")}. Retraso: {tiempo_retraso}.'
                else:
                    motivo_detallado = f'Préstamo vencido del libro "{self.libro.titulo}"'
                
                sancion = Sancion.objects.create(
                    usuario=self.usuario,
                    prestamo=self,
                    tipo_sancion='inhabilitacion_mesas',
                    motivo=motivo_detallado
                )
                
                print(f"[DEBUG] Sanción automática creada: ID {sancion.id_sancion} para préstamo {self.id_prestamo}")
                return sancion
            else:
                print(f"[DEBUG] Ya existe sanción para préstamo {self.id_prestamo}")
                return sancion_existente
        
        return None

    # En el modelo Prestamo, corregir el método puede_extender_prestamo:

    def puede_extender_prestamo(self):
        """Verifica si el préstamo puede ser extendido (solo docentes)"""
        # Verificar que el usuario existe y es docente
        if not self.usuario:
            return False
        
        # CORRECCIÓN 1: Verificar tanto 'docente' como 'profesor'
        if self.usuario.perfil not in ['docente', 'profesor']:
            return False
        
        # CORRECCIÓN 2: Solo préstamos activos pueden extenderse
        if self.estado != 'aprobado':
            return False
        
        # CORRECCIÓN 3: Solo se puede extender una vez
        if self.extension_solicitada:
            return False
        
        # CORRECCIÓN 4: Debe tener fecha de devolución programada
        if not self.fecha_devolucion_programada:
            return False
        
        # CORRECCIÓN 5: Permitir extensión cuando quedan 7 días o menos (más flexible)
        from django.utils import timezone
        tiempo_restante = self.fecha_devolucion_programada - timezone.now()
        dias_restantes = tiempo_restante.days
        
        # Permitir extensión si quedan 7 días o menos, o si ya está vencido
        return dias_restantes <= 7 or tiempo_restante.total_seconds() <= 0

    # TAMBIÉN AGREGAR ESTE MÉTODO AUXILIAR:
    def get_tiempo_restante_texto(self):
        """Retorna el tiempo restante en formato texto"""
        if self.estado != 'aprobado' or not self.fecha_devolucion_programada:
            return "N/A"
        
        from django.utils import timezone
        tiempo_restante = self.fecha_devolucion_programada - timezone.now()
        
        if tiempo_restante.total_seconds() <= 0:
            return "VENCIDO"
        
        dias = tiempo_restante.days
        horas = tiempo_restante.seconds // 3600
        
        if dias > 0:
            return f"{dias} días, {horas} horas"
        else:
            return f"{horas} horas"
    
    def esta_proximo_a_vencer(self):
        """Verifica si el préstamo vence en menos de 24 horas"""
        if self.estado == 'aprobado' and self.fecha_devolucion_programada:
            horas_restantes = (self.fecha_devolucion_programada - timezone.now()).total_seconds() / 3600
            return 0 < horas_restantes <= 24
        return False
    
    def extender_prestamo(self, motivo=""):
        """Extiende el préstamo por 15 días adicionales"""
        if self.puede_extender_prestamo():
            self.fecha_devolucion_programada += datetime.timedelta(days=15)
            self.extension_solicitada = True
            self.fecha_extension = timezone.now()
            self.motivo_extension = motivo
            self.save()
            return True
        return False
            
class Sancion(models.Model):
    TIPO_CHOICES = (
        ('inhabilitacion_mesas', 'Inhabilitación para Mesas de Final'),
        ('suspension_prestamos', 'Suspensión de Préstamos'),
    )
    
    ESTADO_CHOICES = (
        ('pendiente', 'Pendiente de Revisión'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
        ('cumplida', 'Cumplida/Finalizada'),
    )
    
    # AGREGAR ESTOS NUEVOS CAMPOS
    TIPO_USUARIO_SANCION_CHOICES = (
        ('alumno', 'Alumno'),
        ('docente', 'Docente'),
    )
    
    id_sancion = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='sanciones')
    prestamo = models.ForeignKey(Prestamo, on_delete=models.CASCADE, related_name='sanciones')
    tipo_sancion = models.CharField(max_length=30, choices=TIPO_CHOICES, default='inhabilitacion_mesas')
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='pendiente')
    
    # NUEVO CAMPO PARA TIPO DE USUARIO
    tipo_usuario_sancion = models.CharField(
        max_length=10, 
        choices=TIPO_USUARIO_SANCION_CHOICES, 
        default='alumno',
        help_text="Tipo de usuario al que se aplica la sanción"
    )
    
    # NUEVOS CAMPOS PARA DOCENTES
    fecha_suspension_hasta = models.DateTimeField(
        null=True, 
        blank=True,
        help_text="Fecha hasta la que está suspendido el docente (3 meses)"
    )
    
    acumulado_sanciones = models.IntegerField(
        default=0,
        help_text="Número de sanciones acumuladas del docente"
    )
    
    # Campos existentes
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_confirmacion = models.DateTimeField(null=True, blank=True)
    fecha_finalizacion = models.DateTimeField(null=True, blank=True)
    motivo = models.TextField(default='Préstamo vencido')
    observaciones_bibliotecaria = models.TextField(blank=True, null=True)
    libro_devuelto_catalogo = models.BooleanField(default=False)
    fecha_devolucion_catalogo = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"Sanción {self.id_sancion} - {self.usuario.get_full_name()} - {self.get_estado_display()}"
    
    def esta_activa(self):
        if self.estado != 'confirmada':
            return False
        
        # Para docentes, verificar si la suspensión ha expirado
        if self.tipo_usuario_sancion == 'docente' and self.fecha_suspension_hasta:
            from django.utils import timezone
            return timezone.now() < self.fecha_suspension_hasta
        
        return True
    
    # NUEVOS MÉTODOS
    def calcular_fecha_suspension_docente(self):
        """Calcula la fecha de suspensión (3 meses desde confirmación)"""
        if self.fecha_confirmacion:
            import datetime
            return self.fecha_confirmacion + datetime.timedelta(days=90)  # 3 meses
        return None
    
    def verificar_acumulado_critico(self):
        """Verifica si el docente tiene 3 o más sanciones confirmadas"""
        if self.tipo_usuario_sancion == 'docente' and self.usuario:
            sanciones_confirmadas = Sancion.objects.filter(
                usuario=self.usuario,
                tipo_usuario_sancion='docente',
                estado='confirmada'
            ).count()
            return sanciones_confirmadas >= 3
        return False