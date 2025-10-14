
// Variables globales para almacenar callbacks
let callbackConfirmar = null;
let callbackCancelar = null;
let callbackConfirmarReducir = null;
let callbackCancelarReducir = null;

// Función principal que se llama al hacer clic en CANCELAR
function cancelarFormulario() {
    console.log('Función cancelarFormulario ejecutada');
    mostrarModalAlerta();
}

function cerrarModal(tipo = 'vaciar') {
    if (tipo === 'reducir') {
        if (callbackCancelarReducir) {
            callbackCancelarReducir();
            callbackCancelarReducir = null;
        }
        ocultarModalReducirEjemplares();
    } else {
        if (callbackCancelar) {
            callbackCancelar();
            callbackCancelar = null;
        }
        ocultarModalAlerta();
    }
}

function confirmarModal(tipo = 'vaciar') {
    if (tipo === 'reducir') {
        if (callbackConfirmarReducir) {
            callbackConfirmarReducir();
            callbackConfirmarReducir = null;
        }
        ocultarModalReducirEjemplares();
    } else {
        if (callbackConfirmar) {
            callbackConfirmar();
            callbackConfirmar = null;
        }
        ocultarModalAlerta();
    }
}

// Función para mostrar el modal de alerta de vaciar campos
function mostrarModalAlerta(onConfirm = null, onCancel = null) {
    // Guardar callbacks
    callbackConfirmar = onConfirm;
    callbackCancelar = onCancel;
    
    const modalAlerta = document.getElementById('modal-vaciar-campos');
    const backdrop = document.getElementById('modal-backdrop');
    
    if (modalAlerta && backdrop) {
        modalAlerta.style.display = 'flex';
        backdrop.style.display = 'block';
        document.body.style.overflow = 'hidden'; // Prevenir scroll
        console.log('Modal vaciar campos mostrado correctamente');
    } else {
        console.error('Error: No se encontraron los elementos del modal vaciar campos');
    }
}

// Función para ocultar el modal de alerta de vaciar campos
function ocultarModalAlerta() {
    const modalAlerta = document.getElementById('modal-vaciar-campos');
    const backdrop = document.getElementById('modal-backdrop');
    
    if (modalAlerta && backdrop) {
        modalAlerta.style.display = 'none';
        backdrop.style.display = 'none';
        document.body.style.overflow = ''; // Restaurar scroll
    }
}

// Función para mostrar el modal de reducir ejemplares
function mostrarModalReducirEjemplares(onConfirm = null, onCancel = null) {
    // Guardar callbacks
    callbackConfirmarReducir = onConfirm;
    callbackCancelarReducir = onCancel;
    
    const modalReducir = document.getElementById('modal-reducir-ejemplares');
    const backdrop = document.getElementById('modal-backdrop');
    
    if (modalReducir && backdrop) {
        modalReducir.style.display = 'flex';
        backdrop.style.display = 'block';
        document.body.style.overflow = 'hidden'; // Prevenir scroll
        console.log('Modal reducir ejemplares mostrado correctamente');
    } else {
        console.error('Error: No se encontraron los elementos del modal reducir ejemplares');
    }
}

// Función para ocultar el modal de reducir ejemplares
function ocultarModalReducirEjemplares() {
    const modalReducir = document.getElementById('modal-reducir-ejemplares');
    const backdrop = document.getElementById('modal-backdrop');
    
    if (modalReducir && backdrop) {
        modalReducir.style.display = 'none';
        backdrop.style.display = 'none';
        document.body.style.overflow = ''; // Restaurar scroll
    }
}

// Función para el botón CANCELAR del modal
function cancelarModal() {
    ocultarModalAlerta();
}

// Función para el botón CONFIRMAR del modal
function confirmarVaciarCampos() {
    vaciarCamposFormulario();
    ocultarModalAlerta();
}

// Función para vaciar todos los campos del formulario
function vaciarCamposFormulario() {
    // Detectar qué formulario está activo
    const formularioProyector = document.getElementById('alta-proyector-form');
    const formularioNotebook = document.getElementById('alta-notebook-form');
    const formularioLibro = document.getElementById('alta-libro-form');
    
    let formulario = formularioProyector || formularioNotebook || formularioLibro;
    
    if (formulario) {
        // Resetear el formulario completo
        formulario.reset();
        
        // Limpiar inputs de texto y número
        const inputs = formulario.querySelectorAll('input[type="text"], input[type="number"], input[type="email"], input[type="tel"], input[type="date"]');
        inputs.forEach(input => {
            input.value = '';
        });
        
        // Resetear selects a su valor por defecto
        const selects = formulario.querySelectorAll('select');
        selects.forEach(select => {
            select.selectedIndex = 0;
        });
        
        // Limpiar textareas
        const textareas = formulario.querySelectorAll('textarea');
        textareas.forEach(textarea => {
            textarea.value = '';
        });
        
        // Desmarcar checkboxes y radio buttons
        const checkboxesRadios = formulario.querySelectorAll('input[type="checkbox"], input[type="radio"]');
        checkboxesRadios.forEach(input => {
            input.checked = false;
        });
        
        // Limpiar el contenedor de ejemplares dinámicos según el tipo de formulario
        let contenedorEjemplares;
        if (formularioProyector) {
            contenedorEjemplares = document.getElementById('contenedor-ejemplares-proyector');
        } else if (formularioNotebook) {
            contenedorEjemplares = document.getElementById('contenedor-ejemplares-notebook');
        } else if (formularioLibro) {
            contenedorEjemplares = document.getElementById('contenedor-ejemplares-libro');
        }
        
        if (contenedorEjemplares) {
            contenedorEjemplares.innerHTML = '';
        }
        
        // Resetear el campo de cantidad de ejemplares a 1
        const cantEjemplares = document.getElementById('cant_ejemplares');
        if (cantEjemplares) {
            cantEjemplares.value = '1';
        }
        
        // Resetear el select de sede a "Aún sin seleccionar"
        const selectSede = document.getElementById('sede');
        if (selectSede) {
            selectSede.value = '';
        }
        
        console.log('Formulario vaciado correctamente');
    }
}

// Funciones para verificar y actualizar ejemplares (usadas en form_altas.js)
function tieneEjemplaresConDatos(container, nuevaCantidad) {
    const ejemplares = container.querySelectorAll('.row.mb-3, .row.mb-2');
    
    // Verificar si alguno de los ejemplares que se eliminarían tiene datos
    for (let i = nuevaCantidad; i < ejemplares.length; i++) {
        const inputs = ejemplares[i].querySelectorAll('input[type="text"], input[type="number"], select, textarea');
        for (const input of inputs) {
            if (input.value && input.id && !input.id.includes('ejemplar') && !input.readOnly) {
                return true; // Hay al menos un campo con datos
            }
        }
    }
    
    return false;
}

// Función para actualizar los ejemplares sin mostrar alerta
function actualizarEjemplares(tipo, cantidad) {
    const containerProyector = document.getElementById('contenedor-ejemplares-proyector');
    const containerNotebook = document.getElementById('contenedor-ejemplares-notebook');
    const containerLibro = document.getElementById('contenedor-ejemplares-libro');
    
    // Limpiar contenedores
    if (containerProyector && tipo === 'proyector') containerProyector.innerHTML = '';
    if (containerNotebook && tipo === 'notebook') containerNotebook.innerHTML = '';
    if (containerLibro && tipo === 'libro') containerLibro.innerHTML = '';

    for (let i = 1; i <= cantidad; i++) {
        if (tipo === 'proyector' && containerProyector) {
            containerProyector.insertAdjacentHTML('beforeend', plantillaEjemplarMaterial(i, 'proyector'));
        } else if (tipo === 'notebook' && containerNotebook) {
            containerNotebook.insertAdjacentHTML('beforeend', plantillaEjemplarMaterial(i, 'notebook'));
        } else if (tipo === 'libro' && containerLibro) {
            containerLibro.insertAdjacentHTML('beforeend', plantillaEjemplarMaterial(i, 'libro'));
        }
    }
}

// Event listeners que se ejecutan cuando se carga el DOM
document.addEventListener('DOMContentLoaded', function() {
    // Event listeners para modal vaciar campos
    const btnCancelarModal = document.getElementById('btn-cancelar-vaciar');
    const btnConfirmarModal = document.getElementById('btn-confirmar-vaciar');
    
    // Event listeners para modal reducir ejemplares
    const btnCancelarReducir = document.getElementById('btn-cancelar-reducir');
    const btnConfirmarReducir = document.getElementById('btn-confirmar-reducir');
    
    const backdrop = document.getElementById('modal-backdrop');
    
    // Event listener para el botón CANCELAR del modal vaciar campos
    if (btnCancelarModal) {
        btnCancelarModal.addEventListener('click', function() {
            cerrarModal('vaciar');
        });
    }
    
    // Event listener para el botón CONFIRMAR del modal vaciar campos
    if (btnConfirmarModal) {
        btnConfirmarModal.addEventListener('click', function() {
            confirmarModal('vaciar');
        });
    }
    
    // Event listener para el botón CANCELAR del modal reducir ejemplares
    if (btnCancelarReducir) {
        btnCancelarReducir.addEventListener('click', function() {
            cerrarModal('reducir');
        });
    }
    
    // Event listener para el botón CONFIRMAR del modal reducir ejemplares
    if (btnConfirmarReducir) {
        btnConfirmarReducir.addEventListener('click', function() {
            confirmarModal('reducir');
        });
    }
    
    // Cerrar modal al hacer clic en el backdrop
    if (backdrop) {
        backdrop.addEventListener('click', function() {
            // Cerrar ambos modales
            ocultarModalAlerta();
            ocultarModalReducirEjemplares();
        });
    }
});