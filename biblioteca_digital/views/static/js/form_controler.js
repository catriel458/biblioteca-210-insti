document.addEventListener("DOMContentLoaded", function () {
    const tipoMaterialSelect = document.getElementById('tipo_material');
    const formContainer = document.getElementById('formulario-especifico');
    const cantEjemplaresInput = document.getElementById('cant_ejemplares');
    const dynamicRowsContainer = document.getElementById('dynamic-rows');
    const buttonsContainer = document.getElementById('buttons-container');
    const cantEjemplaresContainer = document.getElementById('cant_ejemplares_container');
    const uploadSimple = document.getElementById('upload_simple_container');
    const uploadBox = document.getElementById('upload_box_container');

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
        
        const cantEjemplares = parseInt(cantEjemplaresInput.value) || 1;
        
        // Limpiar filas dinámicas previas
        dynamicRowsContainer.innerHTML = '';
        
        // Mostrar u ocultar el contenedor de filas dinámicas y botones
        const showElements = cantEjemplares >= 1;
        dynamicRowsContainer.style.display = showElements ? 'block' : 'none';
        buttonsContainer.style.display = showElements ? 'block' : 'none';
        
        // Si no hay ejemplares, no crear filas
        if (cantEjemplares <= 0) return;
        
        // Agregar filas basadas en la cantidad de ejemplares
        for (let i = 0; i < cantEjemplares; i++) {
            const row = document.createElement('div');
            row.className = 'row mt-3';
            row.innerHTML = `
                <div class="row">
                    <div class="col-2">
                        <label for="numero_ejemplar_${i}">Ejemplar N°:</label>
                        <input type="text" class="form-control" id="numero_ejemplar_${i}" name="numero_ejemplar[]" value="${i + 1}" required readonly style="background-color: transparent !important;">
                    </div>

                    <div class="col-2 d-flex flex-column justify-content-between">
                        <div>
                            <label for="sede_${i}">Sede:</label>
                            <select class="form-control mb-2" id="sede_${i}" name="sede[]" required>
                                <option value="">Aún sin seleccionar</option>
                                <option value="sede1">La Plata</option>
                                <option value="sede2">Abasto</option>
                            </select>
                        </div>
                        <div>
                            <label for="disponibilidad_${i}">Disponibilidad:</label>
                            <select class="form-control" id="disponibilidad_${i}" name="disponibilidad[]" required>
                                <option value="">Aún sin seleccionar</option>
                                <option value="disponible">Disponible</option>
                                <option value="no_disponible">No Disponible</option>
                            </select>
                        </div>
                    </div>

                    <div class="col-6 ">
                        <label for="observaciones_${i}">Observaciones:</label>
                        <textarea class="form-control h-100" id="observaciones_${i}" name="observaciones[]" rows="2" placeholder="Escriba aquí..."></textarea>
                    </div>
                </div>
            `;
            dynamicRowsContainer.appendChild(row);
        }
    }

    // Asignar la función updateRows al evento input del campo cant_ejemplares
    cantEjemplaresInput.addEventListener('input', updateRows);

    // Mostrar/ocultar carga masiva al cargar la página según el valor actual del select
    if (tipoMaterialSelect && uploadSimple && uploadBox) {
        if (tipoMaterialSelect.value) {
            uploadSimple.style.display = 'block';
            uploadBox.style.display = 'block';
        } else {
            uploadSimple.style.display = 'none';
            uploadBox.style.display = 'none';
        }
    }

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

    // Limpiar todos los campos al enviar el formulario
    const form = document.getElementById('form_alta_material');
    if (form) {
        form.addEventListener('submit', function(e) {
            // Espera un poco para no interferir con el submit real (por si es AJAX o normal)
            setTimeout(function() {
                // Limpiar todos los inputs y textareas manualmente
                form.querySelectorAll('input[type="text"], input[type="number"], textarea').forEach(function(input) {
                    input.value = '';
                });
                // Limpiar selects
                form.querySelectorAll('select').forEach(function(select) {
                    select.selectedIndex = 0;
                });
            }, 100);
        });
    }
});
