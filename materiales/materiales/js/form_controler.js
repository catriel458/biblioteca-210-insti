document.addEventListener("DOMContentLoaded", function () {
    const tipoMaterialSelect = document.getElementById('tipo_material');
    const formContainer = document.getElementById('formulario-especifico');
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
                fetch('/materiales/formulario/libro/')  // esta ruta debe devolver solo el fragmento parcial
                        .then(response => {
            if (!response.ok) throw new Error('Error al cargar el formulario');
            return response.text();
        })
        .then(data => {
            formContainer.innerHTML = data;
            mostrarCantidadEjemplares();
        })
        .catch(error => {
            formContainer.innerHTML = '<p>Error al cargar el formulario.</p>';
            console.error(error);
        });
        break;
            case 'mapa':
                url = `/materiales/formulario/mapa/`; // ajustá para que exista esta vista y url
                break;
            case 'multimedia':
                url = `/materiales/formulario/multimedia/`;
                break;
            case 'proyector':
                url = `/materiales/formulario/proyector/`;
                break;
            case 'programa':
                url = `/materiales/formulario/programa/`;
                break;
            case 'notebook':
                url = `/materiales/formulario/notebook/`;
                break;
            case 'varios':
                url = `/materiales/formulario/varios/`;
                break;
            default:
                formContainer.innerHTML = '';
                cantTituloDescripcionContainer.innerHTML = '';
                return;
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
                mostrarCantidadEjemplares();
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

        if (dynamicRowsContainer) {
            dynamicRowsContainer.innerHTML = '';

            if (cantEjemplares > 1) {
                dynamicRowsContainer.classList.remove('hidden');

                for (let i = 0; i < cantEjemplares; i++) {
                    const row6 = document.createElement('div');
                    row6.className = 'row mt-2';
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
                    row7.className = 'row mt-2';
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

                    dynamicRowsContainer.appendChild(row6);
                    dynamicRowsContainer.appendChild(row7);
                }
            } else {
                dynamicRowsContainer.classList.add('hidden');
            }
        }
    }

    if (cargaMasivaInput) {
        cargaMasivaInput.addEventListener('change', function () {
            const fileList = this.files;
            const fileCount = fileList.length;
            const label = this.nextElementSibling;

            if (label) {
                label.innerHTML = fileCount > 0 ? `${fileCount} archivo(s) seleccionado(s)` : '';
            }
        });
    }
});
