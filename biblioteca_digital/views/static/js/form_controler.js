document.addEventListener("DOMContentLoaded", function () {
    const tipoMaterialSelect = document.getElementById('tipo_material');
    const formContainer = document.getElementById('formulario-especifico');
    const cantEjemplaresInput = document.getElementById('cant_ejemplares');
    const dynamicRowsContainer = document.getElementById('dynamic-rows');
    const buttonsContainer = document.getElementById('buttons-container');
    const cantEjemplaresContainer = document.getElementById('cant_ejemplares_container');

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
                        <textarea class="form-control h-100" id="observaciones_${i}" name="observaciones[]" rows="2">Escriba aquí...</textarea>
                    </div>
                </div>
            `;
            dynamicRowsContainer.appendChild(row);
        }
    }

    function mostrarAlerta() {
        const alertaFondo = document.createElement('div');
        alertaFondo.style.position = 'fixed';
        alertaFondo.style.top = '0';
        alertaFondo.style.left = '0';
        alertaFondo.style.width = '100%';
        alertaFondo.style.height = '100%';
        alertaFondo.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
        alertaFondo.style.display = 'flex';
        alertaFondo.style.justifyContent = 'center';
        alertaFondo.style.alignItems = 'center';
        alertaFondo.style.zIndex = '9999';

        const alertaContenedor = document.createElement('div');
        alertaContenedor.style.width = '400px';
        alertaContenedor.style.backgroundColor = 'white';
        alertaContenedor.style.borderRadius = '5px';

        const alertaTitulo = document.createElement('div');
        alertaTitulo.style.backgroundColor = '#ff69b4';
        alertaTitulo.style.color = 'white';
        alertaTitulo.style.padding = '10px';
        alertaTitulo.style.textAlign = 'center';
        alertaTitulo.style.fontWeight = 'bold';
        alertaTitulo.textContent = '¡ATENCIÓN!';

        const alertaMensaje = document.createElement('div');
        alertaMensaje.style.padding = '20px';
        alertaMensaje.style.textAlign = 'center';
        alertaMensaje.textContent = 'AL REDUCIR LA CANTIDAD DE EJEMPLARES, SE PERDERÁN LOS DATOS DE LOS EJEMPLARES QUE SUPERAN LA CANTIDAD SELECCIONADA.';

        const alertaBotones = document.createElement('div');
        alertaBotones.style.display = 'flex';
        alertaBotones.style.justifyContent = 'space-between';
        alertaBotones.style.padding = '0 20px 20px 20px';

        const botonAceptar = document.createElement('button');
        botonAceptar.textContent = 'ACEPTAR';
        botonAceptar.style.backgroundColor = '#ff69b4';
        botonAceptar.style.color = 'white';
        botonAceptar.style.border = 'none';
        botonAceptar.style.padding = '8px 25px';
        botonAceptar.style.borderRadius = '3px';
        botonAceptar.style.cursor = 'pointer';
        botonAceptar.style.flex = '1';
        botonAceptar.style.marginRight = '10px';

        const botonCancelar = document.createElement('button');
        botonCancelar.textContent = 'CANCELAR';
        botonCancelar.style.backgroundColor = '#6c757d';
        botonCancelar.style.color = 'white';
        botonCancelar.style.border = 'none';
        botonCancelar.style.padding = '8px 25px';
        botonCancelar.style.borderRadius = '3px';
        botonCancelar.style.cursor = 'pointer';
        botonCancelar.style.flex = '1';
        botonCancelar.style.marginLeft = '10px';

        alertaBotones.appendChild(botonAceptar);
        alertaBotones.appendChild(botonCancelar);
        alertaContenedor.appendChild(alertaTitulo);
        alertaContenedor.appendChild(alertaMensaje);
        alertaContenedor.appendChild(alertaBotones);
        alertaFondo.appendChild(alertaContenedor);
        document.body.appendChild(alertaFondo);

        return new Promise((resolve) => {
            botonAceptar.addEventListener('click', function () {
                document.body.removeChild(alertaFondo);
                resolve(true);
            });
            botonCancelar.addEventListener('click', function () {
                document.body.removeChild(alertaFondo);
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

    if (tipoMaterialSelect.value) {
        updateRows();
    }
});
