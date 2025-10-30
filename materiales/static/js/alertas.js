// Función para validar si un archivo es una imagen válida
function esImagenValida(nombreArchivo) {
    if (!nombreArchivo) return false;
    const extension = nombreArchivo.toLowerCase();
    return extension.endsWith('.jpg') || extension.endsWith('.jpeg') || 
           extension.endsWith('.png') || extension.endsWith('.gif');
}

// Función para mostrar el modal de imagen de libro no válida
function mostrarModalImagenLibroNoValido(onAccept = null) {
    // Guardar callback
    callbackAceptarImagenLibroNoValido = onAccept;
    
    const modalImagenNoValida = document.getElementById('modal-imagenlibro-novalido');
    const backdrop = document.getElementById('modal-backdrop');
    
    if (modalImagenNoValida && backdrop) {
        modalImagenNoValida.style.display = 'block';
        modalImagenNoValida.classList.add('show');
        backdrop.style.display = 'block';
        backdrop.classList.add('show');
        document.body.style.overflow = 'hidden'; // Prevenir scroll
        console.log('Modal imagen libro no válida mostrado correctamente');
    } else {
        console.error('Error: No se encontraron los elementos del modal imagen libro no válida');
    }
}

// Función para ocultar el modal de imagen de libro no válida
function ocultarModalImagenLibroNoValido() {
    const modalImagenNoValida = document.getElementById('modal-imagenlibro-novalido');
    const backdrop = document.getElementById('modal-backdrop');
    
    if (modalImagenNoValida && backdrop) {
        modalImagenNoValida.style.display = 'none';
        modalImagenNoValida.classList.remove('show');
        backdrop.style.display = 'none';
        backdrop.classList.remove('show');
        document.body.style.overflow = ''; // Restaurar scroll
    }
}

// Función para cerrar el modal de imagen de libro no válida
function cerrarModalImagenLibroNoValido() {
    if (callbackAceptarImagenLibroNoValido) {
        callbackAceptarImagenLibroNoValido();
        callbackAceptarImagenLibroNoValido = null;
    }
    ocultarModalImagenLibroNoValido();
}// Variables globales para almacenar callbacks
let callbackConfirmar = null;
let callbackCancelar = null;
let callbackConfirmarReducir = null;
let callbackCancelarReducir = null;
let callbackConfirmarCSV = null;
let callbackCancelarCSV = null;
let callbackAceptarArchivoNoValido = null;
let callbackAceptarImagenLibroNoValido = null;

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
    } else if (tipo === 'csv') {
        if (callbackCancelarCSV) {
            callbackCancelarCSV();
            callbackCancelarCSV = null;
        }
        ocultarModalCSV();
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
    } else if (tipo === 'csv') {
        if (callbackConfirmarCSV) {
            callbackConfirmarCSV();
            callbackConfirmarCSV = null;
        }
        ocultarModalCSV();
    } else {
        // Limpiar directamente el campo URL del formulario de programa
        const urlInput = document.querySelector('#url');
        if (urlInput) {
            urlInput.value = '';
            console.log('Campo URL limpiado directamente desde confirmarModal');
        }
        
        // Limpiar SOLO el formulario de programa, no todos los formularios
        const programaForm = document.getElementById('form_alta_programa') || 
                            document.querySelector('form[data-form-type="programa"]');
        
        if (programaForm) {
            // Guardar el tipo de material actual para no perderlo
            const tipoMaterial = document.getElementById('tipo_material');
            const tipoMaterialValue = tipoMaterial ? tipoMaterial.value : null;
            
            // Limpiar campos individualmente en lugar de usar reset()
            const inputs = programaForm.querySelectorAll('input:not([type="hidden"]), select:not(#tipo_material)');
            inputs.forEach(input => {
                if (input.type === 'checkbox' || input.type === 'radio') {
                    input.checked = false;
                } else {
                    input.value = '';
                }
            });
            
            // Restaurar el tipo de material si es necesario
            if (tipoMaterial && tipoMaterialValue) {
                tipoMaterial.value = tipoMaterialValue;
            }
            
            console.log('Formulario de programa limpiado individualmente');
        }
        
        // Ejecutar el callback original si existe
        if (callbackConfirmar) {
            callbackConfirmar();
            callbackConfirmar = null;
        }
        
        // Asegurar que el campo URL esté vacío después de todo
        setTimeout(() => {
            const urlInputAfter = document.querySelector('#url');
            if (urlInputAfter && urlInputAfter.value !== '') {
                urlInputAfter.value = '';
                console.log('Campo URL limpiado con delay');
            }
        }, 100);
        
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
        // Eliminar cualquier clase que pueda estar interfiriendo
        modalAlerta.className = 'tarjeta-alerta';
        // Aplicar estilos directamente con !important para forzar el color rosa
        modalAlerta.setAttribute('style', 'display: flex !important; background-color: #FFB3BA !important; background: #FFB3BA !important; border: 2px solid #FF0000 !important;');
        
        backdrop.classList.add('show');
        backdrop.style.display = 'block';
        document.body.style.overflow = 'hidden'; // Prevenir scroll
        console.log('Modal vaciar campos mostrado correctamente con fondo rosa forzado');
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
        // Eliminar cualquier clase que pueda estar interfiriendo
        modalReducir.className = 'tarjeta-alerta';
        // Aplicar estilos directamente con !important para forzar el color rosa
        modalReducir.setAttribute('style', 'display: flex !important; background-color: #FFB3BA !important; background: #FFB3BA !important; border: 2px solid #FF0000 !important;');
        
        backdrop.style.display = 'block';
        document.body.style.overflow = 'hidden'; // Prevenir scroll
        console.log('Modal reducir ejemplares mostrado correctamente con fondo rosa forzado');
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

// Función para validar si un archivo es CSV o Excel
function esArchivoCSV(nombreArchivo) {
    if (!nombreArchivo) return false;
    const extension = nombreArchivo.toLowerCase();
    return extension.endsWith('.csv') || extension.endsWith('.xls') || extension.endsWith('.xlsx');
}

// Función para mostrar el modal de confirmación CSV
function mostrarModalCSV(nombreArchivo, onConfirm = null, onCancel = null) {
    // Validar que el archivo sea CSV
    if (!esArchivoCSV(nombreArchivo)) {
        // Si no es CSV, mostrar el modal de archivo no válido
        mostrarModalArchivoNoValido();
        // Ejecutar el callback de cancelar si existe
        if (onCancel) {
            onCancel();
        }
        return false;
    }
    
    // Guardar callbacks
    callbackConfirmarCSV = onConfirm;
    callbackCancelarCSV = onCancel;
    
    const modalCSV = document.getElementById('modal-confirmacion-csv');
    const backdrop = document.getElementById('modal-backdrop');
    const nombreArchivoElement = document.getElementById('nombre-archivo-csv');
    
    if (modalCSV && backdrop) {
        // Actualizar el nombre del archivo en el modal
        if (nombreArchivoElement && nombreArchivo) {
            nombreArchivoElement.textContent = nombreArchivo;
        }
        
        modalCSV.style.display = 'flex';
        backdrop.style.display = 'block';
        document.body.style.overflow = 'hidden'; // Prevenir scroll
        console.log('Modal confirmación CSV mostrado correctamente');
        return true;
    } else {
        console.error('Error: No se encontraron los elementos del modal confirmación CSV');
        return false;
    }
}

// Función para ocultar el modal de confirmación CSV
function ocultarModalCSV() {
    const modalCSV = document.getElementById('modal-confirmacion-csv');
    const backdrop = document.getElementById('modal-backdrop');
    
    if (modalCSV && backdrop) {
        modalCSV.style.display = 'none';
        backdrop.style.display = 'none';
        document.body.style.overflow = ''; // Restaurar scroll
    }
}

// Función para el botón CANCELAR del modal CSV
function cerrarModalCSV() {
    cerrarModal('csv');
}

// Función para el botón CONFIRMAR del modal CSV
function confirmarModalCSV() {
    confirmarModal('csv');
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
    
    // Para el caso de programa, tratamiento especial para el campo URL
    if (formulario_elegido === 'programa' || document.getElementById('form_alta_programa')) {
        console.log("Formulario programa detectado - limpiando URL directamente");
        const urlInput = document.querySelector('#url');
        if (urlInput) {
            urlInput.value = '';
            console.log("Campo URL limpiado directamente");
        }
    }
    
    // Para el caso de proyector, vamos a usar un enfoque directo
    if (formulario_elegido === 'proyector') {
        console.log("Formulario proyector seleccionado - usando método directo");
        borrarProyector();
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
            
            // Forzar la limpieza del campo URL con un enfoque alternativo
            setTimeout(() => {
                if (url.value !== '') {
                    url.value = '';
                    console.log('Campo URL limpiado con enfoque alternativo');
                }
            }, 50);
        } else {
            console.warn('Campo URL no encontrado');
            
            // Intentar encontrar el campo URL con un selector más amplio
            const urlAlt = document.querySelector('#url, [name="url"], input[type="url"]');
            if (urlAlt) {
                urlAlt.value = '';
                console.log('Campo URL encontrado con selector alternativo y limpiado');
            }
        }
        
        if (cicloLectivo) {
            cicloLectivo.value = '';
            console.log('Campo ciclo lectivo limpiado');
        }
        
        // Enfoque alternativo: usar reset() en el formulario y luego restaurar los valores que no queremos resetear
        form.reset();
        console.log('Formulario reseteado completamente');
        
        // Asegurar que el campo materia quede deshabilitado después del reset
        if (materia) {
            materia.disabled = true;
            materia.innerHTML = '<option value="">Primero seleccione una carrera</option>';
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
    
    // Guardar el valor actual del tipo de material antes de resetear
    const tipoMaterial = document.getElementById('tipo_material');
    const valorTipoMaterial = tipoMaterial ? tipoMaterial.value : 'proyector';
    
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
        
        // Restaurar el tipo de material a proyector
        if (tipoMaterial) {
            tipoMaterial.value = valorTipoMaterial;
            console.log('Tipo de material mantenido como "' + valorTipoMaterial + '"');
            
            // Asegurar que se muestre el formulario correcto
            if (window.mostrarFormulario) {
                window.mostrarFormulario(valorTipoMaterial);
            }
        }
        
        const inputs = form.querySelectorAll('input[type="text"], input[type="number"], input[type="email"], input[type="tel"], input[type="date"]');
        inputs.forEach(input => {
            input.value = '';
        });
        
        // Resetear selects a su valor por defecto (excepto tipo_material)
        const selects = form.querySelectorAll('select');
        selects.forEach(select => {
            if (select.id !== 'tipo_material') {
                select.selectedIndex = 0;
            }
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

// Función para mostrar el modal de archivo no válido
function mostrarModalArchivoNoValido(mensaje, onAceptar = null) {
    callbackAceptarArchivoNoValido = onAceptar;
    
    const modalArchivoNoValido = document.getElementById('modal-archivo-novalido');
    const backdrop = document.getElementById('modal-backdrop');
    const mensajeElement = document.getElementById('mensaje-archivo-novalido');
    
    if (modalArchivoNoValido && backdrop) {
        // Actualizar el mensaje en el modal si existe
        if (mensajeElement && mensaje) {
            mensajeElement.textContent = mensaje;
        }
        
        modalArchivoNoValido.style.display = 'flex';
        backdrop.style.display = 'block';
        document.body.style.overflow = 'hidden'; // Prevenir scroll
        console.log('Modal archivo no válido mostrado correctamente');
    } else {
        console.error('Error: No se encontraron los elementos del modal archivo no válido');
    }
}

// Función para cerrar el modal de archivo no válido
function cerrarModalArchivoNoValido() {
    const modalArchivoNoValido = document.getElementById('modal-archivo-novalido');
    const backdrop = document.getElementById('modal-backdrop');
    
    if (modalArchivoNoValido && backdrop) {
        modalArchivoNoValido.style.display = 'none';
        backdrop.style.display = 'none';
        document.body.style.overflow = ''; // Restaurar scroll
        
        // Ejecutar callback si existe
        if (callbackAceptarArchivoNoValido) {
            callbackAceptarArchivoNoValido();
            callbackAceptarArchivoNoValido = null;
        }
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
        borrarProyector();
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
    
    // FORZAR LIMPIEZA DEL CAMPO URL - PRIMERA PRIORIDAD
    try {
        // Intentar todos los métodos posibles para limpiar el campo URL
        const urlSelectors = ['#url', 'input[name="url"]', 'input[type="url"]'];
        urlSelectors.forEach(selector => {
            const urlElements = document.querySelectorAll(selector);
            urlElements.forEach(element => {
                element.value = '';
                console.log(`Campo URL limpiado usando selector: ${selector}`);
            });
        });
    } catch (e) {
        console.error('Error al limpiar URL:', e);
    }
    
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

        // FORZAR LIMPIEZA DEL CAMPO URL - SEGUNDA PRIORIDAD
        if (url) {
            url.value = '';
            console.log('Campo URL limpiado directamente desde borrarPrograma');
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
    
    // FORZAR LIMPIEZA DEL CAMPO URL - TERCERA PRIORIDAD (con delay)
    setTimeout(() => {
        try {
            const urlSelectors = ['#url', 'input[name="url"]', 'input[type="url"]'];
            urlSelectors.forEach(selector => {
                const urlElements = document.querySelectorAll(selector);
                urlElements.forEach(element => {
                    if (element.value !== '') {
                        element.value = '';
                        console.log(`Campo URL limpiado con delay usando selector: ${selector}`);
                    }
                });
            });
        } catch (e) {
            console.error('Error en limpieza con delay:', e);
        }
    }, 100);
    
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
    
    // Guardar el valor actual del tipo de material antes de resetear
    const tipoMaterial = document.getElementById('tipo_material');
    const valorTipoMaterial = tipoMaterial ? tipoMaterial.value : 'proyector';
    
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
        
        // Restaurar el tipo de material a proyector
        if (tipoMaterial) {
            tipoMaterial.value = valorTipoMaterial;
            console.log('Tipo de material mantenido como "' + valorTipoMaterial + '"');
            
            // Asegurar que se muestre el formulario correcto
            if (window.mostrarFormulario) {
                window.mostrarFormulario(valorTipoMaterial);
            }
        }
        
        const inputs = form.querySelectorAll('input[type="text"], input[type="number"], input[type="email"], input[type="tel"], input[type="date"]');
        inputs.forEach(input => {
            input.value = '';
        });
        
        // Resetear selects a su valor por defecto (excepto tipo_material)
        const selects = form.querySelectorAll('select');
        selects.forEach(select => {
            if (select.id !== 'tipo_material') {
                select.selectedIndex = 0;
            }
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