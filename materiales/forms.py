# forms.py - REEMPLAZAR LibroForm completo

from django import forms
from .models import Libro, Mapas, Multimedia, Notebook, Proyector, Varios
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import Usuario
from .models import Programa

class LibroForm(forms.ModelForm):
    # Opciones para sede
    SEDE_CHOICES = [
        ('LA_PLATA', 'La Plata'),
        ('ABASTO', 'Abasto'),
    ]
    
    # Opciones para disponibilidad
    DISPONIBILIDAD_CHOICES = [
        ('AULA', 'Aula'),
        ('SALON', 'Salon'),
    ]
    
    # Redefinir campos con widgets personalizados
    sede = forms.ChoiceField(
        choices=SEDE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    
    disponibilidad = forms.ChoiceField(
        choices=DISPONIBILIDAD_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    
    class Meta:
        model = Libro
        fields = [
            'titulo', 'autor', 'editorial', 'descripcion',
            'siglas_autor_titulo', 'clasificacion_cdu', 
            'etiqueta_palabra_clave', 'sede', 'disponibilidad', 
            'observaciones', 'img'
        ]
        
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el título del libro', 'required': True}),
            'autor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el autor del libro', 'required': True}),
            'editorial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la editorial', 'required': True}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ingrese una descripción del libro'}),
            'siglas_autor_titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese las siglas del autor y título', 'required': True}),
            'clasificacion_cdu': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la clasificación CDU', 'required': True}),
            'etiqueta_palabra_clave': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ingrese palabras clave separadas por comas'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observaciones sobre este ejemplar'}),
            'img': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'URL de la imagen del libro'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Hacer campos obligatorios
        self.fields['titulo'].required = True
        self.fields['siglas_autor_titulo'].required = True
        self.fields['sede'].required = True
        self.fields['disponibilidad'].required = True
        
        # Hacer campos opcionales
        self.fields['autor'].required = False
        self.fields['editorial'].required = False
        self.fields['clasificacion_cdu'].required = False
        self.fields['img'].required = False
        self.fields['img'].help_text = 'Ingrese la URL completa de la imagen del libro'
        self.fields['descripcion'].required = False
        self.fields['etiqueta_palabra_clave'].required = False
        self.fields['observaciones'].required = False
        self.fields['etiqueta_palabra_clave'].initial = ''
        
    def clean_img(self):
        """Validación personalizada para imagen URL"""
        img_url = self.cleaned_data.get('img')
        
        # Si está vacío, permitirlo
        if not img_url:
            return ''
            
        return img_url

# Mantener el resto de formularios igual
class MapaForm(forms.ModelForm):
    # Opciones para sede
    SEDE_CHOICES = [
        ('LA_PLATA', 'La Plata'),
        ('ABASTO', 'Abasto'),
    ]
    
    # Redefinir campos con widgets personalizados
    sede = forms.ChoiceField(
        choices=SEDE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    
    class Meta:
        model = Mapas
        fields = ['id_mapa', 'tipo', 'sede', 'denominacion', 'descripcion']
        
        widgets = {
            'id_mapa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ID del mapa'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tipo de mapa', 'required': True}),
            'denominacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Denominación del mapa', 'required': True}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción del mapa'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer campos explícitamente requeridos
        self.fields['tipo'].required = True
        self.fields['denominacion'].required = True
        self.fields['sede'].required = True

class MultimediaEditForm(forms.ModelForm):
    # Carreras REALES del Instituto Superior de Formación Docente y Técnica Nº 210
    CARRERA_CHOICES = [
        ('', 'Seleccione una carrera'),
        # PROFESORADOS
        ('Profesorado de Educación Inicial', 'Profesorado de Educación Inicial'),
        ('Profesorado de Educación Primaria', 'Profesorado de Educación Primaria'),  
        ('Profesorado de Educación Secundaria en Geografía', 'Profesorado de Educación Secundaria en Geografía'),
        # TECNICATURAS
        ('Tecnicatura Superior en Análisis de Sistemas', 'Tecnicatura Superior en Análisis de Sistemas'),
        ('Tecnicatura Superior en Enfermería', 'Tecnicatura Superior en Enfermería'),
        ('Tecnicatura Superior en Acompañamiento Terapéutico', 'Tecnicatura Superior en Acompañamiento Terapéutico'),
        ('Tecnicatura Superior en Higiene y Seguridad en el Trabajo', 'Tecnicatura Superior en Higiene y Seguridad en el Trabajo'),
    ]

    ESTADO_CHOICES = [
        ('Disponible', 'Disponible'),
        ('No disponible', 'No disponible'),
        ('En reparación', 'En reparación'),
        ('Dado de baja', 'Dado de baja'),
    ]

    # Materias organizadas por carrera (usando las mismas que MultimediaForm)
    MATERIAS_POR_CARRERA = {
        'Profesorado de Educación Inicial': [
            "Análisis del Mundo Contemporáneo",
            "Ateneo de Naturaleza y Sociedad",
            "Ateneo de Matemática",
            "Ateneo de Nuevas Expresiones Estéticas",
            "Ateneo de Prácticas del Lenguaje y la Literatura",
            "Corporeidad y Motricidad",
            "Cultura, Comunicación y Educación",
            "Didáctica de la Matemática",
            "Didáctica de las Ciencias Naturales",
            "Didáctica de las Ciencias Sociales",
            "Didáctica de las Prácticas del Lenguaje y la Literatura",
            "Didáctica General",
            "Didáctica y Curriculum de Nivel Inicial",
            "Dimensión Ético-Política de la Praxis Docente",
            "Educación en y para la Salud",
            "Educación Física Escolar",
            "Educación Musical",
            "Educación Plástica",
            "Educación Temprana",
            "Filosofía",
            "Historia y Prospectiva de la Educación",
            "Juego y Desarrollo Infantil",
            "Medios Audiovisuales, TICs y Educación",
            "Pedagogía",
            "Política, Legislación y Administración del Trabajo Escolar",
            "Práctica Docente 1",
            "Práctica Docente 2",
            "Práctica Docente 3",
            "Práctica Docente 4",
            "Psicología del Desarrollo y el Aprendizaje 1",
            "Psicología del Desarrollo y el Aprendizaje 2",
            "Psicología Social e Institucional",
            "Reflexión Filosófica de la Educación",
            "Taller de Ciencias Naturales",
            "Taller de Ciencias Sociales",
            "Taller de Definición Institucional",
            "Taller de Lectura, Escritura y Oralidad (LEO)",
            "Taller de Literatura Infantil",
            "Taller de la Matemática",
            "Taller de Materiales y Objetos Lúdicos",
            "Taller de Pensamiento Lógico Matemático",
            "Teorías Sociopolíticas y Educación",
            "Trayectos Formativos Opcionales"
        ],
        'Profesorado de Educación Primaria': [
            'Análisis del Mundo Contemporáneo', 'Arte y Educación', 'Ateneo de Ciencias Naturales',
            'Ateneo de Ciencias Sociales', 'Ateneo de Matemática', 'Ateneo de Prácticas del Lenguaje y la Literatura',
            'Configuraciones Culturales del Sujeto Educativo de Primaria', 'Corporeidad y Motricidad',
            'Cultura, Comunicación y Educación', 'Didáctica de la Matemática 1', 'Didáctica de la Matemática 2',
            'Didáctica de las Ciencias Naturales 1', 'Didáctica de las Ciencias Naturales 2',
            'Didáctica de las Ciencias Sociales 1', 'Didáctica de las Ciencias Sociales 2',
            'Didáctica de Prácticas del Lenguaje y la Literatura 1', 'Didáctica de Prácticas del Lenguaje y la Literatura 2',
            'Didáctica General', 'Didáctica y Curriculum de Nivel Primario', 'Dimensión Ético-Política de la Praxis Docente',
            'Educación Artística', 'Educación Física Escolar', 'Filosofía', 'Historia y Prospectiva de la Educación',
            'Medios Audiovisuales, TICs y Educación', 'Pedagogía', 'Pedagogía Crítica de las Diferencias',
            'Política, Legislación y Administración del Trabajo Escolar', 'Práctica Docente 1',
            'Práctica Docente 2', 'Práctica Docente 3', 'Práctica Docente 4',
            'Psicología del Desarrollo y el Aprendizaje 1', 'Psicología del Desarrollo y el Aprendizaje 2',
            'Psicología Social e Institucional', 'Reflexión Filosófica de la Educación',
            'Taller de Definición Institucional', 'Taller de Lectura, Escritura y Oralidad (LEO)',
            'Taller de Pensamiento Lógico Matemático', 'Teorías Sociopolíticas y Educación',
            'Trayectos Formativos Opcionales'
        ],
        'Profesorado de Educación Secundaria en Geografía': [
            'Antropología', 'Cartografía', 'Cartografía Digital', 'Cultura Digital y Educación',
            'Derechos, Interculturalidad y Ciudadanía', 'Didáctica de la Geografía', 'Didáctica de las Ciencias Sociales',
            'Didáctica y Curriculum', 'Economía Política', 'Educación Sexual Integral (ESI)',
            'Educación y Transformaciones Sociales Contemporáneas', 'Enseñanza de la Geografía',
            'Espacio de Opción Institucional (EOI)', 'Geografía Ambiental', 'Geografía Ambiental de América Latina',
            'Geografía Ambiental de Argentina', 'Geografía Cultural', 'Geografía de Género',
            'Geografía Económica y Social Argentina', 'Geografía Política y Geopolítica', 'Geografía Rural',
            'Geografía Social', 'Geografía Social de América Latina', 'Geografía Urbana',
            'Historia de los Modelos Económicos de Argentina', 'Historia Social General',
            'Introducción a las Ciencias Sociales y a la Geografía',
            'Organización Económica del Espacio',
            'Pedagogía',
            'Práctica Docente 1',
            'Práctica Docente 2',
            'Práctica Docente 3',
            'Práctica Docente 4',
            'Problemas Ambientales Locales/Regionales: La Investigación en el Aula',
            'Problemas Filosóficos de la Educación',
            'Política Educativa Argentina',
            'Psicología del Aprendizaje',
            'Reflexión Filosófico-Política de la Práctica Docente',
            'Sociología',
            'Teoría y Metodología en Geografía',
            'Trayectorias Educativas de Jóvenes y Adultos',
            'Unidades Curriculares Optativas'
        ],
        'Tecnicatura Superior en Análisis de Sistemas': [
            "Álgebra",
            "Algoritmos y estructuras de datos 1",
            "Algoritmos y estructuras de datos 2",
            "Algoritmos y estructuras de datos 3",
            "Análisis Matemático 1",
            "Análisis Matemático 2",
            "Arquitectura de Computadores",
            "Aspectos legales de la Profesión",
            "Base de Datos",
            "Ciencia, Tecnología y Sociedad",
            "Estadística",
            "Ingeniería de Software 1",
            "Ingeniería de Software 2",
            "Inglés 1",
            "Inglés 2",
            "Inglés 3",
            "Prácticas Profesionalizantes 1",
            "Prácticas Profesionalizantes 2",
            "Prácticas Profesionalizantes 3",
            "Redes y Comunicaciones",
            "Seminario de actualización",
            "Sistemas Operativos",
            "Sistemas y Organizaciones"
        ],
        'Tecnicatura Superior en Enfermería': [
            "Aspectos Bioéticos y Legales de la Profesión",
            "Biología Humana",
            "Comunicación en Ciencias de la Salud",
            "Condiciones y Medio Ambiente del Trabajo",
            "Cuidados de la Salud Centrados en la Comunidad y la Familia",
            "Enfermería Comunitaria y Prácticas Educativas en Salud",
            "Enfermería del Adulto y del Adulto Mayor I",
            "Enfermería del Adulto y el Adulto Mayor II",
            "Enfermería en Emergencias y Catástrofes",
            "Enfermería en Salud Mental",
            "Enfermería Materno Infantil",
            "Farmacología en Enfermería",
            "Fundamentos del Cuidado",
            "Inglés",
            "Introducción a la Metodología de Investigación en Salud",
            "Nutrición y Dietoterapia",
            "Organización y Gestión de Servicios de Enfermería",
            "Prácticas Profesionalizantes 1",
            "Prácticas Profesionalizantes 2",
            "Prácticas Profesionalizantes 3",
            "Psicología",
            "Salud Pública 1",
            "Salud Pública 2",
            "Teorías Socioculturales de la Salud"
        ],
        'Tecnicatura Superior en Acompañamiento Terapéutico': [
            "Acompañamiento Terapéutico del Adulto y Adulto Mayor",
            "Acompañamiento Terapéutico en la Niñez y Adolescencia",
            "Acompañamiento Terapéutico",
            "Contextualización del Campo Profesional del Acompañamiento Terapéutico",
            "Ética",
            "Fundamentos de Psicología General y de Intervención Sociocomunitaria",
            "Inglés",
            "Intervención Comunitaria y Recursos Sociales",
            "Investigación en Salud",
            "Modalidades de Intervención en el Acompañamiento Terapéutico",
            "Modelo de Ocupación Humana",
            "Organización y Gestión de los Servicios de Salud Mental",
            "Prácticas Profesionalizantes I",
            "Prácticas Profesionalizantes II",
            "Prácticas Profesionalizantes III",
            "Principios Médicos y de Psicofarmacología",
            "Psicofarmacología",
            "Psicología de los Ciclos Vitales",
            "Psicología de Grupos",
            "Psicopatología",
            "Salud Pública y Salud Mental",
            "Sistemas Familiares"
        ],
        'Tecnicatura Superior en Higiene y Seguridad en el Trabajo': [
            "Administración de las Organizaciones",
            "Capacitación de Personal",
            "Comunicación y Administración de Medios",
            "Control de la Contaminación",
            "Derecho del Trabajo",
            "Ergonomía",
            "Estadística",
            "Física 1",
            "Física 2",
            "Higiene Laboral y Medio Ambiente 1",
            "Higiene Laboral y Medio Ambiente 2",
            "Inglés Técnico",
            "Medicina del Trabajo 1",
            "Medicina del Trabajo 2",
            "Medios de Representación",
            "Práctica Profesionalizante 1",
            "Práctica Profesionalizante 2",
            "Práctica Profesionalizante 3",
            "Psicología Laboral",
            "Química 1",
            "Química 2",
            "Seguridad 1",
            "Seguridad 2",
            "Seguridad 3"
        ]
    }

    carrera = forms.ChoiceField(
        choices=CARRERA_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control form-control-sm',
            'id': 'id_carrera_edit'
        }),
        required=False
    )

    materia = forms.ChoiceField(
        choices=[('', 'Seleccione primero una carrera')],
        widget=forms.Select(attrs={
            'class': 'form-control form-control-sm',
            'id': 'id_materia_edit'
        }),
        required=True
    )

    estado = forms.ChoiceField(
        choices=ESTADO_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control form-control-sm'
        }),
        required=False
    )

    class Meta:
        model = Multimedia
        fields = ['profesor', 'carrera', 'materia', 'ingresar_enlace', 'titulo_contenido']
        
        widgets = {
            'profesor': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Ingrese el nombre del profesor'
            }),
            'ingresar_enlace': forms.URLInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'https://ejemplo.com/contenido.pdf'
            }),
            'titulo_contenido': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Ingrese el título del contenido'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Determinar la carrera seleccionada (desde POST data o instancia)
        carrera_seleccionada = None
        
        # Priorizar datos POST si están disponibles (para manejar cambios dinámicos)
        if self.data and 'carrera' in self.data:
            carrera_seleccionada = self.data.get('carrera')
        # Si no hay datos POST, usar la carrera de la instancia
        elif self.instance and self.instance.pk and self.instance.carrera:
            carrera_seleccionada = self.instance.carrera
        
        # Configurar las opciones de materia según la carrera seleccionada
        if carrera_seleccionada and carrera_seleccionada in self.MATERIAS_POR_CARRERA:
            materias_choices = [('', 'Seleccione una materia')] + [
                (materia, materia) for materia in self.MATERIAS_POR_CARRERA[carrera_seleccionada]
            ]
            self.fields['materia'].choices = materias_choices

class MultimediaForm(forms.ModelForm):
    # Carreras REALES del Instituto Superior de Formación Docente y Técnica Nº 210
    CARRERA_CHOICES = [
        ('', 'Seleccione una carrera'),
        # PROFESORADOS
        ('Profesorado de Educación Inicial', 'Profesorado de Educación Inicial'),
        ('Profesorado de Educación Primaria', 'Profesorado de Educación Primaria'),  
        ('Profesorado de Educación Secundaria en Geografía', 'Profesorado de Educación Secundaria en Geografía'),
        # TECNICATURAS
        ('Tecnicatura Superior en Análisis de Sistemas', 'Tecnicatura Superior en Análisis de Sistemas'),
        ('Tecnicatura Superior en Enfermería', 'Tecnicatura Superior en Enfermería'),
        ('Tecnicatura Superior en Acompañamiento Terapéutico', 'Tecnicatura Superior en Acompañamiento Terapéutico'),
    ]

    # Materias organizadas por carrera
    MATERIAS_POR_CARRERA = {
            'Profesorado de Educación Inicial': [
                "Análisis del Mundo Contemporáneo",
                "Ateneo de Naturaleza y Sociedad",
                "Ateneo de Matemática",
                "Ateneo de Nuevas Expresiones Estéticas",
                "Ateneo de Prácticas del Lenguaje y la Literatura",
                "Corporeidad y Motricidad",
                "Cultura, Comunicación y Educación",
                "Didáctica de la Matemática",
                "Didáctica de las Ciencias Naturales",
                "Didáctica de las Ciencias Sociales",
                "Didáctica de las Prácticas del Lenguaje y la Literatura",
                "Didáctica General",
                "Didáctica y Curriculum de Nivel Inicial",
                "Dimensión Ético-Política de la Praxis Docente",
                "Educación en y para la Salud",
                "Educación Física Escolar",
                "Educación Musical",
                "Educación Plástica",
                "Educación Temprana",
                "Filosofía",
                "Historia y Prospectiva de la Educación",
                "Juego y Desarrollo Infantil",
                "Medios Audiovisuales, TICs y Educación",
                "Pedagogía",
                "Política, Legislación y Administración del Trabajo Escolar",
                "Práctica Docente 1",
                "Práctica Docente 2",
                "Práctica Docente 3",
                "Práctica Docente 4",
                "Psicología del Desarrollo y el Aprendizaje 1",
                "Psicología del Desarrollo y el Aprendizaje 2",
                "Psicología Social e Institucional",
                "Reflexión Filosófica de la Educación",
                "Taller de Ciencias Naturales",
                "Taller de Ciencias Sociales",
                "Taller de Definición Institucional",
                "Taller de Lectura, Escritura y Oralidad (LEO)",
                "Taller de Literatura Infantil",
                "Taller de la Matemática",
                "Taller de Materiales y Objetos Lúdicos",
                "Taller de Pensamiento Lógico Matemático",
                "Teorías Sociopolíticas y Educación",
                "Trayectos Formativos Opcionales"
            ],
            'Profesorado de Educación Primaria': [
                "Análisis del Mundo Contemporáneo",
                "Arte y Educación",
                "Ateneo de Ciencias Naturales",
                "Ateneo de Ciencias Sociales",
                "Ateneo de Matemática",
                "Ateneo de Prácticas del Lenguaje y la Literatura",
                "Configuraciones Culturales del Sujeto Educativo de Primaria",
                "Corporeidad y Motricidad",
                "Cultura, Comunicación y Educación",
                "Didáctica de la Matemática 1",
                "Didáctica de la Matemática 2",
                "Didáctica de las Ciencias Naturales 1",
                "Didáctica de las Ciencias Naturales 2",
                "Didáctica de las Ciencias Sociales 1",
                "Didáctica de las Ciencias Sociales 2",
                "Didáctica de Prácticas del Lenguaje y la Literatura 1",
                "Didáctica de Prácticas del Lenguaje y la Literatura 2",
                "Didáctica General",
                "Didáctica y Curriculum de Nivel Primario",
                "Dimensión Ético-Política de la Praxis Docente",
                "Educación Artística",
                "Educación Física Escolar",
                "Filosofía",
                "Historia y Prospectiva de la Educación",
                "Medios Audiovisuales, TICs y Educación",
                "Pedagogía",
                "Pedagogía Crítica de las Diferencias",
                "Política, Legislación y Administración del Trabajo Escolar",
                "Práctica Docente 1",
                "Práctica Docente 2",
                "Práctica Docente 3",
                "Práctica Docente 4",
                "Psicología del Desarrollo y el Aprendizaje 1",
                "Psicología del Desarrollo y el Aprendizaje 2",
                "Psicología Social e Institucional",
                "Reflexión Filosófica de la Educación",
                "Taller de Definición Institucional",
                "Taller de Lectura, Escritura y Oralidad (LEO)",
                "Taller de Pensamiento Lógico Matemático",
                "Teorías Sociopolíticas y Educación",
                "Trayectos Formativos Opcionales"
            ],
            'Profesorado de Educación Secundaria en Geografía': [
                "Antropología",
                "Cartografía",
                "Cartografía Digital",
                "Cultura Digital y Educación",
                "Derechos, Interculturalidad y Ciudadanía",
                "Didáctica de la Geografía",
                "Didáctica de las Ciencias Sociales",
                "Didáctica y Curriculum",
                "Economía Política",
                "Educación Sexual Integral (ESI)",
                "Educación y Transformaciones Sociales Contemporáneas",
                "Enseñanza de la Geografía",
                "Espacio de Opción Institucional (EOI)",
                "Geografía Ambiental",
                "Geografía Ambiental de América Latina",
                "Geografía Ambiental de Argentina",
                "Geografía Cultural",
                "Geografía de Género",
                "Geografía Económica y Social Argentina",
                "Geografía Política y Geopolítica",
                "Geografía Rural",
                "Geografía Social",
                "Geografía Social de América Latina",
                "Geografía Urbana",
                "Historia de los Modelos Económicos de Argentina",
                "Historia Social General",
                "Introducción a las Ciencias Sociales y a la Geografía",
                "Organización Económica del Espacio",
                "Pedagogía",
                "Práctica Docente 1",
                "Práctica Docente 2",
                "Práctica Docente 3",
                "Práctica Docente 4",
                "Problemas Ambientales Locales/Regionales: La Investigación en el Aula",
                "Problemas Filosóficos de la Educación",
                "Política Educativa Argentina",
                "Psicología del Aprendizaje",
                "Reflexión Filosófico-Política de la Práctica Docente",
                "Sociología",
                "Teoría y Metodología en Geografía",
                "Trayectorias Educativas de Jóvenes y Adultos",
                "Unidades Curriculares Optativas"
            ],
            'Profesorado de Educación Secundaria en Ciencias Políticas': [
                "Análisis de las Instituciones Educativas",
                "Antropología",
                "Cultura Digital y Educación",
                "Derecho",
                "Derechos Humanos y Ciudadanía",
                "Derechos, Interculturalidad y Ciudadanía",
                "Didáctica de la Ciencia Política",
                "Didáctica de las Ciencias Sociales",
                "Didáctica y Curriculum",
                "Economía Política",
                "Educación y Transformaciones Sociales Contemporáneas",
                "Educación Sexual Integral (ESI)",
                "Espacio de Opción Institucional (EOI)",
                "Estado, Administración y Políticas Públicas",
                "Estado y Política de Género",
                "Fundamentos de Ciencia Política",
                "Geografía",
                "Historia Argentina",
                "Historia Latinoamericana",
                "Historia Mundial",
                "Investigación en la Enseñanza de la Ciencia Política",
                "Opinión Pública, Medios y Política",
                "Pedagogía",
                "Pensamiento Político Pedagógico Latinoamericano",
                "Política Educativa Argentina",
                "Práctica Docente 1",
                "Práctica Docente 2",
                "Práctica Docente 3",
                "Práctica Docente 4",
                "Problemas Filosóficos de la Educación",
                "Problemática y Política Ambiental",
                "Psicología del Aprendizaje",
                "Reflexión Filosófico-Política de la Práctica Docente",
                "Sistemas Políticos Comparados",
                "Sociología",
                "Teoría de las Relaciones Internacionales y Política Internacional",
                "Teoría Política 1",
                "Teoría Política 2",
                "Teoría Política 3",
                "Teoría y Derecho Constitucional",
                "Unidades Curriculares Optativas"
            ],
            'Tecnicatura Superior en Análisis de Sistemas': [
                "Álgebra",
                "Algoritmos y estructuras de datos 1",
                "Algoritmos y estructuras de datos 2",
                "Algoritmos y estructuras de datos 3",
                "Análisis Matemático 1",
                "Análisis Matemático 2",
                "Arquitectura de Computadores",
                "Aspectos legales de la Profesión",
                "Base de Datos",
                "Ciencia, Tecnología y Sociedad",
                "Estadística",
                "Ingeniería de Software 1",
                "Ingeniería de Software 2",
                "Inglés 1",
                "Inglés 2",
                "Inglés 3",
                "Prácticas Profesionalizantes 1",
                "Prácticas Profesionalizantes 2",
                "Prácticas Profesionalizantes 3",
                "Redes y Comunicaciones",
                "Seminario de actualización",
                "Sistemas Operativos",
                "Sistemas y Organizaciones"
            ],
            'Tecnicatura Superior en Enfermería': [
                "Aspectos Bioéticos y Legales de la Profesión",
                "Biología Humana",
                "Comunicación en Ciencias de la Salud",
                "Condiciones y Medio Ambiente del Trabajo",
                "Cuidados de la Salud Centrados en la Comunidad y la Familia",
                "Enfermería Comunitaria y Prácticas Educativas en Salud",
                "Enfermería del Adulto y del Adulto Mayor I",
                "Enfermería del Adulto y el Adulto Mayor II",
                "Enfermería en Emergencias y Catástrofes",
                "Enfermería en Salud Mental",
                "Enfermería Materno Infantil",
                "Farmacología en Enfermería",
                "Fundamentos del Cuidado",
                "Inglés",
                "Introducción a la Metodología de Investigación en Salud",
                "Nutrición y Dietoterapia",
                "Organización y Gestión de Servicios de Enfermería",
                "Prácticas Profesionalizantes 1",
                "Prácticas Profesionalizantes 2",
                "Prácticas Profesionalizantes 3",
                "Psicología",
                "Salud Pública 1",
                "Salud Pública 2",
                "Teorías Socioculturales de la Salud"
            ],
            'Tecnicatura Superior en Acompañamiento Terapéutico': [
                "Acompañamiento Terapéutico del Adulto y Adulto Mayor",
                "Acompañamiento Terapéutico en la Niñez y Adolescencia",
                "Acompañamiento Terapéutico",
                "Contextualización del Campo Profesional del Acompañamiento Terapéutico",
                "Ética",
                "Fundamentos de Psicología General y de Intervención Sociocomunitaria",
                "Inglés",
                "Intervención Comunitaria y Recursos Sociales",
                "Investigación en Salud",
                "Modalidades de Intervención en el Acompañamiento Terapéutico",
                "Modelo de Ocupación Humana",
                "Organización y Gestión de los Servicios de Salud Mental",
                "Prácticas Profesionalizantes I",
                "Prácticas Profesionalizantes II",
                "Prácticas Profesionalizantes III",
                "Principios Médicos y de Psicofarmacología",
                "Psicofarmacología",
                "Psicología de los Ciclos Vitales",
                "Psicología de Grupos",
                "Psicopatología",
                "Salud Pública y Salud Mental",
                "Sistemas Familiares"
            ],
            'Tecnicatura Superior en Higiene y Seguridad en el Trabajo': [
                "Administración de las Organizaciones",
                "Capacitación de Personal",
                "Comunicación y Administración de Medios",
                "Control de la Contaminación",
                "Derecho del Trabajo",
                "Ergonomía",
                "Estadística",
                "Física 1",
                "Física 2",
                "Higiene Laboral y Medio Ambiente 1",
                "Higiene Laboral y Medio Ambiente 2",
                "Inglés Técnico",
                "Medicina del Trabajo 1",
                "Medicina del Trabajo 2",
                "Medios de Representación",
                "Práctica Profesionalizante 1",
                "Práctica Profesionalizante 2",
                "Práctica Profesionalizante 3",
                "Psicología Laboral",
                "Química 1",
                "Química 2",
                "Seguridad 1",
                "Seguridad 2",
                "Seguridad 3"
        ]
    }
    
    class Meta:
        model = Multimedia
        fields = ['profesor', 'carrera', 'materia', 'ingresar_enlace', 'titulo_contenido']
        
        widgets = {
            'profesor': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Ingrese el nombre del profesor'
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
                'placeholder': 'https://ejemplo.com/contenido.pdf'
            }),
            'titulo_contenido': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Ingrese el título del contenido'
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

class NotebookForm(forms.ModelForm):
    class Meta:
        model = Notebook
        fields = ['sede', 'num_registro', 'modelo_not', 'num_ejemplar']
        
        widgets = {
            'sede': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('La Plata', 'La Plata'),
                ('Abasto', 'Abasto'),
            ]),
            'num_registro': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo_not': forms.TextInput(attrs={'class': 'form-control'}),
            'num_ejemplar': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer campos explícitamente requeridos
        self.fields['sede'].required = True
        self.fields['num_registro'].required = True

class ProyectorForm(forms.ModelForm):
    class Meta:
        model = Proyector
        fields = ['id_proyector', 'sede', 'num_registro', 'modelo_pro']
        
        widgets = {
            'id_proyector': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el ID del proyector'}),
            'sede': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('', 'Seleccione una sede'),
                ('La Plata', 'La Plata'),
                ('Abasto', 'Abasto'),
            ]),
            'num_registro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el número de registro'}),
            'modelo_pro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el modelo del proyector'}),
        }

class VariosForm(forms.ModelForm):
    class Meta:
        model = Varios
        fields = ['id_varios', 'tipo', 'sede', 'cantidad', 'cantidad_disponible']

        widgets = {
            'id_varios': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el ID del artículo'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el tipo de artículo'}),
            'sede': forms.Select(attrs={'class': 'form-control'}, choices=[('La Plata', 'La Plata'), ('Abasto', 'Abasto')]),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'Cantidad total'}),
            'cantidad_disponible': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'Cantidad disponible'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer que cantidad_disponible sea igual a cantidad por defecto en nuevos registros
        if not self.instance.pk:
            self.fields['cantidad_disponible'].initial = self.fields['cantidad'].initial or 1

class RegistroForm(UserCreationForm):
    nombre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su nombre'}))
    apellido = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su apellido'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su correo electrónico'}))
    dni = forms.CharField(max_length=8, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su DNI (7-8 dígitos)'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su contraseña'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme su contraseña'}))
    
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
        widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': True, 'placeholder': 'Ingrese su DNI'}),
        label='DNI'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su contraseña'}),
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
    password_actual = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su contraseña actual'}))
    password_nueva = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su nueva contraseña'}))
    password_confirmar = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme su nueva contraseña'}))
    
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
            'Análisis del Mundo Contemporáneo', 'Ateneo de Naturaleza y Sociedad', 'Ateneo de Matemática',
            'Ateneo de Nuevas Expresiones Estéticas', 'Ateneo de Prácticas del Lenguaje y la Literatura',
            'Corporeidad y Motricidad', 'Cultura, Comunicación y Educación', 'Didáctica de la Matemática',
            'Didáctica de las Ciencias Naturales', 'Didáctica de las Ciencias Sociales',
            'Didáctica de las Prácticas del Lenguaje y la Literatura', 'Didáctica General',
            'Didáctica y Curriculum de Nivel Inicial', 'Dimensión Ético-Política de la Praxis Docente',
            'Educación en y para la Salud', 'Educación Física Escolar', 'Educación Musical',
            'Educación Plástica', 'Educación Temprana', 'Filosofía', 'Historia y Prospectiva de la Educación',
            'Juego y Desarrollo Infantil', 'Medios Audiovisuales, TICs y Educación', 'Pedagogía',
            'Política, Legislación y Administración del Trabajo Escolar', 'Práctica Docente 1',
            'Práctica Docente 2', 'Práctica Docente 3', 'Práctica Docente 4',
            'Psicología del Desarrollo y el Aprendizaje 1', 'Psicología del Desarrollo y el Aprendizaje 2',
            'Psicología Social e Institucional', 'Reflexión Filosófica de la Educación',
            'Taller de Ciencias Naturales', 'Taller de Ciencias Sociales', 'Taller de Definición Institucional',
            'Taller de Lectura, Escritura y Oralidad (LEO)', 'Taller de Literatura Infantil',
            'Taller de la Matemática', 'Taller de Materiales y Objetos Lúdicos',
            'Taller de Pensamiento Lógico Matemático', 'Teorías Sociopolíticas y Educación',
            'Trayectos Formativos Opcionales'
        ],
        'Profesorado de Educación Primaria': [
            'Análisis del Mundo Contemporáneo', 'Arte y Educación', 'Ateneo de Ciencias Naturales',
            'Ateneo de Ciencias Sociales', 'Ateneo de Matemática', 'Ateneo de Prácticas del Lenguaje y la Literatura',
            'Configuraciones Culturales del Sujeto Educativo de Primaria', 'Corporeidad y Motricidad',
            'Cultura, Comunicación y Educación', 'Didáctica de la Matemática 1', 'Didáctica de la Matemática 2',
            'Didáctica de las Ciencias Naturales 1', 'Didáctica de las Ciencias Naturales 2',
            'Didáctica de las Ciencias Sociales 1', 'Didáctica de las Ciencias Sociales 2',
            'Didáctica de Prácticas del Lenguaje y la Literatura 1', 'Didáctica de Prácticas del Lenguaje y la Literatura 2',
            'Didáctica General', 'Didáctica y Curriculum de Nivel Primario', 'Dimensión Ético-Política de la Praxis Docente',
            'Educación Artística', 'Educación Física Escolar', 'Filosofía', 'Historia y Prospectiva de la Educación',
            'Medios Audiovisuales, TICs y Educación', 'Pedagogía', 'Pedagogía Crítica de las Diferencias',
            'Política, Legislación y Administración del Trabajo Escolar', 'Práctica Docente 1',
            'Práctica Docente 2', 'Práctica Docente 3', 'Práctica Docente 4',
            'Psicología del Desarrollo y el Aprendizaje 1', 'Psicología del Desarrollo y el Aprendizaje 2',
            'Psicología Social e Institucional', 'Reflexión Filosófica de la Educación',
            'Taller de Definición Institucional', 'Taller de Lectura, Escritura y Oralidad (LEO)',
            'Taller de Pensamiento Lógico Matemático', 'Teorías Sociopolíticas y Educación',
            'Trayectos Formativos Opcionales'
        ],
        'Profesorado de Educación Secundaria en Ciencias Políticas': [
            'Análisis de las Instituciones Educativas', 'Antropología', 'Cultura Digital y Educación',
            'Derecho', 'Derechos Humanos y Ciudadanía', 'Derechos, Interculturalidad y Ciudadanía',
            'Didáctica de la Ciencia Política', 'Didáctica de las Ciencias Sociales', 'Didáctica y Curriculum',
            'Economía Política', 'Educación y Transformaciones Sociales Contemporáneas', 'Educación Sexual Integral (ESI)',
            'Espacio de Opción Institucional (EOI)', 'Estado, Administración y Políticas Públicas',
            'Estado y Política de Género', 'Fundamentos de Ciencia Política', 'Geografía',
            'Historia Argentina', 'Historia Latinoamericana', 'Historia Mundial',
            'Investigación en la Enseñanza de la Ciencia Política', 'Opinión Pública, Medios y Política',
            'Pedagogía', 'Pensamiento Político Pedagógico Latinoamericano', 'Política Educativa Argentina',
            'Práctica Docente 1', 'Práctica Docente 2', 'Práctica Docente 3', 'Práctica Docente 4',
            'Problemas Filosóficos de la Educación', 'Problemática y Política Ambiental', 'Psicología del Aprendizaje',
            'Reflexión Filosófico-Política de la Práctica Docente', 'Sistemas Políticos Comparados',
            'Sociología', 'Teoría de las Relaciones Internacionales y Política Internacional',
            'Teoría Política 1', 'Teoría Política 2', 'Teoría Política 3', 'Teoría y Derecho Constitucional',
            'Unidades Curriculares Optativas'
        ],
        'Profesorado de Educación Secundaria en Geografía': [
            'Antropología', 'Cartografía', 'Cartografía Digital', 'Cultura Digital y Educación',
            'Derechos, Interculturalidad y Ciudadanía', 'Didáctica de la Geografía', 'Didáctica de las Ciencias Sociales',
            'Didáctica y Curriculum', 'Economía Política', 'Educación Sexual Integral (ESI)',
            'Educación y Transformaciones Sociales Contemporáneas', 'Enseñanza de la Geografía',
            'Espacio de Opción Institucional (EOI)', 'Geografía Ambiental', 'Geografía Ambiental de América Latina',
            'Geografía Ambiental de Argentina', 'Geografía Cultural', 'Geografía de Género',
            'Geografía Económica y Social Argentina', 'Geografía Política y Geopolítica', 'Geografía Rural',
            'Geografía Social', 'Geografía Social de América Latina', 'Geografía Urbana',
            'Historia de los Modelos Económicos de Argentina', 'Historia Social General',
            'Introducción a las Ciencias Sociales y a la Geografía', 'Organización Económica del Espacio',
            'Pedagogía', 'Práctica Docente 1', 'Práctica Docente 2', 'Práctica Docente 3', 'Práctica Docente 4',
            'Problemas Ambientales Locales/Regionales: La Investigación en el Aula', 'Problemas Filosóficos de la Educación',
            'Política Educativa Argentina', 'Psicología del Aprendizaje', 'Reflexión Filosófico-Política de la Práctica Docente',
            'Sociología', 'Teoría y Metodología en Geografía', 'Trayectorias Educativas de Jóvenes y Adultos',
            'Unidades Curriculares Optativas'
        ],
        'Tecnicatura Superior en Acompañamiento Terapéutico': [
            'Acompañamiento Terapéutico del Adulto y Adulto Mayor', 'Acompañamiento Terapéutico en la Niñez y Adolescencia',
            'Acompañamiento Terapéutico', 'Contextualización del Campo Profesional del Acompañamiento Terapéutico',
            'Ética', 'Fundamentos de Psicología General y de Intervención Sociocomunitaria', 'Inglés',
            'Intervención Comunitaria y Recursos Sociales', 'Investigación en Salud',
            'Modalidades de Intervención en el Acompañamiento Terapéutico', 'Modelo de Ocupación Humana',
            'Organización y Gestión de los Servicios de Salud Mental', 'Prácticas Profesionalizantes I',
            'Prácticas Profesionalizantes II', 'Prácticas Profesionalizantes III', 'Principios Médicos y de Psicofarmacología',
            'Psicofarmacología', 'Psicología de los Ciclos Vitales', 'Psicología de Grupos', 'Psicopatología',
            'Salud Pública y Salud Mental', 'Sistemas Familiares'
        ],
        'Tecnicatura Superior en Análisis de Sistemas': [
            'Álgebra', 'Algoritmos y estructuras de datos 1', 'Algoritmos y estructuras de datos 2',
            'Algoritmos y estructuras de datos 3', 'Análisis Matemático 1', 'Análisis Matemático 2',
            'Arquitectura de Computadores', 'Aspectos legales de la Profesión', 'Base de Datos',
            'Ciencia, Tecnología y Sociedad', 'Estadística', 'Ingeniería de Software 1', 'Ingeniería de Software 2',
            'Inglés 1', 'Inglés 2', 'Inglés 3', 'Prácticas Profesionalizantes 1', 'Prácticas Profesionalizantes 2',
            'Prácticas Profesionalizantes 3', 'Redes y Comunicaciones', 'Seminario de actualización',
            'Sistemas Operativos', 'Sistemas y Organizaciones'
        ],
        'Tecnicatura Superior en Enfermería': [
            'Aspectos Bioéticos y Legales de la Profesión', 'Biología Humana', 'Comunicación en Ciencias de la Salud',
            'Condiciones y Medio Ambiente del Trabajo', 'Cuidados de la Salud Centrados en la Comunidad y la Familia',
            'Enfermería Comunitaria y Prácticas Educativas en Salud', 'Enfermería del Adulto y del Adulto Mayor I',
            'Enfermería del Adulto y el Adulto Mayor II', 'Enfermería en Emergencias y Catástrofes',
            'Enfermería en Salud Mental', 'Enfermería Materno Infantil', 'Farmacología en Enfermería',
            'Fundamentos del Cuidado', 'Inglés', 'Introducción a la Metodología de Investigación en Salud',
            'Nutrición y Dietoterapia', 'Organización y Gestión de Servicios de Enfermería',
            'Prácticas Profesionalizantes 1', 'Prácticas Profesionalizantes 2', 'Prácticas Profesionalizantes 3',
            'Psicología', 'Salud Pública 1', 'Salud Pública 2', 'Teorías Socioculturales de la Salud'
        ],
        'Tecnicatura Superior en Higiene y Seguridad en el Trabajo': [
            'Administración de las Organizaciones', 'Capacitación de Personal', 'Comunicación y Administración de Medios',
            'Control de la Contaminación', 'Derecho del Trabajo', 'Ergonomía', 'Estadística',
            'Física 1', 'Física 2', 'Higiene Laboral y Medio Ambiente 1', 'Higiene Laboral y Medio Ambiente 2',
            'Inglés Técnico', 'Medicina del Trabajo 1', 'Medicina del Trabajo 2', 'Medios de Representación',
            'Práctica Profesionalizante 1', 'Práctica Profesionalizante 2', 'Práctica Profesionalizante 3',
            'Psicología Laboral', 'Química 1', 'Química 2', 'Seguridad 1', 'Seguridad 2', 'Seguridad 3'
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
        
        # Configurar campos como requeridos
        self.fields['profesor'].required = True
        self.fields['carrera'].required = True
        self.fields['materia'].required = True
        self.fields['ingresar_enlace'].required = True
        self.fields['ciclo_lectivo'].required = True
        
        # Valor inicial eliminado para permitir validación mandatoria correcta