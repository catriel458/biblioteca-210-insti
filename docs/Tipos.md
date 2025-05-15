# Tipos y Estructuras de Datos del Sistema Biblioteca 210

## 🌐 Tipos Globales

### Interfaces Comunes
- `Inventario`: Interfaz base para recursos de la biblioteca
- `RecursoDigital`: Interfaz para recursos con representación digital

## 📋 Backend (Django Models)

### 📚 Modelo Libro
```python
class Libro(Inventario):
    id_libro: AutoField
    titulo: CharField
    autor: CharField
    editorial: CharField
    edicion: IntegerField
    codigo_materia: CharField
    siglas_autor_titulo: CharField
    num_inventario: IntegerField
    resumen: TextField
    img: URLField
```

#### Campos Detallados de Libro
| Campo | Tipo | Descripción | Restricciones |
|-------|------|-------------|---------------|
| `id_libro` | AutoField | Identificador único | Clave primaria |
| `titulo` | CharField | Título del libro | Máximo 255 caracteres |
| `autor` | CharField | Nombre del autor | Máximo 255 caracteres |
| `editorial` | CharField | Editorial del libro | Máximo 255 caracteres |
| `edicion` | IntegerField | Año de edición | Valor por defecto: 1999 |
| `codigo_materia` | CharField | Código de materia | Valor por defecto: '1' |
| `num_inventario` | IntegerField | Número de inventario | Valor por defecto: 1 |
| `resumen` | TextField | Descripción del libro | Sin límite de caracteres |
| `img` | URLField | URL de imagen de portada | Debe ser URL válida |

### 📦 Otros Modelos de Inventario

#### 🗺️ Mapa
- Hereda de `Inventario`
- Campos específicos para mapas geográficos

#### 💿 Multimedia
- Recursos como CDs, DVDs
- Metadatos de contenido multimedia

#### 💻 Notebook
- Información de equipos portátiles
- Estado y disponibilidad

#### 📽️ Proyector
- Detalles de dispositivos de proyección
- Control de préstamos

### 👥 Modelo de Usuarios
```python
class Usuario(AbstractUser):
    rol: CharField  # admin, bibliotecario, estudiante
    legajo: CharField
    telefono: CharField
    fecha_alta: DateTimeField
```

## 🖥️ Frontend (TypeScript)

### 📊 Interfaces de Presentación
```typescript
interface LibroView {
    id: number;
    titulo: string;
    autor: string;
    disponible: boolean;
    portada: string;
}

interface UsuarioSesion {
    id: number;
    nombre: string;
    rol: 'admin' | 'bibliotecario' | 'estudiante';
}
```

## 🔍 Consideraciones Generales
- Todos los tipos siguen convenciones de nomenclatura en español
- Priorizar inmutabilidad y tipado fuerte
- Validar datos en backend y frontend

**Última actualización:** Mayo 2025

