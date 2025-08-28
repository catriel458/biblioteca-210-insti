document.addEventListener("DOMContentLoaded", function () {
    const tipoMaterialSelect = document.getElementById('tipo_material');
    const formContainer = document.getElementById('form-container');
    const cantTituloDescripcionContainer = document.getElementById('cant-titulo-descripcion-container');
    const cargaMasivaInput = document.getElementById('carga_masiva');

    tipoMaterialSelect.addEventListener('change', function () {
        const tipo = tipoMaterialSelect.value;

        if (!tipo) {
            mostrarSoloTipoMaterial();
            return;
        }

        let url = '';
        switch (tipo) {
            case 'libro':
                url = '/biblioteca/formulario/libro/';
                break;
            case 'mapa':
                url = '/biblioteca/formulario/mapa/';
                break;
            case 'multimedia':
                url = '/biblioteca/formulario/multimedia/';
                break;
            case 'proyector':
                url = '/biblioteca/formulario/proyector/';
                break;
            case 'programa':
                url = '/biblioteca/formulario/programa/';
                break;
            case 'notebook':
                url = '/biblioteca/formulario/notebook/';
                break;
        }

        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error al cargar el formulario: ${response.statusText}`);
                }
                return response.text();
            })
            .then(data => {
                formContainer.innerHTML = data;
                //updateRows();
                mostrarCantidadEjemplares();
                //moverElementos();
            })
            .catch(error => {
                console.error('Error al cargar el formulario:', error);
                formContainer.innerHTML = '<p>Error al cargar el formulario. Inténtelo de nuevo más tarde.</p>';
            });
    });

    function mostrarSoloTipoMaterial() {
        formContainer.innerHTML = '';
        cantTituloDescripcionContainer.innerHTML = '';
    }

    function mostrarCantidadEjemplares() {
        const cantEjemplaresHTML = `
            <div class="form-group">
                <label for="cant_ejemplares" style="display: none;">Cant Ejemplares:</label>
                <input type="number" class="form-control" id="cant_ejemplares" name="cant_ejemplares" required min="1">
            </div>
            <div id="dynamic-rows"></div>`;
        
        cantTituloDescripcionContainer.innerHTML = cantEjemplaresHTML;

        const cantEjemplaresInput = document.getElementById('cant_ejemplares');
        if (cantEjemplaresInput) {
            cantEjemplaresInput.addEventListener('input', updateRows);
        }
    }

    function updateRows() {
        const cantEjemplares = parseInt(document.getElementById('cant_ejemplares').value) || 0;
        const dynamicRowsContainer = document.getElementById('dynamic-rows');
        
        // Limpiar filas dinámicas previas
        if (dynamicRowsContainer) {
            dynamicRowsContainer.innerHTML = '';

            // Mostrar u ocultar el contenedor dinámico basado en la cantidad de ejemplares
            if (cantEjemplares > 1) {
                dynamicRowsContainer.classList.remove('hidden');
                
                // Agregar filas basadas en la cantidad de ejemplares
                for (let i = 0; i < cantEjemplares; i++) {
                    // Crear filas 6 y 7
                    const row6 = document.createElement('div');
                    row6.className = 'row mt-2'; // Estilo de fila
                    row6.innerHTML = `
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
                    `;
        
                    const row7 = document.createElement('div');
                    row7.className = 'row mt-2'; // Estilo de fila
                    row7.innerHTML = `
                        <div class="col-10">
                            <label for="observaciones_${i}">Observaciones:</label>
                            <textarea class="form-control auto-expand" id="observaciones_${i}" name="observaciones[]" rows="4">Escriba aquí...</textarea>
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
        
                    // Agregar las filas al contenedor dinámico
                    dynamicRowsContainer.appendChild(row6);
                    dynamicRowsContainer.appendChild(row7);
                }
            } else {
                // Si la cantidad de ejemplares es 1 o menos, ocultar el contenedor dinámico
                dynamicRowsContainer.classList.add('hidden');
            }
        }
    }
    
    cargaMasivaInput.addEventListener('change', function () {
        const fileList = this.files;
        const fileCount = fileList.length;
        const label = this.nextElementSibling;

        label.innerHTML = fileCount > 0 ? `${fileCount} archivo(s) seleccionado(s)` : '';
    });
    
});
