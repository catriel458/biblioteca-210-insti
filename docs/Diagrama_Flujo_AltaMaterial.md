# Diagrama de Flujo - Alta de Material

Este diagrama describe el flujo principal para el alta de materiales en la Biblioteca 210.

```mermaid
flowchart TD
    A[Usuario accede al formulario de alta] --> B[Completa los datos requeridos]
    B --> C[Adjunta imagen o enlace]
    C --> D[Envía el formulario (POST)]
    D --> E[Backend valida los datos]
    E --> F{¿Datos válidos?}
    F -- Sí --> G[Guarda en la base de datos]
    F -- No --> H[Muestra mensaje de error]
    G --> I[Muestra confirmación de alta]
    H --> B
```

## Explicación
1. El usuario accede al formulario y completa los campos.
2. Adjunta una imagen o pega un enlace.
3. Envía el formulario.
4. El backend valida los datos.
5. Si todo es válido, se guarda el material y se muestra una confirmación.
6. Si hay errores, se informa al usuario y puede corregirlos.
