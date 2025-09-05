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

// === Estado independiente ===
window.gruposTiposMapa = [];
window.gruposTiposVarios = [];

// === VARIOS: solo resumen de tipo y cantidad ===
window.renderizarTiposVarios = function() {
    const resumenContainer = document.getElementById('bloque-tipo-cantidad');
    if (!resumenContainer) return;
    let html = '<div class="table-responsive"><table class="table table-sm align-middle">';
    html += '<thead><tr><th></th><th></th></tr></thead><tbody>';
    window.gruposTiposVarios.forEach((g, idx) => {
        html += `<tr>
            <td style="vertical-align:middle; text-align:center;">
                <input type='checkbox' class='chk-tipo-varios' data-idx='${idx}' checked style='vertical-align:middle;'>
            </td>
            <td><span class="form-control" style="width:auto;display:inline-block;vertical-align:middle;border-bottom:2px solid #81123b;">${g.tipo}</span></td>
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
            window.agregarTipoVariosDesdeInputs('input-nuevo-tipo', 'input-nueva-cant', agregarGrupoTipoVarios, window.renderizarTiposVarios);
        });
    }
    // Enter en input para agregar tipo
    const inputNuevoTipo = document.getElementById('input-nuevo-tipo');
    if (inputNuevoTipo) {
        inputNuevoTipo.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                window.agregarTipoVariosDesdeInputs('input-nuevo-tipo', 'input-nueva-cant', agregarGrupoTipoVarios, window.renderizarTiposVarios);
            }
        });
    }

    // Listeners reutilizados para cantidad y checkbox
    inicializarListenersTiposMaterial('.input-cant-varios', '.chk-tipo-varios', window.renderizarTiposVarios);

    // Limpia el contenedor de ejemplares (no aplica en varios)
    const container = document.getElementById('contenedor-ejemplares-varios');
    if (container) container.innerHTML = '';
};

// Función para agregar tipo a gruposTiposVarios
window.agregarGrupoTipoVarios = function(tipo, cantidad) {
    window.gruposTiposVarios.push({ tipo, cantidad });
};

// Función auxiliar global para agregar tipo y limpiar campos en "varios"
window.agregarTipoVariosDesdeInputs = function(inputTipoId = 'input-nuevo-tipo', inputCantId = 'input-nueva-cant', agregarGrupoFn = window.agregarGrupoTipoVarios, renderFn = window.renderizarTiposVarios) {
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

// === MAPA: resumen y campos por ejemplar ===
window.renderizarTiposMapa = function() {
    const resumenContainer = document.getElementById('bloque-tipo-cantidad');
    if (!resumenContainer) return;
    let html = '<div class="table-responsive"><table class="table table-sm align-middle">';
    html += '<thead><tr><th></th><th></th></tr></thead><tbody>';
    window.gruposTiposMapa.forEach((g, idx) => {
        html += `<tr>
            <td><span class="form-control" style="width:180px;height:39px;display:inline-block;vertical-align:middle;border-bottom:2px solid #81123b;">${g.tipo}</span></td>
            <td>
                <input type='number' class='form-control form-control-sm input-cant-mapa' data-idx='${idx}' value='${g.cantidad}' min='1' max='5' style='width:70px;display:inline-block;vertical-align:middle;'>
            </td>
            <td style="vertical-align:middle; text-align:center;">
                <button type='button' class='boton-eliminar btn-eliminar-tipo-mapa' data-idx='${idx}' title='Eliminar tipo'>×</button>
            </td>
        </tr>`;
    });

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
            // Guardar datos existentes antes de agregar nuevo tipo
            const datosExistentes = guardarDatosFormularioMapa();
            
            // Agregar el nuevo tipo
            window.agregarGrupoTipoMapa(nuevoTipo, nuevaCant);
            
            // Regenerar el HTML
            window.renderizarTiposMapa();
            
            // Restaurar datos existentes (sin índice eliminado ya que estamos agregando)
            restaurarDatosFormularioMapaAgregar(datosExistentes);
            
            // Limpiar campos de entrada
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
    if (window.gruposTiposMapa.length > 0) {
        htmlTotal += '<div class="separador-punteado"></div>';
    }
    window.gruposTiposMapa.forEach((grupo, idxGrupo) => {
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
            
            // Guardar datos existentes antes de cambiar cantidad
            const datosExistentes = guardarDatosFormularioMapa();
            
            // Actualizar la cantidad
            window.gruposTiposMapa[idx].cantidad = val;
            
            // Regenerar el HTML
            window.renderizarTiposMapa();
            
            // Restaurar datos existentes
            restaurarDatosFormularioMapaAgregar(datosExistentes);
        });
    });
    // 2. Eliminar tipo (botón eliminar)
    document.querySelectorAll('.btn-eliminar-tipo-mapa').forEach(btn => {
        btn.addEventListener('click', function() {
            const idx = parseInt(this.dataset.idx);
            
            // Guardar datos existentes antes de eliminar
            const datosExistentes = guardarDatosFormularioMapa();
            
            // Eliminar el tipo específico
            window.gruposTiposMapa.splice(idx, 1);
            
            // Regenerar el HTML
            window.renderizarTiposMapa();
            
            // Restaurar datos de los tipos restantes
            restaurarDatosFormularioMapa(datosExistentes, idx);
        });
    });
    
    // Manejar atributos required según si hay fieldsets generados
    const camposIniciales = [
        document.getElementById('sede-mapa'),
        document.getElementById('input-nuevo-tipo-mapa'),
        document.getElementById('input-nueva-cant-mapa')
    ];
    
    if (window.gruposTiposMapa.length > 0) {
        // Si hay fieldsets generados, remover required de campos iniciales
        camposIniciales.forEach(campo => {
            if (campo) campo.removeAttribute('required');
        });
    } else {
        // Si no hay fieldsets, mantener required en campos iniciales
        camposIniciales.forEach(campo => {
            if (campo) campo.setAttribute('required', 'required');
        });
    }
};

// --- Funciones auxiliares para preservar datos del formulario ---
function guardarDatosFormularioMapa() {
    const datos = {};
    
    // Recorrer todos los grupos actuales y guardar los datos de sus campos
    window.gruposTiposMapa.forEach((grupo, idxGrupo) => {
        datos[idxGrupo] = {};
        
        for (let i = 0; i < grupo.cantidad; i++) {
            const idx = `${idxGrupo}_${i}`;
            const nRegistro = document.getElementById(`n_registro_${idx}`);
            const denominacion = document.getElementById(`denominacion_${idx}`);
            const descripcion = document.getElementById(`descripcion_${idx}`);
            
            if (nRegistro || denominacion || descripcion) {
                datos[idxGrupo][i] = {
                    n_registro: nRegistro ? nRegistro.value : '',
                    denominacion: denominacion ? denominacion.value : '',
                    descripcion: descripcion ? descripcion.value : ''
                };
            }
        }
    });
    
    return datos;
}

function restaurarDatosFormularioMapa(datosExistentes, idxEliminado) {
    // Restaurar datos para todos los grupos, ajustando los índices
    Object.keys(datosExistentes).forEach(oldIdxGrupo => {
        const oldIdx = parseInt(oldIdxGrupo);
        
        // Si el índice anterior es menor que el eliminado, mantener el mismo índice
        // Si es mayor, reducir en 1
        let newIdx;
        if (oldIdx < idxEliminado) {
            newIdx = oldIdx;
        } else if (oldIdx > idxEliminado) {
            newIdx = oldIdx - 1;
        } else {
            // Este era el grupo eliminado, no restaurar
            return;
        }
        
        // Restaurar datos para cada ejemplar del grupo
        Object.keys(datosExistentes[oldIdxGrupo]).forEach(ejemplarIdx => {
            const datos = datosExistentes[oldIdxGrupo][ejemplarIdx];
            const newIdxCompleto = `${newIdx}_${ejemplarIdx}`;
            
            const nRegistro = document.getElementById(`n_registro_${newIdxCompleto}`);
            const denominacion = document.getElementById(`denominacion_${newIdxCompleto}`);
            const descripcion = document.getElementById(`descripcion_${newIdxCompleto}`);
            
            if (nRegistro && datos.n_registro) nRegistro.value = datos.n_registro;
            if (denominacion && datos.denominacion) denominacion.value = datos.denominacion;
            if (descripcion && datos.descripcion) descripcion.value = datos.descripcion;
        });
    });
}

function restaurarDatosFormularioMapaAgregar(datosExistentes) {
    // Restaurar datos para todos los grupos existentes manteniendo sus índices originales
    Object.keys(datosExistentes).forEach(idxGrupo => {
        // Restaurar datos para cada ejemplar del grupo
        Object.keys(datosExistentes[idxGrupo]).forEach(ejemplarIdx => {
            const datos = datosExistentes[idxGrupo][ejemplarIdx];
            const idxCompleto = `${idxGrupo}_${ejemplarIdx}`;
            
            const nRegistro = document.getElementById(`n_registro_${idxCompleto}`);
            const denominacion = document.getElementById(`denominacion_${idxCompleto}`);
            const descripcion = document.getElementById(`descripcion_${idxCompleto}`);
            
            if (nRegistro && datos.n_registro) nRegistro.value = datos.n_registro;
            if (denominacion && datos.denominacion) denominacion.value = datos.denominacion;
            if (descripcion && datos.descripcion) descripcion.value = datos.descripcion;
        });
    });
}

// --- Función auxiliar global para agregar tipo y limpiar campos para MAPA ---
window.agregarGrupoTipoMapa = function(tipo, cantidad) {
    window.gruposTiposMapa.push({ tipo, cantidad });
};
window.agregarTipoMapaDesdeInputs = function(inputTipoId = 'input-nuevo-tipo-mapa', inputCantId = 'input-nueva-cant-mapa', agregarGrupoFn = window.agregarGrupoTipoMapa, renderFn = window.renderizarTiposMapa) {
    const nuevoTipoInput = document.getElementById(inputTipoId);
    const nuevaCantInput = document.getElementById(inputCantId);
    
    if (!nuevoTipoInput || !nuevaCantInput) {
        console.error('No se encontraron los inputs de tipo o cantidad');
        return;
    }
    
    const nuevoTipo = nuevoTipoInput.value.trim();
    const nuevaCant = parseInt(nuevaCantInput.value);
    
    // Validación mejorada
    if (!nuevoTipo) {
        alert('Por favor, seleccione un tipo de mapa.');
        nuevoTipoInput.focus();
        return;
    }
    
    if (isNaN(nuevaCant) || nuevaCant < 1) {
        alert('Por favor, ingrese una cantidad válida (mínimo 1).');
        nuevaCantInput.focus();
        return;
    }
    
    // Guardar datos existentes antes de agregar nuevo tipo
    const datosExistentes = guardarDatosFormularioMapa();
    
    // Agregar el nuevo tipo
    agregarGrupoFn(nuevoTipo, nuevaCant);
    
    // Regenerar el HTML
    renderFn();
    
    // Restaurar datos existentes
    restaurarDatosFormularioMapaAgregar(datosExistentes);
    
    // Limpiar campos
    nuevoTipoInput.value = '';
    nuevaCantInput.value = 1;
};

// --- Función de validación para campos dinámicos de ejemplares ---
window.validarCamposDinamicosEjemplares = function() {
    const contenedorEjemplares = document.getElementById('contenedor-ejemplares-mapa');
    const fieldsets = contenedorEjemplares ? contenedorEjemplares.querySelectorAll('fieldset.mb-4.p-3.rounded') : [];
    
    // Si no hay fieldsets generados con las clases específicas, validar campos iniciales
    if (fieldsets.length === 0) {
        const camposIniciales = [
            { campo: document.getElementById('sede-mapa'), nombre: 'Sede' },
            { campo: document.getElementById('input-nuevo-tipo-mapa'), nombre: 'Tipo de Mapa' },
            { campo: document.getElementById('input-nueva-cant-mapa'), nombre: 'Cantidad' }
        ];
        
        for (let item of camposIniciales) {
            if (item.campo && !item.campo.value.trim()) {
                item.campo.scrollIntoView({ behavior: 'smooth', block: 'center' });
                item.campo.focus();
                alert(`Por favor, complete el campo "${item.nombre}" antes de continuar.`);
                return false;
            }
        }
        
        alert('Debe continuar completando los campos requeridos haciendo click en el botón "+".');
        return false;
    }
    
    // Si hay fieldsets generados, validar solo los campos requeridos dentro de los fieldsets
    const camposRequeridos = contenedorEjemplares.querySelectorAll('input[required]');
    const camposVacios = [];
    
    camposRequeridos.forEach(campo => {
        if (!campo.value.trim()) {
            camposVacios.push(campo);
        }
    });
    
    if (camposVacios.length > 0) {
        // Encontrar el primer campo vacío y hacer scroll hacia él
        const primerCampoVacio = camposVacios[0];
        primerCampoVacio.scrollIntoView({ behavior: 'smooth', block: 'center' });
        primerCampoVacio.focus();
        
        // Mostrar mensaje de error específico
        const label = primerCampoVacio.previousElementSibling || primerCampoVacio.parentElement.querySelector('label');
        const nombreCampo = label ? label.textContent.replace('*', '').trim().replace(':', '') : 'Campo requerido';
        alert(`Por favor, complete el campo "${nombreCampo}" antes de guardar.`);
        
        return false;
    }
    
    return true;
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
                <label for="n_registro_${idx}">N° de registro: <span style="color: red;">*</span></label>
                <input type="text" class="form-control" id="n_registro_${idx}" name="n_registro_${idx}" required />
            </div>
            <div class="col-md-2">
                <label for="denominacion_${idx}">Denominación: <span style="color: red;">*</span></label>
                <input type="text" class="form-control" id="denominacion_${idx}" name="denominacion_${idx}" required />
            </div>
            <div class="col-md-6">
                <label for="descripcion_${idx}">Descripción:</label>
                <textarea class="form-control textarea-wrapper" id="descripcion_${idx}" rows="3" name="descripcion_${idx}"></textarea>
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
    const containerMapa = document.getElementById('contenedor-ejemplares-mapa');
    
    let tipo = '';
    if (containerNotebook) tipo = 'notebook';
    else if (containerProyector) tipo = 'proyector';
    
    if (inputCantidad && tipo) {
        inputCantidad.addEventListener('input', function() { window.updateRowsMaterial(tipo); });
        window.updateRowsMaterial(tipo);
    }
    
    // Inicializar renderizado para formulario de mapa
    if (containerMapa) {
        window.renderizarTiposMapa();
    }
});
