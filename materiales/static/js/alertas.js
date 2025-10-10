
// Función principal que se llama al hacer clic en CANCELAR
function cancelarFormulario() {
    mostrarModalAlerta();
}

function cerrarModal() {
    ocultarModalAlerta();
}

function confirmarModal() {
    // Intentar encontrar el formulario de diferentes maneras
    let formulario = document.getElementById('alta-proyector-form');
    
    // Si no lo encuentra por ID, buscar por selector más general
    if (!formulario) {
        formulario = document.querySelector('form[data-form-type="proyector"]');
    }
    
    // Si aún no lo encuentra, buscar cualquier formulario en la página
    if (!formulario) {
        formulario = document.querySelector('form');
    }
    
    if (formulario) {
        console.log('Formulario encontrado:', formulario);
        
        // Resetear el formulario completo primero
        formulario.reset();
        
        // Luego forzar el reseteo manual de campos específicos
        
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
        
        // Limpiar el contenedor de ejemplares dinámicos si existe
        const contenedorEjemplares = document.getElementById('contenedor-ejemplares-proyector');
        if (contenedorEjemplares) {
            contenedorEjemplares.innerHTML = '';
        }
        
        // Resetear específicamente el campo de cantidad de ejemplares a 1
        const cantEjemplares = document.getElementById('cant_ejemplares');
        if (cantEjemplares) {
            cantEjemplares.value = '1';
        }
        
        // Resetear específicamente el select de sede a "Aún sin seleccionar"
        const selectSede = document.getElementById('sede');
        if (selectSede) {
            selectSede.value = '';
        }
        
        // Disparar eventos de cambio para que otros scripts se enteren del reseteo
        const event = new Event('change', { bubbles: true });
        if (cantEjemplares) cantEjemplares.dispatchEvent(event);
        if (selectSede) selectSede.dispatchEvent(event);
        
        console.log('Formulario reseteado completamente');
    } else {
        console.error('No se encontró ningún formulario en la página');
        console.log('Elementos disponibles:', document.querySelectorAll('form'));
    }
    
    // Cerrar el modal
    ocultarModalAlerta();
}

// Función para mostrar el modal de alerta
function mostrarModalAlerta() {
    const modalAlerta = document.getElementById('modal-vaciar-campos');
    const backdrop = document.getElementById('modal-backdrop');
    
    if (modalAlerta && backdrop) {
        modalAlerta.style.display = 'flex';
        backdrop.style.display = 'block';
        document.body.style.overflow = 'hidden'; // Prevenir scroll
    } else {
        console.error('Error: No se encontraron los elementos del modal');
    }
}

// Función para ocultar el modal de alerta
function ocultarModalAlerta() {
    const modalAlerta = document.getElementById('modal-vaciar-campos');
    const backdrop = document.getElementById('modal-backdrop');
    
    if (modalAlerta && backdrop) {
        modalAlerta.style.display = 'none';
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
    const formulario = document.getElementById('alta-proyector-form');
    
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
        
        // Limpiar el contenedor de ejemplares dinámicos si existe
        const contenedorEjemplares = document.getElementById('contenedor-ejemplares-proyector');
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

// Event listeners que se ejecutan cuando se carga el DOM
document.addEventListener('DOMContentLoaded', function() {
    const btnCancelarModal = document.getElementById('btn-cancelar-vaciar');
    const btnConfirmarModal = document.getElementById('btn-confirmar-vaciar');
    const backdrop = document.getElementById('modal-backdrop');
    
    // Event listener para el botón CANCELAR del modal
    if (btnCancelarModal) {
        btnCancelarModal.addEventListener('click', cancelarModal);
    }
    
    // Event listener para el botón CONFIRMAR del modal
    if (btnConfirmarModal) {
        btnConfirmarModal.addEventListener('click', confirmarVaciarCampos);
    }
    
    // Cerrar modal al hacer clic en el backdrop
    if (backdrop) {
        backdrop.addEventListener('click', ocultarModalAlerta);
    }
});