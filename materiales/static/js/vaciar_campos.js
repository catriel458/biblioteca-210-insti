// vaciar_campos.js

document.addEventListener('DOMContentLoaded', function() {
    const btnCancelar = document.getElementById('btn-cancelar-form');
    const formulario = document.getElementById('alta-proyector-form');
    const modalAlerta = document.getElementById('modal-vaciar-campos');
    const backdrop = document.getElementById('modal-backdrop');
    const btnCancelarModal = document.getElementById('btn-cancelar-vaciar');
    const btnConfirmarModal = document.getElementById('btn-confirmar-vaciar');
    
    // Verificar que todos los elementos existen
    if (!btnCancelar || !formulario || !modalAlerta || !backdrop) {
        console.error('Error: No se encontraron todos los elementos necesarios');
        return;
    }
    
    // Mostrar alerta al hacer clic en CANCELAR del formulario
    btnCancelar.addEventListener('click', function(e) {
        e.preventDefault();
        mostrarAlerta();
    });
    
    // Ocultar alerta al hacer clic en CANCELAR del modal
    btnCancelarModal.addEventListener('click', function() {
        ocultarAlerta();
    });
    
    // Vaciar campos al hacer clic en CONFIRMAR del modal
    btnConfirmarModal.addEventListener('click', function() {
        vaciarCamposFormulario();
        ocultarAlerta();
        // Opcional: redirigir o mostrar mensaje de confirmación
        // window.location.href = '/ruta-deseada/';
    });
    
    // Cerrar modal al hacer clic en el backdrop
    backdrop.addEventListener('click', function() {
        ocultarAlerta();
    });
    
    // Función para mostrar la alerta
    function mostrarAlerta() {
        modalAlerta.style.display = 'flex';
        backdrop.style.display = 'block';
        document.body.style.overflow = 'hidden'; // Prevenir scroll
    }
    
    // Función para ocultar la alerta
    function ocultarAlerta() {
        modalAlerta.style.display = 'none';
        backdrop.style.display = 'none';
        document.body.style.overflow = ''; // Restaurar scroll
    }
    
    // Función para vaciar todos los campos del formulario
    function vaciarCamposFormulario() {
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
});