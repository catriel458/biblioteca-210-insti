from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from .models import Libro


class CargarCSVTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_cargar_csv_libro_inserta_en_bd(self):
        csv_content = (
            'tipo_material,titulo,autor,editorial,clasificacion_cdu,siglas_autor_titulo,sede,disponibilidad,observaciones,img,num_ejemplar\n'
            'Libro,El Principito,Antoine de Saint-Exupéry,Reynal & Hitchcock,859.7,SAI,La Plata,Disponible,,https://example.com/img.jpg,1\n'
        ).encode('utf-8')

        uploaded = SimpleUploadedFile(
            'libros.csv',
            csv_content,
            content_type='text/csv'
        )

        response = self.client.post(reverse('cargar_csv'), {'csv_file': uploaded})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Libro.objects.count(), 1)
        libro = Libro.objects.first()
        self.assertEqual(libro.titulo, 'El Principito')
        self.assertEqual(libro.autor, 'Antoine de Saint-Exupéry')
        self.assertEqual(libro.clasificacion_cdu, '859.7')
