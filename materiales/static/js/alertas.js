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
    let formulario_elegido= $('#tipo_material').val();
    switch (formulario_elegido) {
        case 'proyector':
            console.log("Formulario 1 seleccionado");
            borrarProyector();
            break;
        case 'notebook':
            console.log("Formulario 2 seleccionado");
            borrarNotebook();
            break;
        case 'multimedia':
            console.log("Formulario 3 seleccionado");
            borrarMultimedia();
            break;
        case 'varios':
            console.log("Formulario 4 seleccionado");
            borrarVarios();
            break;
        case 'mapa':
            console.log("Formulario 4 seleccionado");
            break;
        default:
            console.log("Formulario no reconocido");
            break;
    } 
}

function borrarVarios() {
    console.log('Limpiando campos del formulario varios...');
    
    // Restablecer sede a valor inicial
    const sede = document.getElementById('sede-varios');
    if (sede) {
        sede.selectedIndex = 0;
    }

    // Limpiar tipo a registrar
    const tipoVarios = document.getElementById('tipo-varios');
    if (tipoVarios) {
        tipoVarios.value = '';
    }

    // Restablecer cantidad de ejemplares a 1
    const cantEjemplares = document.getElementById('cant_ejemplares');
    if (cantEjemplares) {
        cantEjemplares.value = '1';
    }

    // Limpiar los grupos de tipos
    if (window.gruposTiposVariosNuevo) {
        window.gruposTiposVariosNuevo = [];
    }

    // Limpiar el campo oculto que serializa los datos dinámicos
    const gruposTiposInput = document.getElementById('gruposTiposVariosNuevo');
    if (gruposTiposInput) {
        gruposTiposInput.value = '';
    }

    // Limpiar contenedor de tipos dinámicos
    const contenedorTiposDinamicos = document.getElementById('contenedor-tipos-varios-dinamicos');
    if (contenedorTiposDinamicos) {
        contenedorTiposDinamicos.innerHTML = '';
    }

    // Limpiar contenedor de tipos agregados
    const contenedorTiposNuevo = document.getElementById('contenedor-tipos-varios-nuevo');
    if (contenedorTiposNuevo) {
        contenedorTiposNuevo.innerHTML = '';
    }

    // Limpiar contenedor de ejemplares
    const contenedorEjemplares = document.getElementById('contenedor-ejemplares-varios');
    if (contenedorEjemplares) {
        contenedorEjemplares.innerHTML = '';
    }

    // Re-renderizar los tipos si existe la función
    if (window.renderizarTiposVariosNuevo) {
        window.renderizarTiposVariosNuevo();
    }

    console.log('✅ Campos del formulario varios vaciados correctamente');
    
    // Cerrar el modal de alerta si está abierto
    ocultarModalAlerta();
}

function borrarNotebook(){
             
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
}

function borrarProyector() {
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

function borrarMultimedia() {
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