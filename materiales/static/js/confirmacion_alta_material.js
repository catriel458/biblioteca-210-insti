document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('form_alta_material');
    const modal = new bootstrap.Modal(document.getElementById('modalConfirmacionAltaMaterial'));
    
    // Interceptar el submit del formulario
    form.addEventListener('submit', function(e) {
        e.preventDefault(); // Prevenir envío normal
        mostrarVistaPrevia();
    });
    
    function mostrarVistaPrevia() {
        // Obtener datos del formulario
        const formData = new FormData(form);
        
        // Llenar el modal con los datos del formulario
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
    }
    
    // Confirmar y enviar el formulario real
    document.getElementById('btnConfirmarAltaMaterial').addEventListener('click', function() {
        modal.hide();
        // Remover el event listener para que no intercepte el submit
        form.removeEventListener('submit', arguments.callee);
        form.submit(); // Enviar el formulario real
    });
});