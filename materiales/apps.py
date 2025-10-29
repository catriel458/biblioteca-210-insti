from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver


class MaterialesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'materiales'
    
    def ready(self):
        """
        Se ejecuta cuando la aplicación está lista.
        Conecta las señales para crear usuarios automáticamente.
        """
        # Importar aquí para evitar problemas de importación circular
        from django.contrib.auth import get_user_model
        
        @receiver(post_migrate, sender=self)
        def crear_bibliotecarias_automaticamente(sender, **kwargs):
            """
            Crea automáticamente las bibliotecarias después de las migraciones
            """
            try:
                Usuario = get_user_model()
                
                # Usuario 1: Bibliotecaria principal (del backend)
                dni_bibliotecaria = '35135884'
                if not Usuario.objects.filter(dni=dni_bibliotecaria).exists():
                    bibliotecaria = Usuario.objects.create_user(
                        dni=dni_bibliotecaria,
                        password='Biblioteca210',
                        nombre='Bibliotecaria',
                        apellido='Principal',
                        email='biblioteca@insti.edu.ar',
                        perfil='bibliotecaria',
                        is_staff=True,
                        is_superuser=True
                    )
                    print(f"✓ Usuario bibliotecaria principal creado automáticamente: {bibliotecaria.dni}")
                
                # Usuario 2: Nicolas Caprio (del sistema insti)
                dni_nicolas = '41293236'
                if not Usuario.objects.filter(dni=dni_nicolas).exists():
                    nicolas = Usuario.objects.create_user(
                        dni=dni_nicolas,
                        password='12345678',
                        nombre='Nicolas',
                        apellido='Caprio',
                        email='nicocaprio@outlook.com',
                        perfil='bibliotecaria',
                        is_staff=True,
                        is_superuser=True
                    )
                    print(f"✓ Usuario Nicolas Caprio creado automáticamente: {nicolas.dni}")
                else:
                    # Actualizar el perfil si ya existe pero no es bibliotecaria
                    nicolas = Usuario.objects.get(dni=dni_nicolas)
                    if nicolas.perfil != 'bibliotecaria':
                        nicolas.perfil = 'bibliotecaria'
                        nicolas.is_staff = True
                        nicolas.is_superuser = True
                        nicolas.save()
                        print(f"✓ Usuario Nicolas Caprio actualizado a bibliotecaria: {nicolas.dni}")
                    
            except Exception as e:
                print(f"Error al crear bibliotecarias automáticamente: {e}")
