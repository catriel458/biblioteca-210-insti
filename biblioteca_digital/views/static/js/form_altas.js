// === FORMULARIOS DINÁMICOS DE ALTAS ===
// Refactorizado para eliminar IIFE y dejar todo en scope global, siguiendo el modelo de form_controler.js
// Solo se exponen en window las funciones necesarias para HTML y otros scripts

// === GLOBAL ===

let config = {};
let tipos = [];
let tiposAgregados = new Set();
let gruposTiposMapa = [];

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

function agregarGrupoTipoMapa(tipo, cantidad) {
    cantidad = parseInt(cantidad);

    if (!tipo || isNaN(cantidad) || cantidad < 1) {
        alert('Debes ingresar un tipo válido.');
        return;
    }

    if (gruposTiposMapa.some(g => g.tipo.toLowerCase() === tipo.toLowerCase())) {
        alert("Ese tipo de mapa ya fue agregado.");
        return;
    }

    gruposTiposMapa.push({ tipo, cantidad });
    renderizarGruposTiposMapa();
    renderizarListaResumenTipos();  
}

function renderizarListaResumenTipos() {
    const resumenContainer = document.getElementById('bloque-tipo-cantidad');
    if (!resumenContainer) return;

    if (gruposTiposMapa.length === 0) {
        resumenContainer.innerHTML = '';
        return;
    }

    let html = '<div class="table-responsive"><table class="table table-sm table-bordered">';
    html += '<thead><tr><th>Tipo</th><th>Cantidad de ejemplares</th></tr></thead><tbody>';

    gruposTiposMapa.forEach(g => {
        html += `<tr><td>${g.tipo}</td><td>${g.cantidad}</td></tr>`;
    });

    html += '</tbody></table></div>';
    resumenContainer.innerHTML = html;
}

function renderizarGruposTiposMapa() {
    const container = document.getElementById('contenedor-ejemplares-mapa');
    if (!container) return;

    let htmlTotal = '';
    gruposTiposMapa.forEach((grupo, idxGrupo) => {
        let htmlGrupo = `
                <fieldset class="mb-4 p-3 border rounded">
                    <legend class="fw-bold mt-3">TIPO DE MAPA: <span class="text-primary">${grupo.tipo.toUpperCase()}</span></legend>
            `;
            for (let i = 0; i < grupo.cantidad; i++) {
                htmlGrupo += plantillaEjemplarMapa(`${idxGrupo}_${i}`, grupo.tipo);
            }
            htmlGrupo += '</fieldset>';
            htmlTotal += htmlGrupo;
        });

    container.innerHTML = htmlTotal;
}

function plantillaEjemplarMapa(idx, tipo = "") {
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

function agregarTipoDesdeUI() {
    const inputTipo = document.getElementById('tipo');
    if (inputTipo && inputTipo.value.trim() !== '') {
        agregarGrupoTipoMapa(inputTipo.value, 1);
    }
   return `
    <div class="row mb-2">
        <div class="col-md-3">
            <label for="profesor_${idx}">Profesor:</label>
            <input type="text" class="form-control" id="profesor_${idx}" name="profesor_${idx}" required placeholder="Nombre del profesor">
        </div>
        <div class="col-md-3">
            <label for="url_${idx}">Enlace:</label>
            <input type="url" class="form-control" id="url_${idx}" name="url_${idx}" placeholder="URL del programa">
        </div>
        <div class="col-md-3">
            <label for="carrera_${idx}">Carrera:</label>
            <input type="text" class="form-control" id="carrera_${idx}" name="carrera_${idx}" required placeholder="Carrera...">
        </div>
        <div class="col-md-3">
            <label for="materia_${idx}">Materia:</label>
            <input type="text" class="form-control" id="materia_${idx}" name="materia_${idx}" required placeholder="Materia...">
        </div>
    </div>
    `;
}

// === PROYECTOR === 
// @returns {string} HTML del bloque de ejemplar de proyector.
// === PROYECTOR ===
// @returns {string} HTML del bloque de ejemplar de proyector.
function plantillaEjemplarProyector(idx) {
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
    </div>
    `;
}

document.addEventListener('DOMContentLoaded', function () {
    const container = document.getElementById('contenedor-ejemplares-proyector');
    if (container) {
        container.insertAdjacentHTML('beforeend', plantillaEjemplarProyector(1));
    }
});

// === VARIOS ===
// (campos: tipos dinámicos, ejemplares)
function plantillaEjemplarVarios(idx) {
    return `
    <div class="row mb-2">
        <div class="col-md-3">
            <label for="tipo_${idx}">Tipo:</label>
            <input type="text" class="form-control" id="tipo_${idx}" name="tipo_${idx}" required placeholder="Tipo de material..." />
        </div>
        <div class="col-md-3">
            <label for="n_registro_${idx}">N° de registro:</label>
            <input type="text" class="form-control" id="n_registro_${idx}" name="n_registro_${idx}" required placeholder="N° de registro...">
        </div>
        <div class="col-md-3">
            <label for="descripcion_${idx}">Descripción:</label>
            <input type="text" class="form-control" id="descripcion_${idx}" name="descripcion_${idx}" required placeholder="Descripción..." />
        </div>
    </div>
    `;
}

document.addEventListener('DOMContentLoaded', function () {
    const container = document.getElementById('contenedor-ejemplares-varios');
    if (container) {
        container.insertAdjacentHTML('beforeend', plantillaEjemplarVarios(1));
    }
});


function generarHTML(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    const html = `
            <div class="card mb-4">
                <div class="card-header bg-light">
                    <h5 class="mb-0">${config.titulo}</h5>
                </div>
                <div class="card-body">
                    <div class="row mb-3">
                        <div class="col-md-8">
                            <label for="nuevo_tipo" class="form-label">Nuevo Tipo</label>
                            <div class="input-group">
                                <input type="text" class="form-control" id="nuevo_tipo" placeholder="Escriba un nuevo tipo...">
                                <button class="btn btn-primary" type="button" id="btn-agregar-tipo"><i class="bi bi-plus-lg"></i> Agregar</button>
                            </div>
                            ${config.mostrarSugerencias ? `<div id="sugerencias-tipos" class="list-group mt-2" style="display: none;"></div>` : ''}
                        </div>
                    </div>
                    <div id="lista-tipos" class="mt-4"></div>
                </div>
            </div>
            <template id="template-tipo">
                <div class="card mb-3 tipo-card" data-tipo="">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h6 class="mb-0 tipo-titulo"></h6>
                        <button type="button" class="btn btn-sm btn-outline-danger btn-eliminar-tipo"><i class="bi bi-trash"></i></button>
                    </div>
                    <div class="card-body">
                        <div class="row mb-3">
                            <div class="col-md-4">
                                <label class="form-label">Cantidad de Ejemplares</label>
                                <input type="number" class="form-control cant-ejemplares" min="1" value="1">
                            </div>
                            <div class="col-md-4 d-flex align-items-end">
                                <button type="button" class="btn btn-sm btn-outline-primary btn-generar-ejemplares"><i class="bi bi-grid-3x3-gap"></i> Generar Ejemplares</button>
                            </div>
                        </div>
                        <div class="ejemplares-container"></div>
                    </div>
                </div>
            </template>
            <template id="template-ejemplar">
                <div class="ejemplar-card mb-3 p-3 border rounded">
                    <div class="row">
                        <div class="col-md-2">
                            <label class="form-label">N° Ejemplar</label>
                            <input type="text" class="form-control" readonly>
                        </div>
                        <div class="col-md-3">
                            <label class="form-label">Sede</label>
                            <select class="form-select" name="sede[]" required>
                                <option value="">Seleccione una sede</option>
                                ${config.opcionesSede.map(sede => `<option value="${sede.value}">${sede.texto}</option>`).join('')}
                            </select>
                        </div>
                        <div class="col-md-3">
                            <label class="form-label">Estado</label>
                            <select class="form-select" name="estado[]" required>
                                <option value="disponible">Disponible</option>
                                <option value="prestado">Prestado</option>
                                <option value="en_reparacion">En reparación</option>
                                <option value="perdido">Perdido</option>
                            </select>
                        </div>
                        <div class="col-md-4">
                            <label class="form-label">Observaciones</label>
                            <input type="text" class="form-control" name="observaciones[]" placeholder="Opcional">
                        </div>
                        <!-- Campos agregados para ejemplares de mapas -->
                        <div class="col-md-4">
                            <label class="form-label">N° de registro</label>
                            <input type="text" class="form-control" name="n_registro[]" placeholder="Ingrese N° de registro">
                        </div>
                        <div class="col-md-4">
                            <label class="form-label">Denominación</label>
                            <input type="text" class="form-control" name="denominacion[]" placeholder="Ingrese denominación">
                        </div>
                        <div class="col-md-4">
                            <label class="form-label">Descripción</label>
                            <input type="text" class="form-control" name="descripcion[]" placeholder="Ingrese descripción">
                        </div>
                    </div>
                </div>
            </template>
        `;
        container.innerHTML = html;
        inicializarEventos();
    }
    function inicializarEventos() {
        const nuevoTipoInput = document.getElementById('nuevo_tipo');
        const btnAgregarTipo = document.getElementById('btn-agregar-tipo');
        const sugerenciasContainer = document.getElementById('sugerencias-tipos');
        if (config.mostrarSugerencias && nuevoTipoInput && sugerenciasContainer) {
            nuevoTipoInput.addEventListener('focus', cargarSugerencias);
            nuevoTipoInput.addEventListener('input', function() {
                const filtro = this.value.toLowerCase();
                const sugerencias = sugerenciasContainer.getElementsByClassName('list-group-item');
                Array.from(sugerencias).forEach(sugerencia => {
                    const texto = sugerencia.textContent.toLowerCase();
                    sugerencia.style.display = texto.includes(filtro) ? 'block' : 'none';
                });
                sugerenciasContainer.style.display = 'block';
            });
            document.addEventListener('click', function(e) {
                if (!e.target.closest('#nuevo_tipo') && !e.target.closest('#sugerencias-tipos')) {
                    sugerenciasContainer.style.display = 'none';
                }
            });
        }
        if (btnAgregarTipo && nuevoTipoInput) {
            btnAgregarTipo.onclick = function() {
                if (agregarTipoDesdeUI()) {
                    nuevoTipoInput.value = '';
                    if (sugerenciasContainer) sugerenciasContainer.style.display = 'none';
                }
            };
            nuevoTipoInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    if (agregarTipoDesdeUI()) {
                        this.value = '';
                        if (sugerenciasContainer) sugerenciasContainer.style.display = 'none';
                    }
                }
            });
        }
        document.addEventListener('click', function(e) {
            if (e.target.closest('.btn-eliminar-tipo')) {
                const tarjeta = e.target.closest('.tipo-card');
                if (tarjeta && confirm('¿Está seguro de eliminar este tipo y todos sus ejemplares?')) {
                    const tipo = tarjeta.dataset.tipo;
                    tiposAgregados.delete(tipo.toLowerCase());
                    tarjeta.remove();
                }
            } else if (e.target.closest('.btn-generar-ejemplares')) {
                const tarjeta = e.target.closest('.tipo-card');
                const tipo = tarjeta.dataset.tipo;
                const cantidad = parseInt(tarjeta.querySelector('.cant-ejemplares').value) || 1;
                const contenedor = tarjeta.querySelector('.ejemplares-container');
                contenedor.innerHTML = '';
                for (let i = 0; i < cantidad; i++) {
                    const ejemplar = document.getElementById('template-ejemplar').content.cloneNode(true);
                    const inputs = ejemplar.querySelectorAll('input, select');
                    const prefijo = `tipos[${tipo}][ejemplares][${i}]`;
                    inputs.forEach(input => {
                        const name = input.getAttribute('name');
                        if (name) input.name = `${prefijo}[${name.replace('[]', '')}]`;
                    });
                    ejemplar.querySelector('input[type="text"][readonly]').value = `Ejemplar ${i + 1}`;
                    contenedor.appendChild(ejemplar);
                }
            }
        });
    }
    function agregarTipoDesdeUI() {
        const input = document.getElementById('nuevo_tipo');
        if (!input || !input.value.trim()) {
            alert('Por favor ingrese un tipo válido');
            return false;
        }
        const tipo = input.value.trim();
        if (!agregarTipo(tipo)) {
            alert('Este tipo ya ha sido agregado');
            return false;
        }
        const template = document.getElementById('template-tipo');
        const tarjeta = template.content.cloneNode(true);
        const tarjetaElement = tarjeta.querySelector('.tipo-card');
        const tituloElement = tarjeta.querySelector('.tipo-titulo');
        tarjetaElement.dataset.tipo = tipo;
        tituloElement.textContent = tipo;
        document.getElementById('lista-tipos').appendChild(tarjeta);
        return true;
    }
    function cargarSugerencias() {
        const sugerenciasContainer = document.getElementById('sugerencias-tipos');
        if (!sugerenciasContainer || tipos.length === 0) return;
        sugerenciasContainer.innerHTML = '';
        tipos.forEach(tipo => {
            if (tiposAgregados.has(tipo.toLowerCase())) return;
            const sugerencia = document.createElement('button');
            sugerencia.type = 'button';
            sugerencia.className = 'list-group-item list-group-item-action';
            sugerencia.textContent = tipo;
            sugerencia.onclick = function() {
                document.getElementById('nuevo_tipo').value = tipo;
                sugerenciasContainer.style.display = 'none';
            };
            sugerenciasContainer.appendChild(sugerencia);
        });
        if (sugerenciasContainer.children.length > 0) {
            sugerenciasContainer.style.display = 'block';
        } else {
            sugerenciasContainer.style.display = 'none';
        }
    }
    if (sugerenciasContainer.children.length > 0) {
        sugerenciasContainer.style.display = 'block';
    } else {
        sugerenciasContainer.style.display = 'none';
    }
    inputTipo.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && inputTipo.value.trim() !== '') {
            e.preventDefault();
            if (cantidadWrapper) cantidadWrapper.style.display = 'block';
                if (btnWrapper) btnWrapper.style.display = 'flex';
                inputCantidad.focus();
            }
        });

        // Permitir agregar grupo con Enter en cantidad
        inputCantidad.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                if (inputTipo.value.trim() !== '' && inputCantidad.value !== '') {
                    agregarGrupoTipoMapa(inputTipo.value.trim(), parseInt(inputCantidad.value));
                    inputTipo.value = '';
                    inputCantidad.value = '';
                    if (cantidadWrapper) cantidadWrapper.style.display = 'none';
                    if (btnWrapper) btnWrapper.style.display = 'none';
                    inputTipo.focus();
                } else {
                    alert('Debes ingresar un tipo y una cantidad válida.');
                }
            }
        });

        // Si hay botón agregar, conectar evento
        if (btnAgregar) {
            btnAgregar.addEventListener('click', function() {
                if (inputTipo.value.trim() !== '' && inputCantidad.value !== '') {
                    agregarGrupoTipoMapa(inputTipo.value.trim(), parseInt(inputCantidad.value));
                    inputTipo.value = '';
                    inputCantidad.value = '';
                    if (cantidadWrapper) cantidadWrapper.style.display = 'none';
                    if (btnWrapper) btnWrapper.style.display = 'none';
                    inputTipo.focus();
                } else {
                    alert('Debes ingresar un tipo y una cantidad válida.');
                }
            });
        }
    
    if (!contenedor) {
}

// Configurar evento para el botón de generar ejemplares
const btnGenerar = form.querySelector('[data-accion="generar-ejemplares"]');
const inputCantidad = form.querySelector('input[name="cant_ejemplares"]');

if (btnGenerar && inputCantidad) {
    btnGenerar.addEventListener('click', () => {
        const cantidad = parseInt(inputCantidad.value) || 1;
        generarEjemplares(tipo, contenedorId, cantidad);
    });
}

// ... resto del código ...

// Función para agregar grupo tipo mapa
function agregarGrupoTipoMapa(tipo, cantidad) {
    // ... resto de la función ...
}

// Función para generar ejemplares
function generarEjemplares(tipo, contenedorId, cantidad) {
    // ... resto de la función ...
}

// ... resto del código ...

// Función para inicializar eventos
function inicializarEventos() {
    // ... resto de la función ...
}

// Función para agregar tipo desde UI
function agregarTipoDesdeUI() {
    // ... resto de la función ...
}

// Función para cargar sugerencias
function cargarSugerencias() {
    // ... resto de la función ...
}
