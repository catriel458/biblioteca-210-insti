document.addEventListener('DOMContentLoaded', function() {
<<<<<<< HEAD
    console.log('DOM Cargado'); // Para verificar que el script se está ejecutando
    
    const form = document.getElementById('form_alta_notebook');
    const cantEjemplaresInput = document.getElementById('cant_ejemplares');

    if (!cantEjemplaresInput) {
        console.error('No se encontró el campo de cantidad de ejemplares');
        return;
    }

    // Actualizar ejemplares cuando cambia la cantidad
    cantEjemplaresInput.addEventListener('change', function() {
        console.log('Cantidad cambió a:', this.value);
        actualizarEjemplares();
    });

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

function crearEjemplarHtml(numero) {
    return `
        <div class="ejemplar-container mb-3">
            <h6 class="mb-3">Ejemplar ${numero}</h6>
            <div class="row g-3">
                <div class="col-md-6">
                    <label class="form-label">Número de registro:</label>
                    <input type="text" class="form-control" name="numero_registro_${numero}" required>
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

function actualizarEjemplares() {
    const container = document.getElementById('contenedor-ejemplares-notebook');
    const cantidad = parseInt(document.getElementById('cant_ejemplares').value) || 1;
    
    console.log('Actualizando ejemplares:', cantidad);
    
    container.innerHTML = '';
    
    for (let i = 1; i <= cantidad; i++) {
        container.innerHTML += crearEjemplarHtml(i);
    }
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
=======
    // Referencias a elementos del DOM
    const cantEjemplaresInput = document.getElementById('cant_ejemplares');
    const contenedorEjemplares = document.getElementById('contenedor-ejemplares-notebook');
    const btnEnviarForm = document.getElementById('btn-enviar-form');
    const formulario = document.getElementById('form_alta_notebook');
    
    // Referencias a elementos del modal
    const confirmMarca = document.getElementById('confirm-marca');
    const confirmSede = document.getElementById('confirm-sede');
    const confirmCantidad = document.getElementById('confirm-cantidad');
    const confirmEjemplares = document.getElementById('confirm-ejemplares');
    
    // Inicializar el modal usando Bootstrap
    const confirmacionModal = new bootstrap.Modal(document.getElementById('confirmacionModal'));
    
    // Función para actualizar los ejemplares según la cantidad
    function actualizarEjemplares() {
        const cantEjemplares = parseInt(cantEjemplaresInput.value) || 0;
        
        // Limpiar el contenedor
        contenedorEjemplares.innerHTML = '';
        
        // Crear los campos para cada ejemplar
        for (let i = 0; i < cantEjemplares; i++) {
            const ejemplarDiv = document.createElement('div');
            ejemplarDiv.className = 'ejemplar-container border rounded p-3 mb-3';
            
            ejemplarDiv.innerHTML = `
                <h5 class="mb-3">Ejemplar ${i + 1}</h5>
                <div class="row mb-3">
                    <div class="col-6">
                        <label for="registro_${i}" class="form-label">N° de Registro:</label>
                        <input type="text" class="form-control" id="registro_${i}" name="registro[]" required placeholder="Escriba aquí...">
                    </div>
                    <div class="col-6">
                        <label for="modelo_${i}" class="form-label">Modelo:</label>
                        <input type="text" class="form-control" id="modelo_${i}" name="modelo[]" required placeholder="Escriba aquí...">
                    </div>
                </div>
            `;
            
            contenedorEjemplares.appendChild(ejemplarDiv);
        }
    }
    
    // Función para llenar el modal con los datos del formulario
    function llenarModalConfirmacion() {
        const marca = document.getElementById('marca_not').value;
        const sede = document.getElementById('sede').value;
        const cantEjemplares = cantEjemplaresInput.value;
        
        // Mostrar los datos generales
        confirmMarca.textContent = marca;
        confirmSede.textContent = document.getElementById('sede').options[document.getElementById('sede').selectedIndex].text;
        confirmCantidad.textContent = cantEjemplares;
        
        // Limpiar y llenar la sección de ejemplares
        confirmEjemplares.innerHTML = '';
        
        // Crear una tabla para mostrar los ejemplares
        const tabla = document.createElement('table');
        tabla.className = 'table table-bordered';
        
        // Crear encabezado de la tabla
        const thead = document.createElement('thead');
        thead.innerHTML = `
            <tr>
                <th>#</th>
                <th>N° de Registro</th>
                <th>Modelo</th>
            </tr>
        `;
        tabla.appendChild(thead);
        
        // Crear cuerpo de la tabla
        const tbody = document.createElement('tbody');
        
        for (let i = 0; i < parseInt(cantEjemplares); i++) {
            const registro = document.getElementById(`registro_${i}`).value;
            const modelo = document.getElementById(`modelo_${i}`).value;
            
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${i + 1}</td>
                <td>${registro}</td>
                <td>${modelo}</td>
            `;
            
            tbody.appendChild(tr);
        }
        
        tabla.appendChild(tbody);
        confirmEjemplares.appendChild(tabla);
    }
    
    // Validar el formulario antes de mostrar el modal
    function validarFormulario() {
        const marca = document.getElementById('marca_not').value;
        const sede = document.getElementById('sede').value;
        const cantEjemplares = parseInt(cantEjemplaresInput.value) || 0;
        
        if (!marca || !sede || cantEjemplares <= 0) {
            alert('Por favor complete todos los campos obligatorios');
            return false;
        }
        
        // Validar que todos los ejemplares tengan datos
        for (let i = 0; i < cantEjemplares; i++) {
            const registro = document.getElementById(`registro_${i}`).value;
            const modelo = document.getElementById(`modelo_${i}`).value;
            
            if (!registro || !modelo) {
                alert(`Por favor complete todos los datos del ejemplar ${i + 1}`);
                return false;
            }
        }
        
        return true;
    }
    
    // Event listeners
    cantEjemplaresInput.addEventListener('input', actualizarEjemplares);
    
    // Manejar el botón cancelar
    const btnCancelar = document.getElementById('btn-cancelar');
    if (btnCancelar) {
        btnCancelar.addEventListener('click', function() {
            window.history.back(); // Volver a la página anterior
        });
    }
    
    // Interceptar el envío del formulario para mostrar el modal de confirmación
    formulario.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevenir el envío normal del formulario
        
        if (validarFormulario()) {
            llenarModalConfirmacion();
            confirmacionModal.show();
        }
    });
    
    btnEnviarForm.addEventListener('click', function() {
        confirmacionModal.hide();
        formulario.submit(); // Enviar el formulario después de confirmar
    });
    
    // Inicializar los ejemplares al cargar la página
    actualizarEjemplares();
});
>>>>>>> 662dd8e45316254e97fae4e4ff99e716f2a7932b
