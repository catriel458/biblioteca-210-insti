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

// Función para vaciar los campos del formulario
function vaciarCamposFormulario() {
    const form = document.querySelector('form');
    if (form) {
        form.reset();
        console.log('Formulario vaciado correctamente');
    }
}

// Función para mostrar el modal de alerta de vaciar campos
function mostrarModalAlerta(onConfirm = null, onCancel = null) {
    // Si no se proporciona un callback de confirmación, usar vaciarCamposFormulario por defecto
    callbackConfirmar = onConfirm || vaciarCamposFormulario;
    callbackCancelar = onCancel;
    
    const modalAlerta = document.getElementById('modal-vaciar-campos');
    const backdrop = document.getElementById('modal-backdrop');
    
    if (modalAlerta && backdrop) {
        modalAlerta.classList.add('show');
        modalAlerta.style.display = 'block';
        backdrop.classList.add('show');
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
    console.log("Vaciando campos del formulario tipo: " + formulario_elegido);
    
    // Para el caso de proyector, vamos a usar un enfoque directo
    if (formulario_elegido === 'proyector') {
        console.log("Formulario proyector seleccionado - usando método directo");
        // Resetear todos los inputs visibles en el formulario actual
        $('input:visible').not('[type="button"], [type="submit"]').val('');
        $('select:visible').prop('selectedIndex', 0);
        $('textarea:visible').val('');
        
        // Mantener el tipo de material como proyector
        $('#tipo_material').val('proyector');
        
        // Resetear a valores por defecto específicos
        $('#cant_ejemplares').val('1');
        
        console.log('✅ Campos del formulario proyector vaciados correctamente');
        return;
    }
    
    // Para los demás tipos de materiales, seguir con el switch original
    switch (formulario_elegido) {
        case 'notebook':
            console.log("Formulario notebook seleccionado");
            borrarNotebook();
            break;
        case 'multimedia':
            console.log("Formulario multimedia seleccionado");
            borrarMultimedia();
            break;
        case 'varios':
            console.log("Formulario varios seleccionado");
            borrarVarios();
            break;
        case 'mapa':
            console.log("Formulario mapa seleccionado");
            borrarMapa();
            break;
        case 'programa':
            console.log("Formulario programa seleccionado");
            borrarPrograma();
            break;    
        case 'libro':
            console.log("Formulario libro seleccionado");
            borrarLibro();
            break;  
        default:
            console.log("Formulario no reconocido");
            break;
    } 
}

function borrarMapa(){
    console.log('Limpiando campos del formulario mapa...');
    
    // Limpiar sede
    const sedeMapa = document.getElementById('sede-mapa');
    if (sedeMapa) {
        sedeMapa.value = '';
        console.log('Campo sede limpiado');
    }

    // Limpiar tipo de mapa
    const tipoMapa = document.getElementById('input-nuevo-tipo-mapa');
    if (tipoMapa) {
        tipoMapa.value = '';
        console.log('Campo tipo de mapa limpiado');
    }

    // Resetear cantidad a 1
    const cantidadMapa = document.getElementById('input-nueva-cant-mapa');
    if (cantidadMapa) {
        cantidadMapa.value = '1';
        console.log('Cantidad reseteada a 1');
    }

    // Limpiar array de grupos de tipos
    if (window.gruposTiposMapa) {
        window.gruposTiposMapa = [];
        console.log('Array gruposTiposMapa vaciado');
        
        // Limpiar el input oculto
        const gruposTiposMapaInput = document.getElementById('gruposTiposMapa');
        if (gruposTiposMapaInput) {
            gruposTiposMapaInput.value = '';
        }
    }

    // Limpiar el contenedor de ejemplares
    const contenedorEjemplares = document.getElementById('contenedor-ejemplares-mapa');
    if (contenedorEjemplares) {
        contenedorEjemplares.innerHTML = '';
        console.log('Contenedor de ejemplares limpiado');
    }

    // Limpiar el bloque de tipo y cantidad
    const bloqueTipoCantidad = document.getElementById('bloque-tipo-cantidad');
    if (bloqueTipoCantidad) {
        bloqueTipoCantidad.innerHTML = '';
        console.log('Bloque de tipo y cantidad limpiado');
    }

    // Re-renderizar los tipos si existe la función
    if (window.renderizarTiposMapa) {
        window.renderizarTiposMapa();
        console.log('Tipos re-renderizados');
    }

    console.log('✅ Campos del formulario mapa vaciados correctamente');
    
    // Cerrar el modal de alerta
    ocultarModalAlerta();
}

function borrarPrograma(){
    console.log('Limpiando campos del formulario programa...');
    
    // Intentar encontrar el formulario por ID o por atributos
    let form = document.getElementById('form_alta_programa') || 
               document.getElementById('form_alta_material') || 
               document.querySelector('form[data-form-type="programa"]');

    if (form) {
        console.log('Formulario encontrado, limpiando campos...');
        
        // Limpiar campos individualmente para asegurar que los eventos se disparen
        const profesor = form.querySelector('#profesor, [name="profesor"]');
        const carrera = form.querySelector('#carrera, [name="carrera"]');
        const materia = form.querySelector('#materia, [name="materia"]');
        const url = form.querySelector('#url, [name="url"]');
        const cicloLectivo = form.querySelector('#ciclo_lectivo, [name="ciclo_lectivo"]');

        if (profesor) {
            profesor.value = '';
            console.log('Campo profesor limpiado');
        }
        
        // Limpiar carrera y disparar evento change
        if (carrera) {
            carrera.value = '';
            // Crear y disparar evento change
            const event = new Event('change', { bubbles: true });
            carrera.dispatchEvent(event);
            console.log('Campo carrera limpiado y evento disparado');
        }

        // El evento change de carrera ya se encargará de limpiar y deshabilitar materia
        if (materia) {
            materia.innerHTML = '<option value="">Primero seleccione una carrera</option>';
            materia.disabled = true;
            console.log('Campo materia reseteado');
        }

        if (url) {
            url.value = '';
            console.log('Campo URL limpiado');
        }
        
        if (cicloLectivo) {
            cicloLectivo.value = '';
            console.log('Campo ciclo lectivo limpiado');
        }
        
        console.log('✅ Campos del formulario programa vaciados correctamente');
    } else {
        console.error('❌ No se encontró el formulario de programa');
        console.log('Elementos disponibles:', 
            document.querySelectorAll('form').length, 
            'formularios en la página');
    }
    
    // Cerrar el modal de alerta
    ocultarModalAlerta();
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
    console.log('Limpiando campos del formulario proyector...');
    
    // Intentar encontrar el formulario - usar document.forms para mayor compatibilidad
    const forms = document.forms;
    let form = null;
    
    // Buscar el formulario por su ID o por atributos
    for (let i = 0; i < forms.length; i++) {
        if (forms[i].id === 'alta-proyector-form' || 
            (forms[i].querySelector('[data-form-type="proyector"]'))) {
            form = forms[i];
            break;
        }
    }
    
    if (form) {
        console.log('Formulario de proyector encontrado');
        // Resetear el formulario completo primero
        form.reset();
        
        // Mantener seleccionado "proyector" en el select tipo_material
        const tipoMaterial = document.getElementById('tipo_material');
        if (tipoMaterial) {
            tipoMaterial.value = 'proyector';
            console.log('Tipo de material mantenido como "proyector"');
        }
        const inputs = form.querySelectorAll('input[type="text"], input[type="number"], input[type="email"], input[type="tel"], input[type="date"]');
        inputs.forEach(input => {
            input.value = '';
        });
        
        // Resetear selects a su valor por defecto
        const selects = form.querySelectorAll('select');
        selects.forEach(select => {
            select.selectedIndex = 0;
        });
        
        // Limpiar textareas
        const textareas = form.querySelectorAll('textarea');
        textareas.forEach(textarea => {
            textarea.value = '';
        });
        
        // Desmarcar checkboxes y radio buttons
        const checkboxesRadios = form.querySelectorAll('input[type="checkbox"], input[type="radio"]');
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
    
    // No cerramos el modal aquí, ya que confirmarModal() se encargará de cerrarlo
    // ocultarModalAlerta();
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

function borrarLibro() {
    console.log('Limpiando campos del formulario libro...');
    
    // Intentar encontrar el formulario
    const form = document.getElementById('form_alta_material');
    
    if (form) {
        // Resetear el formulario completo primero
        form.reset();
        
        // Mantener seleccionado "libro" en el select tipo_material
        const tipoMaterial = document.getElementById('tipo_material');
        if (tipoMaterial) {
            tipoMaterial.value = 'libro';
            console.log('Tipo de material mantenido como "libro"');
        }
        
        // Limpiar campos principales
        const titulo = form.querySelector('[name="titulo"]');
        if (titulo) {
            titulo.value = '';
        }
        
        const autor = form.querySelector('[name="autor"]');
        if (autor) {
            autor.value = '';
        }
        
        const editorial = form.querySelector('[name="editorial"]');
        if (editorial) {
            editorial.value = '';
        }
        
        const descripcion = form.querySelector('[name="descripcion"]');
        if (descripcion) {
            descripcion.value = '';
        }
        
        const siglasAutorTitulo = form.querySelector('[name="siglas_autor_titulo"]');
        if (siglasAutorTitulo) {
            siglasAutorTitulo.value = '';
        }
        
        const clasificacionCdu = form.querySelector('[name="clasificacion_cdu"]');
        if (clasificacionCdu) {
            clasificacionCdu.value = '';
        }
        
        const etiquetaPalabraClave = form.querySelector('[name="etiqueta_palabra_clave"]');
        if (etiquetaPalabraClave) {
            etiquetaPalabraClave.value = '';
        }
        
        // Restablecer cantidad de ejemplares a 1
        const cantEjemplares = document.getElementById('cant_ejemplares');
        if (cantEjemplares) {
            cantEjemplares.value = '1';
            
            // Disparar evento change para actualizar los ejemplares
            const event = new Event('change', { bubbles: true });
            cantEjemplares.dispatchEvent(event);
        }
        
        // Limpiar el contenedor de ejemplares
        const contenedorEjemplares = document.getElementById('contenedor-ejemplares-libro');
        if (contenedorEjemplares) {
            // Mantener solo un ejemplar vacío
            const ejemplaresActuales = contenedorEjemplares.querySelectorAll('.row.mb-3');
            if (ejemplaresActuales.length > 1) {
                // Conservar solo el primer ejemplar
                const primerEjemplar = ejemplaresActuales[0];
                contenedorEjemplares.innerHTML = '';
                contenedorEjemplares.appendChild(primerEjemplar);
                
                // Limpiar los campos del primer ejemplar
                const inputs = primerEjemplar.querySelectorAll('input, select, textarea');
                inputs.forEach(input => {
                    if (input.type !== 'hidden') {
                        input.value = '';
                    }
                });
            }
        }
        
        // Si existe la función updateRowsMaterial, usarla para regenerar los ejemplares
        if (window.updateRowsMaterial) {
            window.updateRowsMaterial('libro');
        }
        
        console.log('✅ Campos del formulario libro vaciados correctamente');
    } else {
        console.error('❌ No se encontró el formulario de libro');
    }
    
    // Cerrar el modal de alerta
    ocultarModalAlerta();
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