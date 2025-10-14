
// Función principal que se llama al hacer clic en CANCELAR
function cancelarFormulario() {
    console.log('Función cancelarFormulario ejecutada');
    mostrarModalAlerta();
}

function cerrarModal() {
    ocultarModalAlerta();
}

function confirmarModal() {
    // Buscar el formulario activo en la página
    let formulario = null;
    
    // Intentar encontrar el formulario por tipo de formulario
    const tiposFormulario = ['programa', 'proyector', 'multimedia', 'varios', 'mapa', 'notebook'];
    
    for (const tipo of tiposFormulario) {
        const formPorTipo = document.querySelector(`form[data-form-type="${tipo}"]`);
        if (formPorTipo) {
            formulario = formPorTipo;
            console.log(`Formulario encontrado por tipo: ${tipo}`);
            break;
        }
    }
    
    // Si no lo encuentra por tipo, buscar cualquier formulario
    if (!formulario) {
        formulario = document.querySelector('form');
        console.log('Formulario encontrado genérico');
    }
    
    if (formulario) {
        console.log('Formulario encontrado:', formulario);
        
        // Resetear el formulario completo primero
        formulario.reset();
        
        // Luego forzar el reseteo manual de campos específicos
        
        // Limpiar inputs de texto, número, email, tel, date y url
        const inputs = formulario.querySelectorAll('input[type="text"], input[type="number"], input[type="email"], input[type="tel"], input[type="date"], input[type="url"]');
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
        
        // Limpiar contenedores de ejemplares dinámicos según el tipo de formulario
        const tiposContenedores = ['programa', 'proyector', 'multimedia', 'varios', 'mapa', 'notebook'];
        tiposContenedores.forEach(tipo => {
            const contenedor = document.getElementById(`contenedor-ejemplares-${tipo}`);
            if (contenedor) {
                contenedor.innerHTML = '';
            }
        });
        
        // Resetear específicamente el campo de cantidad de ejemplares a 1 si existe
        const cantEjemplares = document.getElementById('cant_ejemplares');
        if (cantEjemplares) {
            cantEjemplares.value = '1';
        }
        
        // Resetear específicamente los selects de materia y carrera
        const selectMateria = document.getElementById('materia');
        if (selectMateria) {
            selectMateria.innerHTML = '<option value="">Primero seleccione una carrera</option>';
            selectMateria.disabled = true;
        }
        
        const selectCarrera = document.getElementById('carrera');
        if (selectCarrera) {
            selectCarrera.value = '';
        }
        
        // Disparar eventos de cambio para que otros scripts se enteren del reseteo
        const event = new Event('change', { bubbles: true });
        if (cantEjemplares) cantEjemplares.dispatchEvent(event);
        if (selectCarrera) selectCarrera.dispatchEvent(event);
        
        console.log('Formulario reseteado completamente');
    } else {
        console.error('No se encontró ningún formulario en la página');
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
        console.log('Modal mostrado correctamente');
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