// alta_material.js

document.addEventListener('DOMContentLoaded', function() {
    console.log('Formulario Alta Material inicializado');
    
    // Referencias a elementos
    const cantEjemplaresSelect = document.getElementById('cant_ejemplares');
    const contenedorEjemplares = document.getElementById('contenedor-ejemplares-proyector');
    const tipoMaterialSelect = document.getElementById('tipo_material');
    const formulario = document.querySelector('form');
    const btnCancelar = document.querySelector('.btn-cancelar');
    const btnGuardar = document.querySelector('.btn-guardar');

    // Manejar cambio en cantidad de ejemplares
    cantEjemplaresSelect.addEventListener('change', function() {
        const cantidad = parseInt(this.value);
        generarEjemplaresAdicionales(cantidad);
    });

    // Función para generar ejemplares adicionales
    function generarEjemplaresAdicionales(cantidad) {
        // Limpiar contenedor
        contenedorEjemplares.innerHTML = '';
        
        // Si hay más de 1 ejemplar, generar campos adicionales
        if (cantidad > 1) {
            for (let i = 2; i <= cantidad; i++) {
                const ejemplarDiv = document.createElement('div');
                ejemplarDiv.className = 'row mb-4 ejemplar-adicional';
                ejemplarDiv.setAttribute('data-ejemplar', i);
                
                ejemplarDiv.innerHTML = `
                    <div class="col-3">
                        <label for="n_registro_${i}" class="form-label">N° Registro ${i}<span class="required-asterisk">*</span></label>
                        <input type="text" class="form-control registro-input" id="n_registro_${i}" name="n_registro_${i}" placeholder="Escriba aquí..." required>
                    </div>
                    <div class="col-3">
                        <label for="modelo_${i}" class="form-label">Modelo ${i}</label>
                        <input type="text" class="form-control modelo-input" id="modelo_${i}" name="modelo_${i}" placeholder="Escriba aquí...">
                    </div>
                `;
                
                contenedorEjemplares.appendChild(ejemplarDiv);
            }
            
            // Aplicar validación a los nuevos campos
            aplicarValidacionCampos();
        }
    }

    // Manejar cambio de tipo de material
    tipoMaterialSelect.addEventListener('change', function() {
        const tipoMaterial = this.value;
        
        // Cambiar el ID del contenedor según el tipo
        contenedorEjemplares.id = `contenedor-ejemplares-${tipoMaterial}`;
        
        // Limpiar contenedor al cambiar tipo
        contenedorEjemplares.innerHTML = '';
        
        // Resetear cantidad a 1
        cantEjemplaresSelect.value = '1';
        
        // Lógica específica por tipo de material
        switch(tipoMaterial) {
            case 'proyector':
                console.log('Modo proyector seleccionado');
                break;
            case 'notebook':
                console.log('Modo notebook seleccionado');
                break;
            case 'tablet':
                console.log('Modo tablet seleccionado');
                break;
            default:
                console.log('Otro tipo de material seleccionado');
                break;
        }
    });

    // Manejo del formulario
    formulario.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Validar formulario
        if (!validarFormulario()) {
            return;
        }
        
        // Mostrar loading en botón
        btnGuardar.disabled = true;
        btnGuardar.textContent = 'GUARDANDO...';
        
        // Recopilar datos del formulario
        const formData = new FormData(this);
        const datos = {
            tipo_material: formData.get('tipo_material'),
            cant_ejemplares: formData.get('cant_ejemplares'),
            sede: formData.get('sede'),
            ejemplares: []
        };
        
        // Recopilar datos de ejemplares
        const cantidad = parseInt(formData.get('cant_ejemplares'));
        for (let i = 1; i <= cantidad; i++) {
            const suffix = i === 1 ? '' : `_${i}`;
            datos.ejemplares.push({
                numero: i,
                n_registro: formData.get(`n_registro${suffix}`),
                modelo: formData.get(`modelo${suffix}`) || ''
            });
        }
        
        console.log('Datos a enviar:', datos);
        
        // Simular envío (reemplazar con tu lógica de envío real)
        setTimeout(() => {
            // Aquí harías tu petición AJAX real
            /*
            fetch('/api/alta-material/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify(datos)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    mostrarMensaje('Material guardado exitosamente', 'success');
                    limpiarFormulario();
                } else {
                    mostrarMensaje('Error al guardar: ' + data.message, 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                mostrarMensaje('Error de conexión', 'error');
            })
            .finally(() => {
                btnGuardar.disabled = false;
                btnGuardar.textContent = 'GUARDAR';
            });
            */
            
            // Para demostración
            btnGuardar.disabled = false;
            btnGuardar.textContent = 'GUARDAR';
            mostrarMensaje('Material guardado exitosamente (demo)', 'success');
        }, 1500);
    });

    // Validar formulario
    function validarFormulario() {
        let esValido = true;
        const camposRequeridos = formulario.querySelectorAll('[required]');
        
        camposRequeridos.forEach(campo => {
            if (!campo.value.trim()) {
                marcarCampoInvalido(campo);
                esValido = false;
            } else {
                marcarCampoValido(campo);
            }
        });
        
        if (!esValido) {
            mostrarMensaje('Por favor complete todos los campos requeridos', 'error');
        }
        
        return esValido;
    }

    // Botón cancelar
    btnCancelar.addEventListener('click', function() {
        const tieneContenido = Array.from(formulario.elements).some(element => 
            element.value && element.value.trim() !== ''
        );
        
        if (tieneContenido) {
            if (confirm('¿Está seguro que desea cancelar? Se perderán todos los datos ingresados.')) {
                limpiarFormulario();
                mostrarMensaje('Operación cancelada', 'info');
            }
        } else {
            limpiarFormulario();
        }
    });

    // Limpiar formulario
    function limpiarFormulario() {
        formulario.reset();
        contenedorEjemplares.innerHTML = '';
        tipoMaterialSelect.className = 'form-select tipo-material-select';
        cantEjemplaresSelect.value = '1';
        
        // Limpiar clases de validación
        formulario.querySelectorAll('.is-valid, .is-invalid').forEach(elemento => {
            elemento.classList.remove('is-valid', 'is-invalid');
        });
    }

    // Aplicar validación en tiempo real
    function aplicarValidacionCampos() {
        const campos = formulario.querySelectorAll('input, select');
        
        campos.forEach(campo => {
            // Validación al perder el foco
            campo.addEventListener('blur', function() {
                if (this.hasAttribute('required')) {
                    if (this.value.trim() === '') {
                        marcarCampoInvalido(this);
                    } else {
                        marcarCampoValido(this);
                    }
                }
            });
            
            // Validación mientras escribe
            campo.addEventListener('input', function() {
                if (this.hasAttribute('required') && this.value.trim() !== '') {
                    marcarCampoValido(this);
                }
            });
            
            // Validación para selects
            campo.addEventListener('change', function() {
                if (this.hasAttribute('required')) {
                    if (this.value === '') {
                        marcarCampoInvalido(this);
                    } else {
                        marcarCampoValido(this);
                    }
                }
            });
        });
    }

    // Marcar campo como inválido
    function marcarCampoInvalido(campo) {
        campo.classList.remove('is-valid');
        campo.classList.add('is-invalid');
    }

    // Marcar campo como válido
    function marcarCampoValido(campo) {
        campo.classList.remove('is-invalid');
        campo.classList.add('is-valid');
    }

    // Mostrar mensajes
    function mostrarMensaje(mensaje, tipo = 'info') {
        // Crear toast o usar tu sistema de notificaciones preferido
        const toast = document.createElement('div');
        toast.className = `alert alert-${tipo === 'success' ? 'success' : tipo === 'error' ? 'danger' : 'info'} alert-dismissible fade show position-fixed`;
        toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        toast.innerHTML = `
            ${mensaje}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(toast);
        
        // Auto-eliminar después de 5 segundos
        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, 5000);
    }

    // Aplicar validación inicial
    aplicarValidacionCampos();

    // Efecto visual para el botón manual
    document.querySelector('.btn-manual').addEventListener('click', function() {
        // Aquí puedes abrir un modal de ayuda o redirigir a documentación
        mostrarMensaje('Función de manual en desarrollo', 'info');
    });

    console.log('Todas las funcionalidades inicializadas correctamente');
});