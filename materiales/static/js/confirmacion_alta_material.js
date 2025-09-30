document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('form_alta_material');
    const modalElement = document.getElementById('modalConfirmacionAltaMaterial');
    let modal = null;
    
    // Solo inicializar el modal si el elemento existe
    if (modalElement) {
        try {
            modal = new bootstrap.Modal(modalElement);
        } catch (error) {
            console.warn('Error inicializando modal:', error);
            modal = null;
        }
    }
    
    // Interceptar el submit del formulario
    form.addEventListener('submit', function(e) {
        e.preventDefault(); // Prevenir envío normal
        mostrarVistaPrevia();
    });
    
    function mostrarVistaPrevia() {
        // Validar campos dinámicos de ejemplares antes de mostrar el modal
        if (typeof window.validarCamposDinamicosEjemplares === 'function') {
            if (!window.validarCamposDinamicosEjemplares()) {
                return; // No mostrar el modal si la validación falla
            }
        }
        
        // Obtener datos del formulario
        const formData = new FormData(form);
        
        // Llenar el modal con los datos del formulario (solo si el modal existe)
        if (modal && modalElement) {
            document.getElementById('confirmTipoMaterial').textContent = 'LIBRO';
            document.getElementById('confirmTitulo').textContent = formData.get('titulo') || 'Sin especificar';
            document.getElementById('confirmAutor').textContent = formData.get('autor') || 'Sin especificar';
            document.getElementById('confirmEditorial').textContent = formData.get('editorial') || 'Sin especificar';
            document.getElementById('confirmDescripcion').textContent = formData.get('descripcion') || 'Sin especificar';
            document.getElementById('confirmSiglasAutor').textContent = formData.get('siglas_autor_titulo') || 'Sin especificar';
            document.getElementById('confirmClasificacion').textContent = formData.get('clasificacion_cdu') || 'Sin especificar';
            document.getElementById('confirmPalabrasClave').textContent = formData.get('etiqueta_palabra_clave') || 'Sin especificar';
            document.getElementById('confirmSede').textContent = form.querySelector('[name="sede"] option:checked')?.text || 'Sin especificar';
            document.getElementById('confirmDisponibilidad').textContent = form.querySelector('[name="disponibilidad"] option:checked')?.text || 'Sin especificar';
            document.getElementById('confirmEjemplarNum').textContent = formData.get('num_inventario') || 'Sin especificar';
            document.getElementById('confirmObservaciones').textContent = formData.get('observaciones') || 'Sin observaciones';
            
            // Mostrar el modal
            modal.show();
        } else {
            // Si no hay modal, enviar directamente el formulario
            form.submit();
        }
    }
    
    // Confirmar y enviar el formulario real (solo si el botón existe)
    const btnConfirmar = document.getElementById('btnConfirmarAltaMaterial');
    if (btnConfirmar && modal) {
        btnConfirmar.addEventListener('click', function() {
            modal.hide();
            // Remover el event listener para que no intercepte el submit
            form.removeEventListener('submit', arguments.callee);
            form.submit(); // Enviar el formulario real
        });
    }
});