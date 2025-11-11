from django import forms
from .models import Libro
from .models import Mapas
from .models import Multimedia
from .models import Notebook
from .models import Proyector
from .models import Varios
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import Usuario



class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = [
            'titulo', 
            'autor', 
            'editorial', 
            'clasificacion_cdu',
            'siglas_autor_titulo', 
            'num_inventario',
            'descripcion',  # Campo agregado
            'etiqueta_palabra_clave', 
            'sede',
            'disponibilidad',  # Campo específico de disponibilidad
            'observaciones', 
            'img'
            # Nota: 'estado' se maneja automáticamente desde Inventario
        ]   
            

    
    def clean_num_inventario(self):
        """Valida que el número de inventario sea único"""
        num_inventario = self.cleaned_data.get('num_inventario')
        
        # Si estamos editando un libro existente, excluirlo de la búsqueda
        if self.instance.pk:
            # Estamos editando
            if Libro.objects.filter(num_inventario=num_inventario).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError(
                    f'Ya existe un libro con el número de inventario "{num_inventario}". '
                    f'Por favor, ingrese un número diferente.'
                )
        else:
            # Estamos creando un nuevo libro
            if Libro.objects.filter(num_inventario=num_inventario).exists():
                raise forms.ValidationError(
                    f'Ya existe un libro con el número de inventario "{num_inventario}". '
                    f'Por favor, ingrese un número diferente.'
                )
        
        return num_inventario

class MapaForm(forms.ModelForm):
    class Meta:
        model = Mapas
        fields = ['id_mapa', 'tipo', 'descripcion', 'num_ejemplar']  # Agrega los campos que necesites

class MultimediaForm(forms.ModelForm):
    class Meta:
        model = Multimedia
        fields = ['id_multi', 'materia','contenido', 'descripcion', 'num_ejemplar']  # Agrega los campos que necesites


class NotebookForm(forms.ModelForm):
    class Meta:
        model = Notebook
        fields = ['id_not', 'marca_not','modelo_not', 'descripcion', 'num_ejemplar']  # Agrega los campos que necesites

class ProyectorForm(forms.ModelForm):
    class Meta:
        model = Proyector
        fields = ['id_proyector', 'marca_pro','modelo_pro', 'descripcion', 'num_ejemplar']  # Agrega los campos que necesites

class VariosForm(forms.ModelForm):
    class Meta:
        model = Varios
        fields = ['id_varios', 'tipo', 'descripcion', 'num_ejemplar']  # Agrega los campos 

class RegistroForm(UserCreationForm):
    nombre = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'})
    )
    apellido = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'})
    )
    dni = forms.CharField(
        max_length=8,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12345678'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'})
    )
    
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
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'DNI',
            'autofocus': True
        }),
        label='DNI'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        }),
        label='Contraseña'
    )
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password
            )
            if self.user_cache is None:
                raise forms.ValidationError('DNI o contraseña incorrectos.')
            else:
                self.confirm_login_allowed(self.user_cache)
        
        return self.cleaned_data

class CambiarPasswordForm(forms.Form):
    password_actual = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña actual'})
    )
    password_nueva = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nueva contraseña'})
    )
    password_confirmar = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar nueva contraseña'})
    )
    
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