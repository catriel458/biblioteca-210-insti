
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

// === VARIOS: solo resumen de tipo y cantidad ===
window.renderizarTiposVarios = function() {
    const resumenContainer = document.getElementById('bloque-tipo-cantidad');
    if (!resumenContainer) return;
    let html = '<div class="table-responsive"><table class="table table-sm align-middle">';
    html += '<thead><tr><th style="width:32px">✔</th><th></th><th>Cant. de ejemplares</th></tr></thead><tbody>';
    gruposTiposElemento.forEach((g, idx) => {
        html += `<tr>
            <td><input type='checkbox' class='chk-tipo-varios' data-idx='${idx}' checked></td>
            <td>${g.tipo}</td>
            <td><input type='number' class='form-control form-control-sm input-cant-varios' data-idx='${idx}' value='${g.cantidad}' min='1' style='width:70px;display:inline-block;'></td>
        </tr>`;
    });
    // Fila de ingreso de nuevo tipo
    html += `<tr>
        <td></td>
        <td><input type='text' class='form-control form-control-sm' id='input-nuevo-tipo' placeholder='Nuevo tipo...'></td>
        <td><input type='number' class='form-control form-control-sm' id='input-nueva-cant' value='1' min='1' style='width:70px;display:inline-block;'></td>
    </tr>`;
    html += '</tbody></table></div>';
    resumenContainer.innerHTML = html;
    // No se generan campos dinámicos extra en 'contenedor-ejemplares-varios'
    const container = document.getElementById('contenedor-ejemplares-varios');
    if (container) container.innerHTML = '';

    // Listeners para inputs dinámicos
    // 1. Cambiar cantidad
    document.querySelectorAll('.input-cant-varios').forEach(inp => {
        inp.addEventListener('change', function() {
            const idx = parseInt(this.dataset.idx);
            let val = parseInt(this.value);
            if (isNaN(val) || val < 1) val = 1;
            gruposTiposElemento[idx].cantidad = val;
            window.renderizarTiposVarios();
        });
    });
    // 2. Eliminar tipo (uncheck)
    document.querySelectorAll('.chk-tipo-varios').forEach(chk => {
        chk.addEventListener('change', function() {
            const idx = parseInt(this.dataset.idx);
            if (!this.checked) {
                gruposTiposElemento.splice(idx, 1);
                window.renderizarTiposVarios();
            }
        });
    });
    // 3. Agregar nuevo tipo con Enter
    document.getElementById('input-nuevo-tipo').addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && this.value.trim() !== '') {
            const nuevoTipo = this.value.trim();
            const nuevaCant = parseInt(document.getElementById('input-nueva-cant').value) || 1;
            agregarGrupoTipoElemento(nuevoTipo, nuevaCant);
            window.renderizarTiposVarios();
            this.value = '';
            document.getElementById('input-nueva-cant').value = 1;
        }
    });
};

// === MAPA: resumen y campos por ejemplar ===
window.renderizarTiposMapa = function() {
    const resumenContainer = document.getElementById('bloque-tipo-cantidad');
    if (!resumenContainer) return;
    let html = '<div class="table-responsive"><table class="table table-sm align-middle">';
    html += '<thead><tr><th style="width:32px"><✔</th><th></th><th>Cant. de ejemplares</th></tr></thead><tbody>';
    gruposTiposElemento.forEach((g, idx) => {
        html += `<tr>
            <td><input type='checkbox' class='chk-tipo-mapa' data-idx='${idx}' checked></td>
            <td>${g.tipo}</td>
            <td><input type='number' class='form-control form-control-sm input-cant-mapa' data-idx='${idx}' value='${g.cantidad}' min='1' style='width:70px;display:inline-block;'></td>
        </tr>`;
    });
    // Fila de ingreso de nuevo tipo
    html += `<tr>
        <td></td>
        <td><input type='text' class='form-control form-control-sm' id='input-nuevo-tipo-mapa' placeholder='Nuevo tipo...'></td>
        <td><input type='number' class='form-control form-control-sm' id='input-nueva-cant-mapa' value='1' min='1' style='width:70px;display:inline-block;'></td>
    </tr>`;
    html += '</tbody></table></div>';
    resumenContainer.innerHTML = html;

    // Generar campos dinámicos por ejemplar
    const container = document.getElementById('contenedor-ejemplares-mapa');
    if (!container) return;
    let htmlTotal = '';
    gruposTiposElemento.forEach((grupo, idxGrupo) => {
        let htmlGrupo = `<fieldset class="mb-4 p-3  rounded">
            <legend class="fw-bold mt-3">TIPO DE Mapa: <span class="text-primary">${grupo.tipo.toUpperCase()}</span></legend>`;
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
    // 3. Agregar nuevo tipo con Enter
    document.getElementById('input-nuevo-tipo-mapa').addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && this.value.trim() !== '') {
            const nuevoTipo = this.value.trim();
            const nuevaCant = parseInt(document.getElementById('input-nueva-cant-mapa').value) || 1;
            agregarGrupoTipoElemento(nuevoTipo, nuevaCant);
            window.renderizarTiposMapa();
            this.value = '';
            document.getElementById('input-nueva-cant-mapa').value = 1;
        }
    });
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
            <div class="col-md-3">
                <label for="tipo_${idx}">Tipo:</label>
                <input type="text" class="form-control" id="tipo_${idx}" name="tipo_${idx}" value="${tipo}" readonly />
            </div>
            <div class="col-md-3">
                <label for="n_registro_${idx}">N° de registro:</label>
                <input type="text" class="form-control" id="n_registro_${idx}" name="n_registro_${idx}" required />
            </div>
            <div class="col-md-3">
                <label for="denominacion_${idx}">Denominación:</label>
                <input type="text" class="form-control" id="denominacion_${idx}" name="denominacion_${idx}" required />
            </div>
            <div class="col-md-3">
                <label for="descripcion_${idx}">Descripción:</label>
                <textarea class="form-control textarea-wrapper" id="descripcion_${idx}" name="descripcion_${idx}" required></textarea>
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
