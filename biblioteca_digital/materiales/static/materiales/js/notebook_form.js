document.addEventListener('DOMContentLoaded', function() {
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