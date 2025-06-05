document.addEventListener('DOMContentLoaded', function() {
    // Función para obtener el valor de un campo
    function getFieldValue(fieldId, index = null) {
        let field;
        try {
            if (index !== null) {
                field = document.getElementById(`${fieldId}_${index}`);
                if (!field) {
                    // Intentar obtener el valor del campo usando el nombre del campo con índice
                    const fields = document.getElementsByName(`${fieldId}[${index}]`);
                    if (fields.length > 0) field = fields[0];
                }
            } else {
                field = document.getElementById(fieldId);
                if (!field) {
                    // Intentar obtener el valor del campo usando el nombre del campo
                    const fields = document.getElementsByName(fieldId);
                    if (fields.length > 0) field = fields[0];
                }
            }

            if (!field) return '';
            
            // Si es un select, obtener el texto de la opción seleccionada
            if (field.tagName === 'SELECT' && field.selectedOptions.length > 0) {
                return field.selectedOptions[0].text;
            }

            // Si es un campo de palabras clave, formatear correctamente
            if (fieldId === 'palabras_clave') {
                return field.value.split(',').map(palabra => palabra.trim()).filter(palabra => palabra).join(', ');
            }

            return field.value || '';
        } catch (error) {
            console.error(`Error al obtener el valor del campo ${fieldId}:`, error);
            return '';
        }
    }

    // Función para actualizar el contenido del modal
    function actualizarModalConfirmacion() {
        try {
            // Obtener valores del formulario
            const tipoMaterial = getFieldValue('tipo_material').toUpperCase();
            document.getElementById('confirmTipoMaterial').textContent = tipoMaterial;
            document.getElementById('confirmTitulo').textContent = getFieldValue('titulo');
            document.getElementById('confirmAutor').textContent = getFieldValue('autor');
            document.getElementById('confirmEditorial').textContent = getFieldValue('editorial');
            document.getElementById('confirmDescripcion').textContent = getFieldValue('descripcion');
            document.getElementById('confirmSiglasAutor').textContent = getFieldValue('siglas_autor_titulo');
            document.getElementById('confirmClasificacion').textContent = getFieldValue('clasificacion_cdu');
            document.getElementById('confirmPalabrasClave').textContent = getFieldValue('palabras_clave');

            // Obtener la cantidad de ejemplares
            const cantEjemplares = parseInt(getFieldValue('cant_ejemplares')) || 1;
            
            // Limpiar el contenedor de ejemplares
            const ejemplaresContainer = document.getElementById('ejemplaresContainer');
            ejemplaresContainer.innerHTML = '';

            // Generar la información para cada ejemplar
            for (let i = 0; i < cantEjemplares; i++) {
                const ejemplarDiv = document.createElement('div');
                ejemplarDiv.className = 'ejemplar-info mb-3';
                ejemplarDiv.innerHTML = `
                    <h6 class="text-primary mb-2">Ejemplar ${i + 1}</h6>
                    <div class="row g-3">
                        <div class="col-md-4">
                            <strong>Sede:</strong>
                            <p class="info-text">${getFieldValue('sede', i) || 'No especificada'}</p>
                        </div>
                        <div class="col-md-4">
                            <strong>Disponibilidad:</strong>
                            <p class="info-text">${getFieldValue('disponibilidad', i) || 'No especificada'}</p>
                        </div>
                        <div class="col-md-4">
                            <strong>Observaciones:</strong>
                            <p class="info-text">${getFieldValue('observaciones', i) || 'Sin observaciones'}</p>
                        </div>
                    </div>
                `;
                ejemplaresContainer.appendChild(ejemplarDiv);
            }

            // Actualizar campos adicionales
            document.getElementById('confirmSede').textContent = getFieldValue('sede', 0) || 'No especificada';
            document.getElementById('confirmDisponibilidad').textContent = getFieldValue('disponibilidad', 0) || 'No especificada';
            document.getElementById('confirmEjemplarNum').textContent = cantEjemplares.toString();
            document.getElementById('confirmObservaciones').textContent = getFieldValue('observaciones', 0) || 'Sin observaciones';

        } catch (error) {
            console.error('Error al actualizar el modal de confirmación:', error);
        }
    }

    // Escuchar el evento de apertura del modal
    const modalConfirmacion = document.getElementById('modalConfirmacionAltaMaterial');
    if (modalConfirmacion) {
        modalConfirmacion.addEventListener('show.bs.modal', actualizarModalConfirmacion);
    }
});