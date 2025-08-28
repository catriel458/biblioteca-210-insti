document.addEventListener('DOMContentLoaded', function() {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const form = document.getElementById('form_alta_notebook');
    const cantEjemplaresInput = document.getElementById('cant_ejemplares');

    // Actualizar ejemplares cuando cambia la cantidad
    cantEjemplaresInput.addEventListener('change', actualizarEjemplares);

    // Inicializar con un ejemplar
    actualizarEjemplares();

    // Validación del formulario
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        if (!validarFormulario()) {
            return;
        }
        mostrarModalConfirmacion();
    });

    // Botón enviar del modal
    document.getElementById('btn-enviar-form').addEventListener('click', enviarFormulario);
});

function validarFormulario() {
    const marca = document.getElementById('marca_not').value.trim();
    const sede = document.getElementById('sede').value;
    const cantEjemplares = document.getElementById('cant_ejemplares').value;

    if (marca === '') {
        mostrarError('Por favor ingrese la marca');
        return false;
    }
    if (sede === '') {
        mostrarError('Por favor seleccione una sede');
        return false;
    }
    if (cantEjemplares < 1) {
        mostrarError('La cantidad de ejemplares debe ser mayor a 0');
        return false;
    }
    return true;
}

function actualizarEjemplares() {
    const container = document.getElementById('contenedor-ejemplares-notebook');
    const cantidad = parseInt(document.getElementById('cant_ejemplares').value);
    
    container.innerHTML = '';
    
    for (let i = 1; i <= cantidad; i++) {
        container.innerHTML += crearEjemplarHtml(i);
    }
}

function crearEjemplarHtml(numero) {
    return `
        <div class="ejemplar-container">
            <h6>Ejemplar ${numero}</h6>
            <div class="row">
                <div class="col-md-6">
                    <label class="form-label">Número de serie:</label>
                    <input type="text" class="form-control" name="numero_serie_${numero}" required>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Estado:</label>
                    <select class="form-select" name="estado_${numero}" required>
                        <option value="">Seleccione un estado</option>
                        <option value="nuevo">Nuevo</option>
                        <option value="usado">Usado</option>
                    </select>
                </div>
            </div>
        </div>
    `;
}

async function enviarFormulario() {
    try {
        const form = document.getElementById('form_alta_notebook');
        const formData = new FormData(form);
        
        const response = await fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        });
        
        if (!response.ok) throw new Error('Error al guardar');
        
        const data = await response.json();
        if (data.success) {
            mostrarMensaje('Notebook guardada exitosamente', 'success');
            setTimeout(() => window.location.reload(), 2000);
        }
    } catch (error) {
        mostrarError('Error al guardar la notebook: ' + error.message);
    }
}

function mostrarError(mensaje) {
    const errorDiv = document.getElementById('errores');
    errorDiv.textContent = mensaje;
    errorDiv.classList.remove('d-none');
    setTimeout(() => errorDiv.classList.add('d-none'), 5000);
}

function mostrarMensaje(mensaje, tipo) {
    const mensajeDiv = document.getElementById('mensajes');
    mensajeDiv.textContent = mensaje;
    mensajeDiv.classList.remove('d-none');
    setTimeout(() => mensajeDiv.classList.add('d-none'), 5000);
}

function mostrarModalConfirmacion() {
    // Actualizar datos en el modal
    document.getElementById('confirm-marca').textContent = document.getElementById('marca_not').value;
    document.getElementById('confirm-sede').textContent = document.getElementById('sede').options[document.getElementById('sede').selectedIndex].text;
    document.getElementById('confirm-cantidad').textContent = document.getElementById('cant_ejemplares').value;
    
    // Mostrar el modal
    new bootstrap.Modal(document.getElementById('confirmacionModal')).show();
}