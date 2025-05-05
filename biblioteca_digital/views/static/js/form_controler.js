document.addEventListener("DOMContentLoaded", function () {
    const tipoMaterialSelect = document.getElementById('tipo_material');
    const formContainer = document.getElementById('formulario-especifico');
    const cantEjemplaresInput = document.getElementById('cant_ejemplares');
    const dynamicRowsContainer = document.getElementById('dynamic-rows');
    const buttonsContainer = document.getElementById('buttons-container');
    const cantEjemplaresContainer = document.getElementById('cant_ejemplares_container');
    const uploadSimple = document.getElementById('upload_simple_container');
    const uploadBox = document.getElementById('upload_box_container');

    let valorAnterior = parseInt(cantEjemplaresInput.value) || 1;

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

    function updateRows() {
        const cantEjemplares = parseInt(cantEjemplaresInput.value) || 1;

        dynamicRowsContainer.innerHTML = '';

        const showElements = cantEjemplares >= 1;
        dynamicRowsContainer.style.display = showElements ? 'block' : 'none';
        buttonsContainer.style.display = showElements ? 'block' : 'none';

        if (cantEjemplares <= 0) return;

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
                    <div class="col-6">
                        <label for="observaciones_${i}">Observaciones:</label>
                        <textarea class="form-control h-100" id="observaciones_${i}" name="observaciones[]" rows="4" style="min-width:100%; max-width:100%; min-height:70px;" placeholder="Escriba aquí..."></textarea>
                    </div>
                </div>
            `;
            dynamicRowsContainer.appendChild(row);
        }
    }

    function mostrarAlerta() {
        const overlay = document.createElement('div');
        overlay.style.position = 'fixed';
        overlay.style.top = '0';
        overlay.style.left = '0';
        overlay.style.width = '100%';
        overlay.style.height = '100%';
        overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
        overlay.style.zIndex = '9999';
        overlay.style.display = 'flex';
        overlay.style.justifyContent = 'center';
        overlay.style.alignItems = 'center';
    
        const modal = document.createElement('div');
        modal.style.width = '420px';
        modal.style.backgroundColor = '#ffd5d5';
        modal.style.borderRadius = '10px';
        modal.style.boxShadow = '0 4px 10px rgba(0,0,0,0.3)';
        modal.style.overflow = 'hidden';
        modal.style.fontFamily = 'sans-serif';
    
        const header = document.createElement('div');
        header.textContent = '¡ATENCIÓN!';
        header.style.backgroundColor = '#ff4d4d';
        header.style.color = 'white';
        header.style.textAlign = 'center';
        header.style.fontWeight = 'bold';
        header.style.padding = '12px';
        header.style.fontSize = '18px';
    
        const body = document.createElement('div');
        body.textContent = 'AL REDUCIR LA CANTIDAD DE EJEMPLARES, SE PERDERÁN LOS DATOS INTRODUCIDOS PARA LOS EJEMPLARES QUE SUPEREN LA CANTIDAD SELECCIONADA.';
        body.style.padding = '20px';
        body.style.textAlign = 'center';
        body.style.fontSize = '14px';
        body.style.color = '#333';
    
        const footer = document.createElement('div');
        footer.style.display = 'flex';
        footer.style.justifyContent = 'space-between';
        footer.style.padding = '10px 20px 20px 20px';
    
        const btnCancelar = document.createElement('button');
        btnCancelar.textContent = 'CANCELAR';
        btnCancelar.style.backgroundColor = '#4e6ef2';
        btnCancelar.style.color = 'white';
        btnCancelar.style.border = 'none';
        btnCancelar.style.padding = '10px 20px';
        btnCancelar.style.borderRadius = '6px';
        btnCancelar.style.cursor = 'pointer';
        btnCancelar.style.flex = '1';
        btnCancelar.style.marginRight = '10px';
        btnCancelar.style.fontWeight = 'bold';
    
        const btnConfirmar = document.createElement('button');
        btnConfirmar.textContent = 'CONFIRMAR';
        btnConfirmar.style.backgroundColor = '#d63333';
        btnConfirmar.style.color = 'white';
        btnConfirmar.style.border = 'none';
        btnConfirmar.style.padding = '10px 20px';
        btnConfirmar.style.borderRadius = '6px';
        btnConfirmar.style.cursor = 'pointer';
        btnConfirmar.style.flex = '1';
        btnConfirmar.style.fontWeight = 'bold';
    
        footer.appendChild(btnCancelar);
        footer.appendChild(btnConfirmar);
    
        modal.appendChild(header);
        modal.appendChild(body);
        modal.appendChild(footer);
        overlay.appendChild(modal);
        document.body.appendChild(overlay);
    
        return new Promise((resolve) => {
            btnConfirmar.addEventListener('click', () => {
                overlay.remove();
                resolve(true);
            });
            btnCancelar.addEventListener('click', () => {
                overlay.remove();
                resolve(false);
            });
        });
    }
    

    async function manejarReduccionEjemplares(valorActual) {
        cantEjemplaresInput.value = valorAnterior;

        const confirmado = await mostrarAlerta();

        if (confirmado) {
            cantEjemplaresInput.value = valorActual;
            valorAnterior = valorActual;
            updateRows();
        } else {
            cantEjemplaresInput.value = valorAnterior;
        }
    }

    cantEjemplaresInput.addEventListener('change', async function () {
        const valorActual = parseInt(cantEjemplaresInput.value) || 1;

        if (valorActual < valorAnterior) {
            await manejarReduccionEjemplares(valorActual);
        } else if (valorActual > valorAnterior) {
            valorAnterior = valorActual;
            updateRows();
        }
    });
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
        cantEjemplaresContainer.style.display = tipo ? 'block' : 'none';

        if (!tipo) {
            formContainer.innerHTML = '';
            dynamicRowsContainer.innerHTML = '';
            dynamicRowsContainer.style.display = 'none';
            buttonsContainer.style.display = 'none';
            return;
        }

        const templateContent = await loadMaterialTemplate(tipo);
        if (templateContent) {
            formContainer.innerHTML = templateContent;
        }

        valorAnterior = parseInt(cantEjemplaresInput.value) || 1;
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
    if (tipoMaterialSelect.value) {
        updateRows();
    }
});
