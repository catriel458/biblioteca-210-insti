# forms.py - REEMPLAZAR LibroForm completo

from django import forms
from .models import Libro, Mapas, Multimedia, Notebook, Proyector, Varios
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import Usuario

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
        fields = ['id_not','sede', 'num_registro', 'modelo_not']

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