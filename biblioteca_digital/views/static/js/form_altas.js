// === GLOBAL ===

let config = {};
let tipos = [];
let tiposAgregados = new Set();
let gruposTiposElemento = [];

function guardarTipos() {
    localStorage.setItem(config.tiposKey, JSON.stringify(Array.from(tiposAgregados)));
}

function cargarTipos() {
    const guardados = localStorage.getItem(config.tiposKey);
    if (guardados) tiposAgregados = new Set(JSON.parse(guardados));
}

function agregarTipo(tipo) {
    if (!tipo || tiposAgregados.has(tipo.toLowerCase())) return false;
    tiposAgregados.add(tipo.toLowerCase());
    guardarTipos();
    return true;
}

function limpiarTipos() {
    tiposAgregados.clear();
    localStorage.removeItem(config.tiposKey);
}

function cargarSugerencias(sugerencias, inputId, containerId) {
    // === GLOBAL ===
}

function agregarGrupoTipoElemento(tipo, cantidad) {
    cantidad = parseInt(cantidad);

    if (!tipo || isNaN(cantidad) || cantidad < 1) {
        alert('Debes ingresar un tipo válido.');
        return;
    }

    if (gruposTiposElemento.some(g => g.tipo.toLowerCase() === tipo.toLowerCase())) {
        alert("Ese tipo de Elemento ya fue agregado.");
        return;
    }

    gruposTiposElemento.push({ tipo, cantidad });
    renderizarGruposTiposElemento();
    renderizarListaResumenTipos();  
}

// === UTILIDAD: listeners reutilizables para resumen de tipos ===
/**
 * Inicializa listeners para inputs de cantidad y checkboxes de tipos de material.
 * Permite DRY entre distintos materiales (mapa, varios, etc).
 * @param {string} selectorCantidad - Selector para los inputs de cantidad.
 * @param {string} selectorCheckbox - Selector para los checkboxes.
 * @param {function} renderFn - Función de renderizado a llamar tras cambios.
 */
function inicializarListenersTiposMaterial(selectorCantidad, selectorCheckbox, renderFn) {
    // 1. Cambiar cantidad
    document.querySelectorAll(selectorCantidad).forEach(inp => {
        inp.addEventListener('change', function() {
            const idx = parseInt(this.dataset.idx);
            let val = parseInt(this.value);
            if (isNaN(val) || val < 1) val = 1;
            gruposTiposElemento[idx].cantidad = val;
            renderFn();
        });
    });
    // 2. Eliminar tipo (uncheck)
    document.querySelectorAll(selectorCheckbox).forEach(chk => {
        chk.addEventListener('change', function() {
            const idx = parseInt(this.dataset.idx);
            if (!this.checked) {
                gruposTiposElemento.splice(idx, 1);
                renderFn();
            }
        });
    });
}

// === VARIOS: solo resumen de tipo y cantidad ===
window.renderizarTiposVarios = function() {
    const resumenContainer = document.getElementById('bloque-tipo-cantidad');
    if (!resumenContainer) return;
    let html = '<div class="table-responsive"><table class="table table-sm align-middle">';
    html += '<thead><tr><th></th><th></th><th>Cant. de ejemplares</th></tr></thead><tbody>';
    gruposTiposElemento.forEach((g, idx) => {
        html += `<tr>
            <td style="vertical-align:middle; text-align:center;">
                <input type='checkbox' class='chk-tipo-varios' data-idx='${idx}' checked style='vertical-align:middle;'>
            </td>
            <td><span class="input-especial">${g.tipo}</span></td>
            <td style="vertical-align:middle;">
                <input type='number' class='form-control form-control-sm input-cant-varios d-inline-block' data-idx='${idx}' value='${g.cantidad}' min='1' style='width:196px;display:inline-block;vertical-align:middle;'>
            </td>
        </tr>`;
    });
    // Fila de ingreso de nuevo tipo
    html += `<tr>
        <td></td>
        <td><input type='text' class='input-especial' id='input-nuevo-tipo' placeholder='Nuevo tipo...'></td>
        <td><input type='number' class='form-control form-control-sm' id='input-nueva-cant' value='1' min='1' style='width:196px;display:inline-block;'></td>
    </tr>`;
    html += '</tbody></table></div>';
    html += '<div class="w-50 d-flex justify-content-center mt-2"><button type="button" class="boton-mas" id="btn-agregar-tipo-varios">+</button></div>';
    resumenContainer.innerHTML = html;

    // Botón + para agregar tipo
    const btnAgregarTipoVarios = document.getElementById('btn-agregar-tipo-varios');
    if (btnAgregarTipoVarios) {
        btnAgregarTipoVarios.addEventListener('click', function() {
            window.agregarTipoMapaDesdeInputs('input-nuevo-tipo', 'input-nueva-cant', agregarGrupoTipoElemento, window.renderizarTiposVarios);
        });
    }
    // Enter en input para agregar tipo
    const inputNuevoTipo = document.getElementById('input-nuevo-tipo');
    if (inputNuevoTipo) {
        inputNuevoTipo.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                window.agregarTipoMapaDesdeInputs('input-nuevo-tipo', 'input-nueva-cant', agregarGrupoTipoElemento, window.renderizarTiposVarios);
            }
        });
    }

    // Listeners reutilizados para cantidad y checkbox
    inicializarListenersTiposMaterial('.input-cant-varios', '.chk-tipo-varios', window.renderizarTiposVarios);

    // Limpia el contenedor de ejemplares (no aplica en varios)
    const container = document.getElementById('contenedor-ejemplares-varios');
    if (container) container.innerHTML = '';
};


// === MAPA: resumen y campos por ejemplar ===
window.renderizarTiposMapa = function() {
    const resumenContainer = document.getElementById('bloque-tipo-cantidad');
    if (!resumenContainer) return;
    let html = '<div class="table-responsive"><table class="table table-sm align-middle">';
    html += '<thead><tr><th></th><th></th><th>Cant. de ejemplares</th></tr></thead><tbody>';
    gruposTiposElemento.forEach((g, idx) => {
        html += `<tr>
            <td style="vertical-align:middle; text-align:center;">
                <input type='checkbox' class='chk-tipo-mapa' data-idx='${idx}' checked style='vertical-align:middle;'>
            </td>
            <td><span class="input-especial">${g.tipo}</span></td>
            <td>
                <input type='number' class='form-control form-control-sm input-cant-mapa' data-idx='${idx}' value='${g.cantidad}' min='1' style='width:70px;display:inline-block;vertical-align:middle;'>
            </td>
        </tr>`;
    });
    // Fila de ingreso de nuevo tipo
    html += `<tr>
        <td></td>
        <td><input type='text' class='form-control form-control-sm' id='input-nuevo-tipo-mapa' placeholder='Nuevo tipo...'></td>
        <td><input type='number' class='form-control form-control-sm' id='input-nueva-cant-mapa' value='1' min='1' style='width:70px;display:inline-block;vertical-align:middle;'></td>
    </tr>`;
    html += '</tbody></table></div>';
    // Agregar el botón + debajo de la tabla, centrado
    html += '<div class="w-50 d-flex justify-content-center mt-2"><button type="button" class="boton-mas" id="btn-agregar-tipo-mapa">+</button></div>';
    resumenContainer.innerHTML = html;

    // Función auxiliar para agregar tipo y limpiar campos
    function agregarTipoMapaDesdeInputs() {
        const nuevoTipoInput = document.getElementById('input-nuevo-tipo-mapa');
        const nuevaCantInput = document.getElementById('input-nueva-cant-mapa');
        const nuevoTipo = nuevoTipoInput.value.trim();
        const nuevaCant = parseInt(nuevaCantInput.value) || 1;
        if (nuevoTipo !== '') {
            agregarGrupoTipoElemento(nuevoTipo, nuevaCant);
            window.renderizarTiposMapa();
            nuevoTipoInput.value = '';
            nuevaCantInput.value = 1;
        }
    }

    // Listener para el botón +
    const btnAgregarTipoMapa = document.getElementById('btn-agregar-tipo-mapa');
    if (btnAgregarTipoMapa) {
        btnAgregarTipoMapa.addEventListener('click', agregarTipoMapaDesdeInputs);
    }

    // Listener para Enter en el input de nuevo tipo
    const inputNuevoTipoMapa = document.getElementById('input-nuevo-tipo-mapa');
    if (inputNuevoTipoMapa) {
        inputNuevoTipoMapa.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                agregarTipoMapaDesdeInputs();
            }
        });
    }

    // Generar campos dinámicos por ejemplar
    const container = document.getElementById('contenedor-ejemplares-mapa');
    if (!container) return;
    let htmlTotal = '';
    if (gruposTiposElemento.length > 0) {
        htmlTotal += '<div class="separador-punteado"></div>';
    }
    gruposTiposElemento.forEach((grupo, idxGrupo) => {
        // Agrega el separador antes de cada grupo excepto el primero
        if (idxGrupo > 0) {
            htmlTotal += '<div class="separador-punteado"></div>';
        }
        let htmlGrupo = `<fieldset class="mb-4 p-3  rounded">
            <legend class="fw-bold mt-3">TIPO DE MAPA: <span class="text-secundario">${grupo.tipo.toUpperCase()}</span></legend>`;
        for (let i = 0; i < grupo.cantidad; i++) {
            htmlGrupo += plantillaEjemplarElemento(`${idxGrupo}_${i}`, grupo.tipo);
        }
        htmlGrupo += '</fieldset>';
        htmlTotal += htmlGrupo;
    });
    container.innerHTML = htmlTotal;

    // Listeners para inputs dinámicos
    // 1. Cambiar cantidad
    document.querySelectorAll('.input-cant-mapa').forEach(inp => {
        inp.addEventListener('change', function() {
            const idx = parseInt(this.dataset.idx);
            let val = parseInt(this.value);
            if (isNaN(val) || val < 1) val = 1;
            gruposTiposElemento[idx].cantidad = val;
            window.renderizarTiposMapa();
        });
    });
    // 2. Eliminar tipo (uncheck)
    document.querySelectorAll('.chk-tipo-mapa').forEach(chk => {
        chk.addEventListener('change', function() {
            const idx = parseInt(this.dataset.idx);
            if (!this.checked) {
                gruposTiposElemento.splice(idx, 1);
                window.renderizarTiposMapa();
            }
        });
    });
};

// --- Función auxiliar global para agregar tipo y limpiar campos ---
window.agregarTipoMapaDesdeInputs = function(inputTipoId = 'input-nuevo-tipo-mapa', inputCantId = 'input-nueva-cant-mapa', agregarGrupoFn = agregarGrupoTipoElemento, renderFn = window.renderizarTiposMapa) {
    const nuevoTipoInput = document.getElementById(inputTipoId);
    const nuevaCantInput = document.getElementById(inputCantId);
    const nuevoTipo = nuevoTipoInput.value.trim();
    const nuevaCant = parseInt(nuevaCantInput.value) || 1;
    if (nuevoTipo !== '') {
        agregarGrupoFn(nuevoTipo, nuevaCant);
        renderFn();
        nuevoTipoInput.value = '';
        nuevaCantInput.value = 1;
    }
};

function renderizarListaResumenTipos() {
    const resumenContainer = document.getElementById('bloque-tipo-cantidad');
    if (!resumenContainer) return;

    if (gruposTiposElemento.length === 0) {
        resumenContainer.innerHTML = '';
        return;
    }

    let html = '<div class="table-responsive"><table class="table table-sm ">';
    html += '<thead><tr><th>Tipo</th><th>Cantidad de ejemplares</th></tr></thead><tbody>';

    gruposTiposElemento.forEach(g => {
        html += `<tr><td>${g.tipo}</td><td>${g.cantidad}</td></tr>`;
    });

    html += '</tbody></table></div>';
    resumenContainer.innerHTML = html;
}

function renderizarGruposTiposElemento() {
    const container = document.getElementById('contenedor-ejemplares-Elemento');
    if (!container) return;

    let htmlTotal = '';
    gruposTiposElemento.forEach((grupo, idxGrupo) => {
        let htmlGrupo = `
                <fieldset class="mb-4 p-3 border rounded">
                    <legend class="fw-bold mt-3">TIPO DE Elemento: <span class="text-primary">${grupo.tipo.toUpperCase()}</span></legend>
            `;
            for (let i = 0; i < grupo.cantidad; i++) {
                htmlGrupo += plantillaEjemplarElemento(`${idxGrupo}_${i}`, grupo.tipo);
            }
            htmlGrupo += '</fieldset>';
            htmlTotal += htmlGrupo;
        });

    container.innerHTML = htmlTotal;
}

function plantillaEjemplarElemento(idx, tipo = "") {
    return `
    <div class="row mb-3">
            <div class="col-md-2">
                <label for="n_registro_${idx}">N° de registro:</label>
                <input type="text" class="form-control" id="n_registro_${idx}" name="n_registro_${idx}" required />
            </div>
            <div class="col-md-2">
                <label for="denominacion_${idx}">Denominación:</label>
                <input type="text" class="form-control" id="denominacion_${idx}" name="denominacion_${idx}" required />
            </div>
            <div class="col-md-2">
                <label for="descripcion_${idx}">Descripción:</label>
                <textarea class="form-control textarea-wrapper" id="descripcion_${idx}" rows="2" name="descripcion_${idx}" required></textarea>
            </div>
        </div>
    `;
}


// === EJEMPLARES DINÁMICOS GENERALES (Notebook y Proyector) ===
// Genera el HTML de un ejemplar según el tipo de material
function plantillaEjemplarMaterial(idx, tipo) {
    if (tipo === 'notebook') {
        return `
        <div class="row mb-2">
            <div class="col-md-3">
                <label for="serie_${idx}">N° de serie:</label>
                <input type="text" class="form-control" id="serie_${idx}" name="serie_${idx}" required placeholder="N° de serie...">
            </div>
            <div class="col-md-3">
                <label for="modelo_${idx}">Modelo:</label>
                <input type="text" class="form-control" id="modelo_${idx}" name="modelo_${idx}" required placeholder="Modelo...">
            </div>
        </div>`;
    } else if (tipo === 'proyector') {
        return `
        <div class="row mb-2">
            <div class="col-md-3">
                <label for="sede_${idx}">Sede:</label>
                <input type="text" class="form-control" id="sede_${idx}" name="sede_${idx}" required placeholder="Sede...">
            </div>
            <div class="col-md-3">
                <label for="n_registro_${idx}">N° de registro:</label>
                <input type="text" class="form-control" id="n_registro_${idx}" name="n_registro_${idx}" required placeholder="N° de registro...">
            </div>
            <div class="col-md-3">
                <label for="modelo_${idx}">Modelo:</label>
                <input type="text" class="form-control" id="modelo_${idx}" name="modelo_${idx}" required placeholder="Modelo..." />
            </div>
        </div>`;
    }
    return '';
}

// Generador dinámico de ejemplares para notebook y proyector
window.updateRowsMaterial = function(tipo) {
    const cantidadInput = document.querySelector('input[name="cant_ejemplares"]');
    const containerNotebook = document.getElementById('contenedor-ejemplares-notebook');
    const containerProyector = document.getElementById('contenedor-ejemplares-proyector');
    const cantidad = parseInt(cantidadInput ? cantidadInput.value : 1) || 1;

    // Limpiar ambos contenedores
    if (containerNotebook) containerNotebook.innerHTML = '';
    if (containerProyector) containerProyector.innerHTML = '';

    for (let i = 1; i <= cantidad; i++) {
        if (tipo === 'notebook' && containerNotebook) {
            containerNotebook.insertAdjacentHTML('beforeend', plantillaEjemplarMaterial(i, 'notebook'));
        } else if (tipo === 'proyector' && containerProyector) {
            containerProyector.insertAdjacentHTML('beforeend', plantillaEjemplarMaterial(i, 'proyector'));
        }
    }
};

// Inicializar evento al cargar (solo para carga directa, no dinámica)
document.addEventListener('DOMContentLoaded', function () {
    const inputCantidad = document.querySelector('input[name="cant_ejemplares"]');
    const containerNotebook = document.getElementById('contenedor-ejemplares-notebook');
    const containerProyector = document.getElementById('contenedor-ejemplares-proyector');
    let tipo = '';
    if (containerNotebook) tipo = 'notebook';
    else if (containerProyector) tipo = 'proyector';
    if (inputCantidad && tipo) {
        inputCantidad.addEventListener('input', function() { window.updateRowsMaterial(tipo); });
        window.updateRowsMaterial(tipo);
    }
});
