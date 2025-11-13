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

// Función para guardar datos del formulario multimedia
window.guardarDatosFormularioMultimedia = function() {
    window.datosFormularioMultimedia = {};
    
    // Guardar datos de campos básicos
    const profesor = document.getElementById('profesor');
    const carrera = document.getElementById('carrera');
    const materia = document.getElementById('materia');
    
    if (profesor) window.datosFormularioMultimedia.profesor = profesor.value;
    if (carrera) window.datosFormularioMultimedia.carrera = carrera.value;
    if (materia) window.datosFormularioMultimedia.materia = materia.value;
    
    // Guardar datos de ejemplares dinámicos
    window.gruposTiposMultimedia.forEach((grupo, index) => {
        const inputUrl = document.getElementById(`multimedia_${index}_url`);
        const inputTitulo = document.getElementById(`multimedia_${index}_titulo`);
        
        if (inputUrl) {
            window.datosFormularioMultimedia[`multimedia_${index}_url`] = inputUrl.value;
        }
        if (inputTitulo) {
            window.datosFormularioMultimedia[`multimedia_${index}_titulo`] = inputTitulo.value;
        }
    });
    
    console.log('💾 Datos del formulario multimedia guardados:', window.datosFormularioMultimedia);
};

// Función para restaurar datos del formulario multimedia
window.restaurarDatosFormularioMultimedia = function() {
    if (!window.datosFormularioMultimedia) return;
    
    // Restaurar datos de campos básicos
    const profesor = document.getElementById('profesor');
    const carrera = document.getElementById('carrera');
    const materia = document.getElementById('materia');
    
    if (profesor && window.datosFormularioMultimedia.profesor) {
        profesor.value = window.datosFormularioMultimedia.profesor;
    }
    if (carrera && window.datosFormularioMultimedia.carrera) {
        carrera.value = window.datosFormularioMultimedia.carrera;
    }
    if (materia && window.datosFormularioMultimedia.materia) {
        materia.value = window.datosFormularioMultimedia.materia;
    }
    
    // Restaurar datos de ejemplares dinámicos
    window.gruposTiposMultimedia.forEach((grupo, index) => {
        const inputUrl = document.getElementById(`multimedia_${index}_url`);
        const inputTitulo = document.getElementById(`multimedia_${index}_titulo`);
        
        if (inputUrl && window.datosFormularioMultimedia[`multimedia_${index}_url`]) {
            inputUrl.value = window.datosFormularioMultimedia[`multimedia_${index}_url`];
        }
        if (inputTitulo && window.datosFormularioMultimedia[`multimedia_${index}_titulo`]) {
            inputTitulo.value = window.datosFormularioMultimedia[`multimedia_${index}_titulo`];
        }
    });
    
    console.log('🔄 Datos del formulario multimedia restaurados');
};

// Función para restaurar datos del formulario multimedia después de agregar
window.restaurarDatosFormularioMultimediaAgregar = function() {
    if (!window.datosFormularioMultimedia) return;
    
    // Solo restaurar campos básicos, no los ejemplares dinámicos
    const profesor = document.getElementById('profesor');
    const carrera = document.getElementById('carrera');
    const materia = document.getElementById('materia');
    
    if (profesor && window.datosFormularioMultimedia.profesor) {
        profesor.value = window.datosFormularioMultimedia.profesor;
    }
    if (carrera && window.datosFormularioMultimedia.carrera) {
        carrera.value = window.datosFormularioMultimedia.carrera;
    }
    if (materia && window.datosFormularioMultimedia.materia) {
        materia.value = window.datosFormularioMultimedia.materia;
    }
    
    console.log('🔄 Datos básicos del formulario multimedia restaurados después de agregar');
};

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
            <td><span class="form-control form-control-sm" style="display:inline-block;vertical-align:middle;border-bottom:2px solid #81123b;">${g.tipo}</span></td>
            <td>
                <input type='number' id='cant-mapa-${idx}' name='cant-mapa-${idx}' class='form-control form-control-sm input-cant-mapa' data-idx='${idx}' data-valor-anterior='${g.cantidad}' value='${g.cantidad}' min='1' max='5' style='display:inline-block;vertical-align:middle;'>
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
        const handler = function() {
            const idx = parseInt(this.dataset.idx);
            let val = parseInt(this.value);
            if (isNaN(val) || val < 1) val = 1;
            const prevAttr = parseInt(this.getAttribute('data-valor-anterior'));
            const prev = Number.isFinite(prevAttr) ? prevAttr : (window.gruposTiposMapa[idx]?.cantidad || 1);

            const aplicarCambio = () => {
                const datosExistentes = guardarDatosFormularioMapa();
                window.gruposTiposMapa[idx].cantidad = val;
                this.setAttribute('data-valor-anterior', val);
                window.renderizarTiposMapa();
                restaurarDatosFormularioMapaAgregar(datosExistentes);
            };

            if (val < prev) {
                if (typeof mostrarModalReducirEjemplares === 'function') {
                    mostrarModalReducirEjemplares(
                        aplicarCambio,
                        () => { this.value = prev; }
                    );
                } else {
                    if (confirm('Reducir la cantidad eliminará datos de ejemplares adicionales. ¿Confirmar?')) {
                        aplicarCambio();
                    } else {
                        this.value = prev;
                    }
                }
            } else {
                aplicarCambio();
            }
        };
        inp.addEventListener('change', handler);
        inp.addEventListener('input', handler);
    });
    // 2. Eliminar tipo (botón eliminar) con alerta de confirmación
    document.querySelectorAll('.btn-eliminar-tipo-mapa').forEach(btn => {
        btn.addEventListener('click', function() {
            const idx = parseInt(this.dataset.idx);
            // Guardar datos existentes antes de eliminar
            const datosExistentes = guardarDatosFormularioMapa();

            // Usar el modal de reducir ejemplares para unificar la UX
            if (typeof mostrarModalReducirEjemplares === 'function') {
                mostrarModalReducirEjemplares(function() {
                    // Confirmado: eliminar y re-renderizar
                    window.gruposTiposMapa.splice(idx, 1);
                    window.renderizarTiposMapa();
                    restaurarDatosFormularioMapa(datosExistentes, idx);
                });
            } else {
                // Fallback si el modal específico no está disponible
                if (confirm('Reducir tipos eliminará datos de ejemplares adicionales. ¿Confirmar?')) {
                    window.gruposTiposMapa.splice(idx, 1);
                    window.renderizarTiposMapa();
                    restaurarDatosFormularioMapa(datosExistentes, idx);
                }
            }
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
    // Validar campos de mapas
    const contenedorEjemplares = document.getElementById('contenedor-ejemplares-mapa');
    const fieldsets = contenedorEjemplares ? contenedorEjemplares.querySelectorAll('fieldset.mb-4.p-3.rounded') : [];
    
    // Si no hay fieldsets generados con las clases específicas, validar campos iniciales
    if (fieldsets.length === 0 && contenedorEjemplares) {
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
    if (contenedorEjemplares) {
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
    }
    
    // Validar campos de multimedia
    const contenedorMultimedia = document.getElementById('contenedor-ejemplares-multimedia');
    if (contenedorMultimedia && window.gruposTiposMultimedia && window.gruposTiposMultimedia.length === 0) {
        // Si no hay multimedia dinámicos, validar campos iniciales
        const urlInicial = document.getElementById('ingresar_enlace');
        const tituloInicial = document.getElementById('titulo_contenido');
        
        if (tituloInicial && tituloInicial.hasAttribute('required') && !tituloInicial.value.trim()) {
            tituloInicial.scrollIntoView({ behavior: 'smooth', block: 'center' });
            tituloInicial.focus();
            alert('Por favor, complete el campo "Título del contenido" antes de guardar.');
            return false;
        }
    } else if (contenedorMultimedia && window.gruposTiposMultimedia && window.gruposTiposMultimedia.length > 0) {
        // Si hay multimedia dinámicos, validar que tengan título
        for (let i = 0; i < window.gruposTiposMultimedia.length; i++) {
            const tituloInput = document.getElementById(`multimedia_${i}_titulo`);
            if (tituloInput && !tituloInput.value.trim()) {
                tituloInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
                tituloInput.focus();
                alert(`Por favor, complete el título del ejemplar ${i + 1} antes de guardar.`);
                return false;
            }
        }
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
            <div class="col-md-3">
                <label for="n_registro_${idx}" style="font-size: 14px;">N° de registro: <span style="color: red;">*</span></label>
                <input type="text" class="form-control form-control-sm" id="n_registro_${idx}" name="n_registro_${idx}" required />
            </div>
            <div class="col-md-3">
                <label for="denominacion_${idx}" style="font-size: 14px;">Denominación: <span style="color: red;">*</span></label>
                <input type="text" class="form-control form-control-sm" id="denominacion_${idx}" name="denominacion_${idx}" required />
            </div>
            <div class="col-md-3">
                <label for="descripcion_${idx}" style="font-size: 14px;">Descripción:</label>
                <textarea class="form-control form-control-sm textarea-wrapper" id="descripcion_${idx}" rows="2" name="descripcion_${idx}"></textarea>
            </div>
        </div>
    `;
}


// === EJEMPLARES DINÁMICOS GENERALES (Solo Proyector) ===
// Genera el HTML de un ejemplar según el tipo de material
function plantillaEjemplarMaterial(idx, tipo) {
    console.log('🔧 GENERANDO PLANTILLA:', idx, tipo);
    if (tipo === 'proyector') {
        return `
        <!-- Línea punteada -->
        <div style="
            background: repeating-linear-gradient(
                to right,
                #8B1D69 0px,
                #8B1D69 10px,
                transparent 10px,
                transparent 30px
            );
            height: 3px;
            margin: 25px 0;
            width: 100%;
        "></div>
        <div class="row mb-2">
            <div class="col-md-3">
                <label for="num_registro_${idx}" style="font-size: 14px;">N° de registro<span style="color: #dc3545; font-weight: bold; font-size: 16px;">*</span>:</label>
                <input type="text" class="form-control" id="num_registro_${idx}" name="num_registro_${idx}" required placeholder="N° de registro...">
            </div>
            <div class="col-md-3">
                <label for="modelo_pro_${idx}" style="font-size: 14px;">Modelo:</label>
                <input type="text" class="form-control" id="modelo_pro_${idx}" name="modelo_pro_${idx}" placeholder="Modelo..." />
            </div>
        </div>`;
    } else if (tipo === 'notebook') {
        return `
        <!-- Línea punteada -->
        <div style="
            background: repeating-linear-gradient(
                to right,
                #8B1D69 0px,
                #8B1D69 10px,
                transparent 10px,
                transparent 30px
            );
            height: 3px;
            margin: 25px 0;
            width: 100%;
        "></div>
        <div class="row mb-2">
            <div class="col-md-3">
                <label for="num_registro_${idx}" style="font-size: 14px;">N° de registro<span style="color: #dc3545; font-weight: bold; font-size: 16px;">*</span>:</label>
                <input type="text" class="form-control" id="num_registro_${idx}" name="num_registro_${idx}" required placeholder="N° de registro...">
            </div>
            <div class="col-md-3">
                <label for="modelo_not_${idx}" style="font-size: 14px;">Modelo:</label>
                <input type="text" class="form-control" id="modelo_not_${idx}" name="modelo_not_${idx}" placeholder="Modelo..." />
            </div>
        </div>`;
    } else if (tipo === 'libro') {
        return `
        <!-- Línea punteada -->
        <div style="
            background: repeating-linear-gradient(
                to right,
                #8B1D69 0px,
                #8B1D69 10px,
                transparent 10px,
                transparent 30px
            );
            height: 3px;
            margin: 25px 0;
            width: 100%;
        "></div>
        <div class="row mb-3">
            <div class="col-12 col-sm-3 col-lg-3">
                <div class="form-group mb-3">
                    <label style="font-size: 14px;">Ejemplar N°:</label>
                    <input type="text" class="form-control" value="${idx}" readonly style="background-color: white !important; cursor: default;">
                </div>
                <div class="form-group mb-3">
                    <label style="font-size: 14px;">N° Inventario:</label>
                    <input name="num_inventario_${idx}" type="text" class="form-control" placeholder="Escriba aquí..." />
                </div>
            </div>
            <div class="col-12 col-sm-9 col-lg-9">
                <div class="row">
                    <div class="col-12 col-sm-4 col-lg-4">
                        <div class="form-group mb-3">
                            <label style="font-size: 14px;">Sede<span class="text-danger">*</span>:</label>
                            <select name="sede_${idx}" class="form-control" required style="width: 100%;">
                                <option value="">Seleccione una sede</option>
                                <option value="La Plata">La Plata</option>
                                <option value="Abasto">Abasto</option>
                            </select>
                        </div>
                        <div class="form-group mb-3">
                            <label style="font-size: 14px;">Disponibilidad<span class="text-danger">*</span>:</label>
                            <select name="disponibilidad_${idx}" class="form-control" required style="width: 100%;">
                                <option value="">Seleccione disponibilidad</option>
                                <option value="Aula">Aula</option>
                                <option value="Domicilio">Domicilio</option>
                            </select>
                        </div>
                    </div>
                    <div class="col-12 col-sm-8 col-lg-8 form-group mb-3">
                        <label style="font-size: 14px; margin-top: 0;">Observaciones:</label>
                        <textarea name="observaciones_${idx}" class="form-control" rows="4" placeholder="Observaciones sobre este ejemplar"></textarea>
                    </div>
                </div>
            </div>
        </div>`;
    }
    return '';
}

// Generador dinámico de ejemplares para proyector, notebook y libro
window.updateRowsMaterial = function(tipo) {
    console.log('🔧 UPDATE ROWS MATERIAL LLAMADO - Tipo:', tipo);
    const cantidadInput = document.querySelector('input[name="cant_ejemplares"]');
    const containerProyector = document.getElementById('contenedor-ejemplares-proyector');
    const containerNotebook = document.getElementById('contenedor-ejemplares-notebook');
    const containerLibro = document.getElementById('contenedor-ejemplares-libro');
    const cantidad = parseInt(cantidadInput ? cantidadInput.value : 1) || 1;
    console.log('📊 DATOS:', {cantidadInput, cantidad, containerProyector, containerNotebook, containerLibro});

    // Limpiar contenedores
    if (containerProyector) containerProyector.innerHTML = '';
    if (containerNotebook) containerNotebook.innerHTML = '';
    if (containerLibro) containerLibro.innerHTML = '';

    for (let i = 1; i <= cantidad; i++) {
        if (tipo === 'proyector' && containerProyector) {
            containerProyector.insertAdjacentHTML('beforeend', plantillaEjemplarMaterial(i, 'proyector'));
        } else if (tipo === 'notebook' && containerNotebook) {
            containerNotebook.insertAdjacentHTML('beforeend', plantillaEjemplarMaterial(i, 'notebook'));
        } else if (tipo === 'libro' && containerLibro) {
            containerLibro.insertAdjacentHTML('beforeend', plantillaEjemplarMaterial(i, 'libro'));
        }
    }
};

// Inicializar evento al cargar (solo para carga directa, no dinámica)
document.addEventListener('DOMContentLoaded', function () {
    const inputCantidad = document.querySelector('input[name="cant_ejemplares"]');
    const containerProyector = document.getElementById('contenedor-ejemplares-proyector');
    const containerNotebook = document.getElementById('contenedor-ejemplares-notebook');
    const containerMapa = document.getElementById('contenedor-ejemplares-mapa');
    const containerLibro = document.getElementById('contenedor-ejemplares-libro');
    
    // Código eliminado - se maneja específicamente más abajo para cada tipo
    
    // Inicializar renderizado para formulario de mapa
    if (containerMapa) {
        window.renderizarTiposMapa();
    }
    
    // Inicializar renderizado para formulario de proyector
    const containerProyectorTipos = document.getElementById('contenedor-tipos-proyector');
    if (containerProyectorTipos) {
        window.renderizarTiposProyector();
        
        // Inicializar el botón de agregar proyector
        const btnAgregarProyector = document.getElementById('btn-agregar-proyector');
        if (btnAgregarProyector) {
            btnAgregarProyector.addEventListener('click', function() {
                window.agregarTipoProyectorDesdeInputs();
            });
        }
    }
    
    // Configurar evento dinámico para proyectores
    const cantEjemplaresProyector = document.getElementById('cant_ejemplares');
    const contenedorEjemplaresProyector = document.getElementById('contenedor-ejemplares-proyector');
    
    if (cantEjemplaresProyector && contenedorEjemplaresProyector) {
        console.log('🎯 ELEMENTOS ENCONTRADOS PARA PROYECTOR:', cantEjemplaresProyector, contenedorEjemplaresProyector);
        
        // Event listener para cambios dinámicos
        cantEjemplaresProyector.addEventListener('input', function() {
            console.log('📝 EVENT INPUT PROYECTOR - Valor:', this.value);
            window.updateRowsMaterial('proyector');
        });
        
        cantEjemplaresProyector.addEventListener('change', function() {
            console.log('🔄 EVENT CHANGE PROYECTOR - Valor:', this.value);
            window.updateRowsMaterial('proyector');
        });
        
        // Inicializar campos al cargar la página
        console.log('🚀 INICIALIZANDO PROYECTOR...');
        window.updateRowsMaterial('proyector');
    }
    // Los elementos del proyector solo existen cuando se carga dinámicamente el formulario
    
    // Configurar evento dinámico para notebooks
    const cantEjemplaresNotebook = document.getElementById('cant_ejemplares');
    const contenedorEjemplaresNotebook = document.getElementById('contenedor-ejemplares-notebook');
    
    if (cantEjemplaresNotebook && contenedorEjemplaresNotebook) {
        // Event listener para cambios dinámicos
        cantEjemplaresNotebook.addEventListener('input', function() {
            window.updateRowsMaterial('notebook');
        });
        
        cantEjemplaresNotebook.addEventListener('change', function() {
            window.updateRowsMaterial('notebook');
        });
        
        // Inicializar campos al cargar la página
        window.updateRowsMaterial('notebook');
    }
    
    // Inicializar renderizado para formulario de varios (nueva implementación)
    const containerVariosNuevo = document.getElementById('contenedor-tipos-varios-nuevo');
    if (containerVariosNuevo) {
        window.renderizarTiposVariosNuevo();
    }
    
    // Inicialización para multimedia
    const contenedorMultimedia = document.getElementById('contenedor-tipos-multimedia');
    if (contenedorMultimedia) {
        console.log('🎯 Inicializando multimedia');
        window.renderizarTiposMultimedia();
    }
});

// === FUNCIONES ESPECÍFICAS PARA VARIOS (NUEVA IMPLEMENTACIÓN) ===
window.gruposTiposVariosNuevo = [];

window.renderizarTiposVariosNuevo = function() {
    const contenedor = document.getElementById('contenedor-tipos-varios-nuevo');
    if (!contenedor) return;

    let html = '';
    
    // Filtrar solo elementos dinámicos (excluir el primer elemento que es del formulario estático)
    const elementosDinamicos = window.gruposTiposVariosNuevo && window.gruposTiposVariosNuevo.length > 1 
        ? window.gruposTiposVariosNuevo.slice(1) 
        : [];
    
    elementosDinamicos.forEach((grupo, index) => {
        // Usar el índice original para mantener la consistencia con los datos
        const originalIndex = index + 1;
        html += `
        <div class="card mb-3" style="border: 1px solid #dee2e6;">
            <div class="card-header d-flex justify-content-between align-items-center" style="background-color: #f8f9fa; padding: 0.75rem;">
                <h6 class="mb-0" style="color: #495057;">
                    <strong>Tipo a registrar:</strong> ${grupo.tipo}
                </h6>
                <button type="button" class="btn btn-outline-danger btn-sm" onclick="eliminarGrupoTipoVariosNuevo(${originalIndex})">
                    <i class="fas fa-trash"></i> Eliminar
                </button>
            </div>
            <div class="card-body" style="padding: 1rem;">
                <div class="row mb-2">
                    <div class="col-md-12">
                        <div class="d-flex align-items-center gap-3">
                            <div class="flex-grow-1">
                                <label class="form-label small mb-1"><strong>Cantidad de ejemplares:</strong></label>
                                <input type="number" 
                                       id="input-cantidad-varios-${originalIndex}"
                                       class="form-control form-control-sm" 
                                       value="${grupo.cantidad}" 
                                       min="1" 
                                       data-valor-anterior="${grupo.cantidad}"
                                       onchange="actualizarCantidadVariosNuevo(${originalIndex}, this.value)"
                                       oninput="actualizarCantidadVariosNuevo(${originalIndex}, this.value)"
                                       style="max-width: 120px;">
                            </div>
                        </div>
                    </div>
                </div>
                
                <div id="ejemplares-varios-nuevo-${originalIndex}">
                    <!-- Los ejemplares se generarán aquí -->
                </div>
            </div>
        </div>`;
    });

    contenedor.innerHTML = html;
    
    // Generar ejemplares para cada grupo dinámico usando el índice original
    elementosDinamicos.forEach((grupo, index) => {
        const originalIndex = index + 1;
        generarEjemplaresVariosNuevo(originalIndex, grupo.cantidad);
    });
};

window.agregarGrupoTipoVariosNuevo = function(tipo, cantidad) {
    window.gruposTiposVariosNuevo.push({ tipo, cantidad });
    window.renderizarTiposVariosNuevo();
};

window.agregarTipoVariosNuevoDesdeInputs = function(inputTipoId = 'input-nuevo-tipo-varios', inputCantId = 'input-nueva-cant-varios') {
    const inputTipo = document.getElementById(inputTipoId);
    const inputCant = document.getElementById(inputCantId);
    
    if (!inputTipo || !inputCant) return;
    
    const tipo = inputTipo.value.trim();
    const cantidad = parseInt(inputCant.value) || 1;
    
    if (tipo === '') {
        alert('Por favor, ingrese un tipo de material.');
        return;
    }
    
    window.agregarGrupoTipoVariosNuevo(tipo, cantidad);
    
    // Limpiar inputs
    inputTipo.value = '';
    inputCant.value = '1';
};

window.eliminarGrupoTipoVariosNuevo = function(index) {
    // Usar el modal genérico de alerta para confirmar eliminación
    if (typeof mostrarModalAlerta === 'function') {
        mostrarModalAlerta(function() {
            window.gruposTiposVariosNuevo.splice(index, 1);
            window.renderizarTiposVariosNuevo();
        });
    } else {
        // Fallback si no está disponible el modal
        if (confirm('¿Está seguro de que desea eliminar este tipo de material?')) {
            window.gruposTiposVariosNuevo.splice(index, 1);
            window.renderizarTiposVariosNuevo();
        }
    }
};

window.actualizarCantidadVariosNuevo = function(index, nuevaCantidad) {
    const input = document.getElementById(`input-cantidad-varios-${index}`);
    const prevAttr = input ? parseInt(input.getAttribute('data-valor-anterior')) : null;
    const prev = Number.isFinite(prevAttr) ? prevAttr : (window.gruposTiposVariosNuevo[index]?.cantidad || 1);
    const cantidad = parseInt(nuevaCantidad) || 1;

    const aplicarCambio = function() {
        if (input) input.setAttribute('data-valor-anterior', cantidad);
        if (window.gruposTiposVariosNuevo[index]) {
            window.gruposTiposVariosNuevo[index].cantidad = cantidad;
        }
        generarEjemplaresVariosNuevo(index, cantidad);
        console.log(`✅ Cantidad actualizada para grupo ${index}: ${cantidad}`);
    };

    if (cantidad < prev) {
        if (typeof mostrarModalReducirEjemplares === 'function') {
            mostrarModalReducirEjemplares(
                aplicarCambio,
                function() { if (input) input.value = prev; }
            );
        } else {
            // Fallback sin modal
            if (confirm('Reducir la cantidad eliminará datos de ejemplares adicionales. ¿Confirmar?')) {
                aplicarCambio();
            } else {
                if (input) input.value = prev;
            }
        }
    } else {
        aplicarCambio();
    }
};

function generarEjemplaresVariosNuevo(grupoIndex, cantidad) {
    const contenedor = document.getElementById(`ejemplares-varios-nuevo-${grupoIndex}`);
    if (!contenedor) return;
    
    let html = '';
    for (let i = 1; i <= cantidad; i++) {
        html += `
        <div class="row mb-2" style="border-left: 3px solid #ffc107; padding-left: 10px; margin-left: 5px;">
            <div class="col-md-1">
                <label class="form-label small"><strong>N° Regis.</strong></label>
                <input type="text" 
                       class="form-control form-control-sm" 
                       name="varios_${grupoIndex}_${i}_registro" 
                       placeholder="N° Registro" 
                       required>
            </div>
            <div class="col-md-3">
                <label class="form-label small"><strong>Denominación</strong></label>
                <input type="text" 
                       class="form-control form-control-sm" 
                       name="varios_${grupoIndex}_${i}_denominacion" 
                       placeholder="Denominación" 
                       required>
            </div>
            <div class="col-md-6">
                <label class="form-label small"><strong>Descripción</strong></label>
                <textarea class="form-control form-control-sm" 
                          name="varios_${grupoIndex}_${i}_descripcion" 
                          placeholder="Descripción del material" 
                          rows="2" 
                          required></textarea>
            </div>
        </div>`;
    }
    contenedor.innerHTML = html;
}

// === FUNCIONES ESPECÍFICAS PARA PROYECTORES ===
window.gruposTiposProyector = [];

window.renderizarTiposProyector = function() {
    const contenedor = document.getElementById('contenedor-tipos-proyector');
    if (!contenedor) return;

    let html = '';
    
    window.gruposTiposProyector.forEach((grupo, index) => {
        html += `
        <div class="card mb-3" style="border: 1px solid #dee2e6;">
            <div class="card-header d-flex justify-content-between align-items-center" style="background-color: #f8f9fa; padding: 0.75rem;">
                <h6 class="mb-0" style="color: #495057;">
                    <strong>Tipo a registrar:</strong> ${grupo.tipo}
                </h6>
                <button type="button" class="btn btn-outline-danger btn-sm" onclick="eliminarGrupoTipoProyector(${index})">
                    <i class="fas fa-trash"></i> Eliminar
                </button>
            </div>
            <div class="card-body" style="padding: 1rem;">
                <div class="row mb-2">
                    <div class="col-md-12">
                        <div class="d-flex align-items-center gap-3">
                            <div class="flex-grow-1">
                                <label class="form-label small mb-1"><strong>Cantidad de ejemplares:</strong></label>
                                <input type="number" 
                                       id="input-cantidad-proyector-${index}"
                                       class="form-control form-control-sm" 
                                       value="${grupo.cantidad}" 
                                       min="1" 
                                       data-valor-anterior="${grupo.cantidad}"
                                       onchange="actualizarCantidadProyector(${index}, this.value)"
                                       oninput="actualizarCantidadProyector(${index}, this.value)"
                                       style="max-width: 120px;">
                            </div>
                        </div>
                    </div>
                </div>
                
                <div id="ejemplares-proyector-${index}">
                    <!-- Los ejemplares se generarán aquí -->
                </div>
            </div>
        </div>`;
    });

    contenedor.innerHTML = html;
    
    // Generar ejemplares para cada grupo
    window.gruposTiposProyector.forEach((grupo, index) => {
        generarEjemplaresProyector(index, grupo.cantidad);
    });
};

window.agregarGrupoTipoProyector = function(tipo, cantidad) {
    window.gruposTiposProyector.push({ tipo, cantidad });
    window.renderizarTiposProyector();
};

window.agregarTipoProyectorDesdeInputs = function(inputTipoId = 'tipo-proyector', inputCantId = 'cant_ejemplares') {
    const inputTipo = document.getElementById(inputTipoId);
    const inputCant = document.getElementById(inputCantId);
    
    if (!inputTipo || !inputCant) return;
    
    const tipo = inputTipo.value.trim();
    const cantidad = parseInt(inputCant.value) || 1;
    
    if (tipo === '') {
        alert('Por favor, ingrese un tipo de proyector.');
        return;
    }
    
    window.agregarGrupoTipoProyector(tipo, cantidad);
    
    // Limpiar inputs
    inputTipo.value = '';
    inputCant.value = '1';
};

window.eliminarGrupoTipoProyector = function(index) {
    const ejecutar = function() {
        window.gruposTiposProyector.splice(index, 1);
        window.renderizarTiposProyector();
        console.log('✅ Tipo de proyector eliminado tras confirmar');
    };
    if (typeof mostrarModalAlerta === 'function') {
        mostrarModalAlerta(ejecutar);
    } else {
        if (confirm('¿Está seguro de que desea eliminar este tipo de proyector?')) ejecutar();
    }
};

window.actualizarCantidadProyector = function(index, nuevaCantidad) {
    const input = document.getElementById(`input-cantidad-proyector-${index}`);
    const prevAttr = input ? parseInt(input.getAttribute('data-valor-anterior')) : null;
    const prev = Number.isFinite(prevAttr) ? prevAttr : (window.gruposTiposProyector[index]?.cantidad || 1);
    const cantidad = parseInt(nuevaCantidad) || 1;

    const aplicarCambio = function() {
        if (input) input.setAttribute('data-valor-anterior', cantidad);
        if (window.gruposTiposProyector[index]) {
            window.gruposTiposProyector[index].cantidad = cantidad;
        }
        generarEjemplaresProyector(index, cantidad);
        console.log(`✅ Cantidad actualizada para tipo proyector ${index}: ${cantidad}`);
    };

    if (cantidad < prev) {
        if (typeof mostrarModalReducirEjemplares === 'function') {
            mostrarModalReducirEjemplares(
                aplicarCambio,
                function() { if (input) input.value = prev; }
            );
        } else {
            if (confirm('Reducir la cantidad eliminará datos de ejemplares adicionales. ¿Confirmar?')) {
                aplicarCambio();
            } else {
                if (input) input.value = prev;
            }
        }
    } else {
        aplicarCambio();
    }
};

function generarEjemplaresProyector(grupoIndex, cantidad) {
    const contenedor = document.getElementById(`ejemplares-proyector-${grupoIndex}`);
    if (!contenedor) return;
    
    let html = '';
    for (let i = 1; i <= cantidad; i++) {
        html += `
        <div class="row mb-2" style="border-left: 3px solid #28a745; padding-left: 10px; margin-left: 5px;">
            <div class="col-md-1">
                <label class="form-label small"><strong>N° Regis.<span class="text-danger">*</span></strong></label>
                <input type="text" 
                       class="form-control form-control-sm" 
                       name="proyector_${grupoIndex}_${i}_registro" 
                       placeholder="N° Registro" 
                       required>
            </div>
            <div class="col-md-3">
                <label class="form-label small"><strong>Denominación</strong></label>
                <input type="text" 
                       class="form-control form-control-sm" 
                       name="proyector_${grupoIndex}_${i}_denominacion" 
                       placeholder="Denominación" 
                       required>
            </div>
            <div class="col-md-6">
                <label class="form-label small"><strong>Descripción</strong></label>
                <textarea class="form-control form-control-sm" 
                          name="proyector_${grupoIndex}_${i}_descripcion" 
                          placeholder="Descripción del proyector" 
                          rows="2" 
                          required></textarea>
            </div>
        </div>`;
    }
     contenedor.innerHTML = html;
}

// ===== FUNCIONES PARA MULTIMEDIA =====

// Variable global para almacenar los grupos de tipos de multimedia
window.gruposTiposMultimedia = [];

// Función para renderizar los tipos de multimedia
window.renderizarTiposMultimedia = function() {
    const contenedor = document.getElementById('contenedor-tipos-multimedia');
    if (!contenedor) {
        console.log('⚠️ Contenedor tipos multimedia no encontrado');
        return;
    }
    
    let html = '';
    
    // Mostrar tabla resumen si hay multimedia agregados
    if (window.gruposTiposMultimedia.length > 0) {
        html += `
        <div class="table-responsive mb-3">
            <table class="table table-sm table-bordered">
                <thead class="table-light">
                    <tr>
                        <th>URL</th>
                        <th>Título</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>`;
        
        window.gruposTiposMultimedia.forEach((grupo, index) => {
            html += `
                    <tr>
                        <td>${grupo.url || 'Sin URL'}</td>
                        <td>${grupo.titulo || 'Sin título'}</td>
                        <td>
                            <button type="button" class="btn btn-outline-danger btn-sm" onclick="eliminarGrupoTipoMultimedia(${index})">
                                <i class="fas fa-trash"></i>
                            </button>
                        </td>
                    </tr>`;
        });
        
        html += `
                </tbody>
            </table>
        </div>`;
    }
    
    contenedor.innerHTML = html;
    
    // Generar ejemplares dinámicos
    generarEjemplaresMultimedia();
    
    // Manejar atributo required de campos iniciales
    const urlInicial = document.getElementById('ingresar_enlace');
    const tituloInicial = document.getElementById('titulo_contenido');
    
    if (window.gruposTiposMultimedia.length > 0) {
        // Si hay multimedia dinámicos, los campos iniciales no son requeridos
        if (urlInicial) urlInicial.removeAttribute('required');
        if (tituloInicial) tituloInicial.removeAttribute('required');
    } else {
        // Si no hay multimedia dinámicos, el título inicial es requerido
        if (tituloInicial) tituloInicial.setAttribute('required', '');
    }
};

// Función para agregar un nuevo grupo de tipo multimedia
window.agregarGrupoTipoMultimedia = function(url, titulo) {
    window.gruposTiposMultimedia.push({ url, titulo });
    window.renderizarTiposMultimedia();
};

// Función para agregar tipo multimedia desde los inputs
window.agregarTipoMultimediaDesdeInputs = function() {
    const inputUrl = document.getElementById('ingresar_enlace');
    const inputTitulo = document.getElementById('titulo_contenido');
    
    if (!inputUrl || !inputTitulo) {
        console.log('⚠️ Campos URL o título no encontrados');
        return;
    }
    
    const url = inputUrl.value.trim();
    const titulo = inputTitulo.value.trim();
    
    if (titulo === '') {
        alert('Por favor, ingrese un título para el contenido multimedia.');
        inputTitulo.focus();
        return;
    }
    
    // Guardar datos del formulario antes de agregar
    if (typeof guardarDatosFormularioMultimedia === 'function') {
        guardarDatosFormularioMultimedia();
    }
    
    window.agregarGrupoTipoMultimedia(url, titulo);
    
    // Limpiar inputs
    inputUrl.value = '';
    inputTitulo.value = '';
    
    // Restaurar datos del formulario
    if (typeof restaurarDatosFormularioMultimediaAgregar === 'function') {
        restaurarDatosFormularioMultimediaAgregar();
    }
    
    console.log('✅ Multimedia agregado:', { url, titulo });
};

// Función para eliminar un grupo de tipo multimedia
window.eliminarGrupoTipoMultimedia = function(index) {
    const ejecutar = function() {
        window.gruposTiposMultimedia.splice(index, 1);
        window.renderizarTiposMultimedia();
        console.log('✅ Tipo de multimedia eliminado tras confirmar');
    };
    if (typeof mostrarModalAlerta === 'function') {
        mostrarModalAlerta(ejecutar);
    } else {
        if (confirm('¿Está seguro de que desea eliminar este tipo de multimedia?')) ejecutar();
    }
};

// Función para generar ejemplares dinámicos de multimedia
function generarEjemplaresMultimedia() {
    const contenedor = document.getElementById('contenedor-ejemplares-multimedia');
    if (!contenedor) {
        console.log('⚠️ Contenedor ejemplares multimedia no encontrado');
        return;
    }
    
    let html = '';
    
    // Generar fieldsets para cada multimedia agregado
    window.gruposTiposMultimedia.forEach((grupo, index) => {
        html += `
        <div class="dotted-separator mb-3"></div>
        <fieldset class="border p-3 mb-3" style="border-radius: 8px; background-color: #f8f9fa;">
            <legend class="w-auto px-2" style="font-size: 1rem; font-weight: bold; color: #495057;">
                Ejemplar ${index + 1}
            </legend>
            <div class="row">
                <div class="col-md-3">
                    <label for="multimedia_${index}_url" class="form-label small">Ingresar enlace (URL)</label>
                    <div class="input-group">
                        <input type="url" 
                               class="form-control form-control-sm" 
                               id="multimedia_${index}_url" 
                               name="multimedia_${index}_url" 
                               value="${grupo.url || ''}" 
                               placeholder="URL del contenido multimedia">
                    </div>
                </div>
                <div class="col-md-6">
                    <label for="multimedia_${index}_titulo" class="form-label small">Título del contenido <span class="text-danger">*</span></label>
                    <input type="text" 
                           class="form-control form-control-sm" 
                           id="multimedia_${index}_titulo" 
                           name="multimedia_${index}_titulo" 
                           value="${grupo.titulo || ''}" 
                           required 
                           placeholder="Título del contenido">
                </div>
            </div>
        </fieldset>`;
    });
    
    contenedor.innerHTML = html;
    
    // Agregar event listeners para actualizar los datos cuando cambien los inputs
    window.gruposTiposMultimedia.forEach((grupo, index) => {
        const inputUrl = document.getElementById(`multimedia_${index}_url`);
        const inputTitulo = document.getElementById(`multimedia_${index}_titulo`);
        
        if (inputUrl) {
            inputUrl.addEventListener('input', function() {
                window.gruposTiposMultimedia[index].url = this.value;
                // Actualizar tabla resumen
                window.renderizarTiposMultimedia();
            });
        }
        
        if (inputTitulo) {
            inputTitulo.addEventListener('input', function() {
                window.gruposTiposMultimedia[index].titulo = this.value;
                // Actualizar tabla resumen
                window.renderizarTiposMultimedia();
            });
        }
    });
}
