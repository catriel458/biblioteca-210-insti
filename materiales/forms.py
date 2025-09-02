# forms.py - REEMPLAZAR LibroForm completo

from django import forms
from .models import Libro, Mapas, Multimedia, Notebook, Proyector, Varios
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import Usuario
from .models import Programa

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = [
            'titulo', 'autor', 'editorial', 'descripcion',
            'siglas_autor_titulo', 'clasificacion_cdu', 
            'etiqueta_palabra_clave', #'num_inventario',
            'sede', 'disponibilidad', 'observaciones', 
            'num_ejemplar', 'img'
        ]
        
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'autor': forms.TextInput(attrs={'class': 'form-control'}),
            'editorial': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'siglas_autor_titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'clasificacion_cdu': forms.TextInput(attrs={'class': 'form-control'}),
            'etiqueta_palabra_clave': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            #'num_inventario': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'sede': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('', 'Seleccione una sede'),
                ('La Plata', 'La Plata'),
                ('Abasto', 'Abasto'),
            ]),
            'disponibilidad': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('', 'Seleccione disponibilidad'),
                ('Aula', 'Aula'),
                ('Domicilio', 'Domicilio'),
            ]),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'num_ejemplar': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'img': forms.URLInput(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Hacer campos opcionales
        self.fields['img'].required = False
        self.fields['img'].help_text = 'Ingrese la URL completa de la imagen del libro'
        self.fields['autor'].required = False
        self.fields['editorial'].required = False
        self.fields['descripcion'].required = False
        self.fields['clasificacion_cdu'].required = False
        self.fields['etiqueta_palabra_clave'].required = False
        self.fields['observaciones'].required = False
        
    def clean_img(self):
        """Validación personalizada para imagen URL"""
        img_url = self.cleaned_data.get('img')
        
        # Si está vacío, permitirlo
        if not img_url:
            return ''
            
        return img_url

# Mantener el resto de formularios igual
class MapaForm(forms.ModelForm):
    class Meta:
        model = Mapas
        fields = ['id_mapa', 'tipo', 'descripcion', 'num_ejemplar']

class MultimediaForm(forms.ModelForm):
    class Meta:
        model = Multimedia
        fields = ['id_inventario', 'profesor', 'carrera', 'materia', 'ingresar_enlace', 'titulo_contenido']

class NotebookForm(forms.ModelForm):
    class Meta:
        model = Notebook
        fields = ['sede', 'num_registro', 'modelo_not', 'marca', 'num_ejemplar']
        
        widgets = {
            'sede': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('', 'Seleccione una sede'),
                ('La Plata', 'La Plata'),
                ('Abasto', 'Abasto'),
            ]),
            'num_registro': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo_not': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'num_ejemplar': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

class ProyectorForm(forms.ModelForm):
    class Meta:
        model = Proyector
        fields = ['id_proyector', 'sede', 'num_registro', 'modelo_pro']

class VariosForm(forms.ModelForm):
    class Meta:
        model = Varios
        fields = ['id_varios', 'tipo', 'descripcion', 'num_ejemplar']

class RegistroForm(UserCreationForm):
    nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellido = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    dni = forms.CharField(max_length=8, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Usuario
        fields = ('dni', 'nombre', 'apellido', 'email', 'password1', 'password2')
    
    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if not dni.isdigit():
            raise forms.ValidationError('El DNI solo debe contener números.')
        if len(dni) < 7 or len(dni) > 8:
            raise forms.ValidationError('El DNI debe tener entre 7 y 8 dígitos.')
        if Usuario.objects.filter(dni=dni).exists():
            raise forms.ValidationError('Ya existe un usuario con este DNI.')
        return dni
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError('Ya existe un usuario con este email.')
        return email

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=8,
        widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': True}),
        label='DNI'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Contraseña'
    )
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError('DNI o contraseña incorrectos.')
            else:
                self.confirm_login_allowed(self.user_cache)
        
        return self.cleaned_data

class CambiarPasswordForm(forms.Form):
    password_actual = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_nueva = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirmar = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean_password_actual(self):
        password_actual = self.cleaned_data.get('password_actual')
        if not self.user.check_password(password_actual):
            raise forms.ValidationError('La contraseña actual es incorrecta.')
        return password_actual
    
    def clean(self):
        cleaned_data = super().clean()
        password_nueva = cleaned_data.get('password_nueva')
        password_confirmar = cleaned_data.get('password_confirmar')
        
        if password_nueva and password_confirmar:
            if password_nueva != password_confirmar:
                raise forms.ValidationError('Las contraseñas no coinciden.')
        
        return cleaned_data
    
class ProgramaForm(forms.ModelForm):
    # Carreras REALES del Instituto Superior de Formación Docente y Técnica Nº 210
    CARRERA_CHOICES = [
        ('', 'Seleccione una carrera'),
        # PROFESORADOS
        ('Profesorado de Educación Inicial', 'Profesorado de Educación Inicial'),
        ('Profesorado de Educación Primaria', 'Profesorado de Educación Primaria'),  
        ('Profesorado de Educación Secundaria en Geografía', 'Profesorado de Educación Secundaria en Geografía'),
        ('Profesorado de Educación Secundaria en Ciencias Políticas', 'Profesorado de Educación Secundaria en Ciencias Políticas'),
        # TECNICATURAS
        ('Tecnicatura Superior en Análisis de Sistemas', 'Tecnicatura Superior en Análisis de Sistemas'),
        ('Tecnicatura Superior en Enfermería', 'Tecnicatura Superior en Enfermería'),
        ('Tecnicatura Superior en Acompañamiento Terapéutico', 'Tecnicatura Superior en Acompañamiento Terapéutico'),
        ('Tecnicatura Superior en Higiene y Seguridad en el Trabajo', 'Tecnicatura Superior en Higiene y Seguridad en el Trabajo'),
    ]

    # Materias organizadas por carrera
    MATERIAS_POR_CARRERA = {
        'Profesorado de Educación Inicial': [
            'Pedagogía', 'Psicología Educacional', 'Sociología de la Educación', 
            'Historia y Política de la Educación Argentina', 'Filosofía de la Educación',
            'Didáctica General', 'Curriculum y Didáctica del Nivel Inicial', 
            'Juego y Desarrollo Infantil', 'Literatura Infantil', 'Matemática y su Didáctica',
            'Ciencias Sociales y su Didáctica', 'Ciencias Naturales y su Didáctica',
            'Lengua y su Didáctica', 'Educación Artística', 'Educación Física',
            'Práctica Docente I', 'Práctica Docente II', 'Práctica Docente III', 'Práctica Docente IV'
        ],
        'Profesorado de Educación Primaria': [
            'Pedagogía', 'Psicología Educacional', 'Sociología de la Educación',
            'Historia y Política de la Educación Argentina', 'Filosofía de la Educación',
            'Didáctica General', 'Curriculum y Didáctica del Nivel Primario',
            'Matemática y su Didáctica I', 'Matemática y su Didáctica II',
            'Lengua y su Didáctica I', 'Lengua y su Didáctica II',
            'Ciencias Sociales y su Didáctica I', 'Ciencias Sociales y su Didáctica II',
            'Ciencias Naturales y su Didáctica I', 'Ciencias Naturales y su Didáctica II',
            'Educación Artística', 'Educación Física', 'Tecnologías de la Información',
            'Práctica Docente I', 'Práctica Docente II', 'Práctica Docente III', 'Práctica Docente IV'
        ],
        'Profesorado de Educación Secundaria en Geografía': [
            'Pedagogía', 'Psicología Educacional', 'Sociología de la Educación',
            'Historia y Política de la Educación Argentina', 'Filosofía de la Educación',
            'Didáctica General', 'Didáctica de la Geografía',
            'Geografía Física I', 'Geografía Física II', 'Geografía Humana I', 'Geografía Humana II',
            'Geografía de América', 'Geografía de Argentina', 'Geografía Mundial',
            'Cartografía', 'Climatología', 'Geomorfología', 'Biogeografía',
            'Geografía Económica', 'Geografía Urbana y Rural', 'Epistemología de la Geografía',
            'Práctica Docente I', 'Práctica Docente II', 'Práctica Docente III', 'Práctica Docente IV'
        ],
        'Profesorado de Educación Secundaria en Ciencias Políticas': [
            'Pedagogía', 'Psicología Educacional', 'Sociología de la Educación',
            'Historia y Política de la Educación Argentina', 'Filosofía de la Educación',
            'Didáctica General', 'Didáctica de las Ciencias Políticas',
            'Teoría Política', 'Historia del Pensamiento Político', 'Sistemas Políticos Comparados',
            'Política Argentina', 'Política Latinoamericana', 'Relaciones Internacionales',
            'Derecho Constitucional', 'Sociología Política', 'Economía Política',
            'Filosofía Política', 'Metodología de la Investigación Social',
            'Práctica Docente I', 'Práctica Docente II', 'Práctica Docente III', 'Práctica Docente IV'
        ],
        'Tecnicatura Superior en Análisis de Sistemas': [
            'Matemática', 'Inglés Técnico', 'Arquitectura de Computadoras',
            'Sistemas Operativos', 'Algoritmos y Estructuras de Datos',
            'Programación I', 'Programación II', 'Programación III',
            'Base de Datos I', 'Base de Datos II', 'Análisis de Sistemas I', 'Análisis de Sistemas II',
            'Ingeniería de Software', 'Redes y Comunicaciones', 'Seguridad Informática',
            'Desarrollo Web', 'Programación Orientada a Objetos', 'Metodologías de Desarrollo',
            'Gestión de Proyectos', 'Práctica Profesionalizante I', 'Práctica Profesionalizante II'
        ],
        'Tecnicatura Superior en Enfermería': [
            'Anatomía y Fisiología I', 'Anatomía y Fisiología II', 'Microbiología y Parasitología',
            'Farmacología', 'Patología', 'Nutrición y Dietoterapia',
            'Enfermería Básica', 'Enfermería Médica', 'Enfermería Quirúrgica',
            'Enfermería Materno Infantil', 'Enfermería Pediátrica', 'Enfermería Geriátrica',
            'Enfermería en Salud Mental', 'Enfermería Comunitaria', 'Administración en Enfermería',
            'Bioética', 'Epidemiología', 'Primeros Auxilios',
            'Práctica Profesional I', 'Práctica Profesional II', 'Práctica Profesional III'
        ],
        'Tecnicatura Superior en Acompañamiento Terapéutico': [
            'Psicología General', 'Psicopatología', 'Neurociencias', 'Desarrollo Humano',
            'Teorías y Técnicas de Acompañamiento Terapéutico', 'Comunicación Terapéutica',
            'Dinámicas Familiares', 'Integración Social', 'Recreación Terapéutica',
            'Talleres de Expresión', 'Primeros Auxilios', 'Bioética',
            'Legislación en Salud Mental', 'Trabajo Interdisciplinario',
            'Práctica Profesional I', 'Práctica Profesional II', 'Práctica Profesional III'
        ],
        'Tecnicatura Superior en Higiene y Seguridad en el Trabajo': [
            'Matemática', 'Física', 'Química', 'Legislación Laboral',
            'Higiene Industrial I', 'Higiene Industrial II', 'Seguridad Industrial I', 'Seguridad Industrial II',
            'Medicina del Trabajo', 'Toxicología Laboral', 'Ergonomía',
            'Protección contra Incendios', 'Contaminación Ambiental', 'Gestión de Residuos',
            'Capacitación en Seguridad', 'Investigación de Accidentes', 'Auditorías de Seguridad',
            'Gestión de Riesgos', 'Práctica Profesional I', 'Práctica Profesional II'
        ]
    }

    class Meta:
        model = Programa
        fields = [
            'profesor',         # ← Profesor/a
            'carrera',          # ← Carrera (con opciones reales del ISDFyT)
            'materia',          # ← Materia (dropdown dependiente de carrera)
            'ingresar_enlace',  # ← Enlace
            'ciclo_lectivo',    # ← Ciclo lectivo
        ]
        
        widgets = {
            'profesor': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Ingrese el nombre del profesor/a'
            }),
            'carrera': forms.Select(attrs={
                'class': 'form-control form-control-sm',
                'id': 'id_carrera'
            }),
            'materia': forms.Select(attrs={
                'class': 'form-control form-control-sm',
                'id': 'id_materia'
            }),
            'ingresar_enlace': forms.URLInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'https://ejemplo.com/programa.pdf'
            }),
            'ciclo_lectivo': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': '2025'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configurar las opciones de carrera
        self.fields['carrera'].widget.choices = self.CARRERA_CHOICES
        
        # Configurar materia como select vacío inicialmente
        self.fields['materia'].widget.choices = [('', 'Primero seleccione una carrera')]
        
        # Configurar campos opcionales/requeridos
        self.fields['ingresar_enlace'].required = False
        
        # Valores iniciales
        self.fields['ciclo_lectivo'].initial = '2025'