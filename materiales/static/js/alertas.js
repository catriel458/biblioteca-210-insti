// Variables globales para almacenar callbacks
let callbackConfirmar = null;
let callbackCancelar = null;
let callbackConfirmarReducir = null;
let callbackCancelarReducir = null;

// Función principal que se llama al hacer clic en CANCELAR
function cancelarFormulario() {
    console.log('Función cancelarFormulario ejecutada');
    // Pasar la función vaciarCamposFormulario como callback para confirmar
    mostrarModalAlerta(vaciarCamposFormulario);
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

// Función para vaciar los campos del formulario
function vaciarCamposFormulario() {
    // Detectar qué formulario está activo
    const formularioNotebook = document.getElementById('alta-notebook-form');
    const formAltaMaterial = document.getElementById('form_alta_material');
    const formAltaMultimedia = document.getElementById('form_alta_multimedia');
    
    if (formularioNotebook) {
        console.log('Vaciando campos del formulario notebook...');
        
        // Restablecer la cantidad de ejemplares a 1
        const cantEjemplares = document.getElementById('cant_ejemplares');
        if (cantEjemplares) {
            cantEjemplares.value = '1';
        }

        // Restablecer el select de sede
        const sede = document.getElementById('sede');
        if (sede) {
            sede.selectedIndex = 0;
        }

        // Usar la función updateRowsMaterial para generar correctamente los ejemplares
        if (window.updateRowsMaterial) {
            window.updateRowsMaterial('notebook');
        } else {
            console.error('Error: La función updateRowsMaterial no está disponible');
            
            // Fallback: Limpiar los campos de los ejemplares manualmente
            const contenedorEjemplares = document.getElementById('contenedor-ejemplares-notebook');
            if (contenedorEjemplares) {
                contenedorEjemplares.innerHTML = '';
                // Generar un solo ejemplar vacío usando la plantilla manual
                let html = `
                    <div class="row mb-3">
                        <div class="col-md-3">
                            <label for="num_registro_1" style="font-size: 14px;">N° de registro<span class="text-danger">*</span>:</label>
                            <input type="text" class="form-control form-control-sm" id="num_registro_1" name="num_registro_1" required>
                        </div>
                        <div class="col-md-3">
                            <label for="modelo_1" style="font-size: 14px;">Modelo:</label>
                            <input type="text" class="form-control form-control-sm" id="modelo_1" name="modelo_1">
                        </div>
                    </div>`;
                contenedorEjemplares.innerHTML = html;
            }
        }

        console.log('✅ Campos del formulario notebook vaciados correctamente');
    } else if (formAltaMaterial) {
        // Verificar si es el formulario de mapas
        const tipoMaterial = document.getElementById('tipo_material');
        if (tipoMaterial && tipoMaterial.value === 'mapa') {
            console.log('Vaciando campos del formulario mapa...');
            
            // Restablecer el select de sede
            const sedeMapa = document.getElementById('sede-mapa');
            if (sedeMapa) {
                sedeMapa.selectedIndex = 0;
            }

            // Restablecer el select de tipo de mapa
            const tipoMapa = document.getElementById('input-nuevo-tipo-mapa');
            if (tipoMapa) {
                tipoMapa.selectedIndex = 0;
            }

            // Restablecer la cantidad a 1
            const cantMapa = document.getElementById('input-nueva-cant-mapa');
            if (cantMapa) {
                cantMapa.value = '1';
            }

            // Limpiar los grupos de tipos
            if (window.gruposTiposMapa) {
                window.gruposTiposMapa = [];
            }

            // Limpiar el campo oculto de gruposTiposMapa
            const gruposTiposMapaInput = document.getElementById('gruposTiposMapa');
            if (gruposTiposMapaInput) {
                gruposTiposMapaInput.value = '';
            }

            // Limpiar el contenedor de ejemplares
            const contenedorEjemplares = document.getElementById('contenedor-ejemplares-mapa');
            if (contenedorEjemplares) {
                contenedorEjemplares.innerHTML = '';
            }

            // Limpiar el bloque de tipo y cantidad
            const bloqueTipoCantidad = document.getElementById('bloque-tipo-cantidad');
            if (bloqueTipoCantidad) {
                bloqueTipoCantidad.innerHTML = '';
            }

            // Regenerar el botón + llamando a la función de renderizado
            if (window.renderizarTiposMapa) {
                window.renderizarTiposMapa();
            }

            console.log('✅ Campos del formulario mapa vaciados correctamente');
        }
    } else if (formAltaMultimedia) {
        console.log('Vaciando campos del formulario multimedia...');
        
        // Limpiar campos básicos del formulario multimedia
        const profesor = document.getElementById('profesor');
        if (profesor) {
            profesor.value = '';
        }

        const carrera = document.getElementById('carrera');
        if (carrera) {
            carrera.selectedIndex = 0;
        }

        const materia = document.getElementById('materia');
        if (materia) {
            materia.innerHTML = '<option value="">Primero seleccione una carrera</option>';
            materia.disabled = true;
        }

        const ingresarEnlace = document.getElementById('ingresar_enlace');
        if (ingresarEnlace) {
            ingresarEnlace.value = '';
        }

        const tituloContenido = document.getElementById('titulo_contenido');
        if (tituloContenido) {
            tituloContenido.value = '';
        }

        // Limpiar los grupos de multimedia
        if (window.gruposTiposMultimedia) {
            window.gruposTiposMultimedia = [];
        }

        // Limpiar el campo oculto de gruposMultimedia
        const gruposMultimediaInput = document.getElementById('gruposMultimedia');
        if (gruposMultimediaInput) {
            gruposMultimediaInput.value = '';
        }

        // Limpiar el contenedor de tipos multimedia
        const contenedorTiposMultimedia = document.getElementById('contenedor-tipos-multimedia');
        if (contenedorTiposMultimedia) {
            contenedorTiposMultimedia.innerHTML = '';
        }

        // Limpiar el contenedor de ejemplares multimedia
        const contenedorEjemplaresMultimedia = document.getElementById('contenedor-ejemplares-multimedia');
        if (contenedorEjemplaresMultimedia) {
            contenedorEjemplaresMultimedia.innerHTML = '';
        }

        console.log('✅ Campos del formulario multimedia vaciados correctamente');
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