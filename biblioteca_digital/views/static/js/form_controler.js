document.addEventListener("DOMContentLoaded", function () {
    const tipoMaterialSelect = document.getElementById('tipo_material');
    const formContainer = document.getElementById('formulario-especifico');
    const cantEjemplaresInput = document.getElementById('cant_ejemplares');
    const dynamicRowsContainer = document.getElementById('dynamic-rows');
    const buttonsContainer = document.getElementById('buttons-container');
    const cantEjemplaresContainer = document.getElementById('cant_ejemplares_container');

    // Función para cargar el template específico del tipo de material
    async function loadMaterialTemplate(tipo) {
        try {
            const response = await fetch(`/libros/get_material_template/${tipo}/`);
            if (response.ok) {
                return await response.text();
            }
            return '';
        } catch (error) {
            console.error('Error loading template:', error);
            return '';
        }
    }

    // Función para actualizar las filas basado en la cantidad de ejemplares
    function updateRows() {
        if (!tipoMaterialSelect.value) return;
        
        const cantEjemplares = parseInt(cantEjemplaresInput.value) || 0;
        
        // Limpiar filas dinámicas previas
        dynamicRowsContainer.innerHTML = '';
        
        // Mostrar u ocultar el contenedor de filas dinámicas y botones
        const showElements = cantEjemplares > 0;
        dynamicRowsContainer.style.display = showElements ? 'block' : 'none';
        buttonsContainer.style.display = showElements ? 'block' : 'none';
        
        // Si no hay ejemplares, no crear filas
        if (cantEjemplares <= 0) return;
        
        // Agregar filas basadas en la cantidad de ejemplares
        for (let i = 0; i < cantEjemplares; i++) {
            const row = document.createElement('div');
            row.className = 'row mt-3';
            row.innerHTML = `
                <div class="col-2">
                    <label for="numero_ejemplar_${i}">Ejemplar N°:</label>
                    <input type="text" class="form-control" id="numero_ejemplar_${i}" name="numero_ejemplar[]" value="${i + 1}" required readonly>
                </div>
                <div class="col-2">
                    <label for="sede_${i}">Sede:</label>
                    <select class="form-control" id="sede_${i}" name="sede[]" required>
                        <option value="">Selecciona una sede</option>
                        <option value="sede1">La Plata</option>
                        <option value="sede2">Abasto</option>
                    </select>
                </div>
                <div class="col-6">
                    <label for="observaciones_${i}">Observaciones:</label>
                    <textarea class="form-control" id="observaciones_${i}" name="observaciones[]" rows="1">Escriba aquí...</textarea>
                </div>
                <div class="col-2">
                    <label for="disponibilidad_${i}">Disponibilidad:</label>
                    <select class="form-control" id="disponibilidad_${i}" name="disponibilidad[]" required>
                        <option value="">Selecciona disponibilidad</option>
                        <option value="disponible">Disponible</option>
                        <option value="no_disponible">No Disponible</option>
                    </select>
                </div>
            `;
            dynamicRowsContainer.appendChild(row);
        }
    }

    // Asignar la función updateRows al evento input del campo cant_ejemplares
    cantEjemplaresInput.addEventListener('input', updateRows);

    // Manejar cambios en el tipo de material
    tipoMaterialSelect.addEventListener('change', async function () {
        const tipo = tipoMaterialSelect.value;
        
        // Mostrar el campo de cantidad de ejemplares si se selecciona un tipo
        cantEjemplaresContainer.style.display = tipo ? 'block' : 'none';
        
        if (!tipo) {
            formContainer.innerHTML = '';
            dynamicRowsContainer.innerHTML = '';
            dynamicRowsContainer.style.display = 'none';
            buttonsContainer.style.display = 'none';
            return;
        }

        // Cargar el template específico
        const templateContent = await loadMaterialTemplate(tipo);
        if (templateContent) {
            formContainer.innerHTML = templateContent;
        }
        
        // Inicializar las filas dinámicas
        updateRows();
    });
});
