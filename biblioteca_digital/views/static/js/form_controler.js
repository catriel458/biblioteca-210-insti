// Lógica principal para formularios dinámicos de materiales
// Autor: Juni & Cascade
// Última actualización: 2025-05-15

// Lógica AJAX y helpers exclusivos para alta_material.html
// No contiene lógica de TiposEjemplares ni gestión de tipos/ejemplares dedicados (ver form_altas.js para eso)
document.addEventListener("DOMContentLoaded", function () {
    // --- Mostrar/ocultar campos exclusivos de libro ---
    function toggleCamposLibro() {
        const tipoMaterial = document.getElementById('tipo_material');
        const tipo = tipoMaterial ? tipoMaterial.value : null;
        const camposLibro = document.querySelectorAll('.campos-libro');
        camposLibro.forEach(el => {
            el.style.display = (tipo === 'libro') ? 'flex' : 'none';
        });
    }

    // Elementos clave del DOM
    // Este script debe ser cargado únicamente en alta_material.html
    const tipoMaterialSelect = document.getElementById('tipo_material');
    const formContainer = document.getElementById('formulario-especifico');
    const cantEjemplaresInput = document.getElementById('cant_ejemplares');
    const cantEjemplaresContainer = document.getElementById('cant_ejemplares_container');

    // --- Cargar el formulario parcial correspondiente al material seleccionado (AJAX) ---
    async function loadMaterialTemplate(tipo) {
        if (!tipo) {
            if (formContainer) formContainer.innerHTML = '';
            if (cantEjemplaresContainer) cantEjemplaresContainer.style.display = 'none';
            return;
        }
        try {
            const tipoLower = tipo.toLowerCase();
            const response = await fetch(`/libros/get_material_template/${tipoLower}/`);
            if (response.ok) {
                const html = await response.text();
                // --- PARSEAR Y EXTRAER SOLO EL FRAGMENTO DEL FORMULARIO ---
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                // Ajusta el selector según el tipo recibido (libro, mapa, varios, etc.)
                // Busca tanto el atributo data-form como data-form-type para compatibilidad
                const fragmento = doc.querySelector(`[data-form-type="${tipoLower}"], [data-form="${tipoLower}"]`);
                if (fragmento) {
                    formContainer.innerHTML = '';
                    formContainer.appendChild(fragmento.cloneNode(true));

                    // --- Inicialización automática de TiposEjemplares según el tipo ---
                    if (tipoLower === 'mapa' && typeof TiposEjemplares !== 'undefined') {
                        const mapaManager = TiposEjemplares.init({
                            tiposKey: 'tipos_mapa',
                            titulo: 'Tipos de Mapa',
                            opcionesSede: [
                                { value: 'sede1', texto: 'La Plata' },
                                { value: 'sede2', texto: 'Abasto' }
                            ]
                        });
                        mapaManager.generarHTML('contenedor-tipos-mapa');
                    }
                    if (tipoLower === 'varios' && typeof TiposEjemplares !== 'undefined') {
                        const variosManager = TiposEjemplares.init({
                            tiposKey: 'tipos_varios',
                            titulo: 'Tipos de Material',
                            opcionesSede: [
                                { value: 'sede1', texto: 'La Plata' },
                                { value: 'sede2', texto: 'Abasto' }
                            ]
                        });
                        variosManager.generarHTML('contenedor-tipos-varios');
                    }
                } else {
                    formContainer.innerHTML = '<div class="alert alert-danger">No se encontró el formulario esperado en la respuesta.</div>';
                }
                // Mostrar/ocultar campo de ejemplares solo para libro
                if (tipoLower === 'libro' && cantEjemplaresContainer) {
                    cantEjemplaresContainer.style.display = 'block';
                    if (typeof updateRows === 'function') updateRows();
                } else if (cantEjemplaresContainer) {
                    cantEjemplaresContainer.style.display = 'none';
                }
            } else {
                formContainer.innerHTML = '<div class="alert alert-danger">No se pudo cargar el formulario.</div>';
                if (cantEjemplaresContainer) cantEjemplaresContainer.style.display = 'none';
            }
        } catch (error) {
            formContainer.innerHTML = '<div class="alert alert-danger">Error de conexión.</div>';
            if (cantEjemplaresContainer) cantEjemplaresContainer.style.display = 'none';
        }
    }

    // Listener principal para el selector de materiales
    if (tipoMaterialSelect) {
        tipoMaterialSelect.addEventListener('change', function() {
            loadMaterialTemplate(this.value);
        });
    }

    // Inicializar al cargar la página
    // Si el selector no tiene valor, seleccionamos el primero disponible
    let tipoInicial = tipoMaterialSelect && tipoMaterialSelect.value;
    if (!tipoInicial && tipoMaterialSelect && tipoMaterialSelect.options.length > 0) {
        tipoInicial = tipoMaterialSelect.options[0].value;
    }
    if (tipoInicial) {
        loadMaterialTemplate(tipoInicial);
    }


    // Listener para mostrar/ocultar campos exclusivos de libro
    if (tipoMaterialSelect) {
        tipoMaterialSelect.addEventListener('change', toggleCamposLibro);
    }
    window.addEventListener('DOMContentLoaded', toggleCamposLibro);

    // --- El resto de la lógica (updateRows, carga de imágenes, etc.) permanece igual ---

    let valorAnterior = cantEjemplaresInput ? (parseInt(cantEjemplaresInput.value) || 1) : 1;


    // Genera dinámicamente los campos de ejemplares según la cantidad indicada
    window.updateRows = function() {
        // Referencias seguras a los elementos clave
        const cantEjemplaresInput = document.getElementById('cant_ejemplares');
        const ejemplaresContainer = document.getElementById('ejemplares-container');
        // Si no existe el input o el contenedor, no hacer nada
        if (!cantEjemplaresInput || !ejemplaresContainer) return;

        const cantEjemplares = parseInt(cantEjemplaresInput.value) || 1;

        // Limpiar el contenedor antes de agregar nuevas filas
        ejemplaresContainer.innerHTML = '';

        // Mostrar u ocultar el contenedor según la cantidad
        ejemplaresContainer.style.display = cantEjemplares >= 1 ? 'block' : 'none';

        if (cantEjemplares <= 0) return;

        // Generar las filas dinámicamente
        for (let i = 0; i < cantEjemplares; i++) {
            const row = document.createElement('div');
            row.className = 'row mt-3';
            row.innerHTML = `
                <div class="row">
                    <div class="col-2">
                        <label for="numero_ejemplar_${i}">Ejemplar N°:</label>
                        <input type="text" class="form-control" id="numero_ejemplar_${i}" name="numero_ejemplar[]" value="${i + 1}" required readonly style="background-color: transparent !important;">
                    </div>
                    <div class="col-2 d-flex flex-column justify-content-between">
                        <div>
                            <label for="sede_${i}">Sede:</label>
                            <select class="form-control mb-2" id="sede_${i}" name="sede[]" required>
                                <option value="">Aún sin seleccionar</option>
                                <option value="sede1">La Plata</option>
                                <option value="sede2">Abasto</option>
                            </select>
                        </div>
                        <div>
                            <label for="disponibilidad_${i}">Disponibilidad:</label>
                            <select class="form-control" id="disponibilidad_${i}" name="disponibilidad[]" required>
                                <option value="">Aún sin seleccionar</option>
                                <option value="disponible">Disponible</option>
                                <option value="no_disponible">No Disponible</option>
                            </select>
                        </div>
                    </div>
                    <div class="col-6">
                        <label for="observaciones_${i}">Observaciones:</label>
                        <textarea class="form-control h-100" id="observaciones_${i}" name="observaciones[]" rows="4" style="min-width:100%; max-width:100%; min-height:70px;" placeholder="Escriba aquí..."></textarea>
                    </div>
                </div>
            `;
            ejemplaresContainer.appendChild(row);
        }
    }

    function mostrarAlerta() {
        const overlay = document.createElement('div');
        overlay.style.position = 'fixed';
        overlay.style.top = '0';
        overlay.style.left = '0';
        overlay.style.width = '100%';
        overlay.style.height = '100%';
        overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
        overlay.style.zIndex = '9999';
        overlay.style.display = 'flex';
        overlay.style.justifyContent = 'center';
        overlay.style.alignItems = 'center';
    
        const modal = document.createElement('div');
        modal.style.width = '420px';
        modal.style.backgroundColor = '#ffd5d5';
        modal.style.borderRadius = '10px';
        modal.style.boxShadow = '0 4px 10px rgba(0,0,0,0.3)';
        modal.style.overflow = 'hidden';
        modal.style.fontFamily = 'sans-serif';
    
        const header = document.createElement('div');
        header.textContent = '¡ATENCIÓN!';
        header.style.backgroundColor = '#ff4d4d';
        header.style.color = 'white';
        header.style.textAlign = 'center';
        header.style.fontWeight = 'bold';
        header.style.padding = '12px';
        header.style.fontSize = '18px';
    
        const body = document.createElement('div');
        body.textContent = 'AL REDUCIR LA CANTIDAD DE EJEMPLARES, SE PERDERÁN LOS DATOS INTRODUCIDOS PARA LOS EJEMPLARES QUE SUPEREN LA CANTIDAD SELECCIONADA.';
        body.style.padding = '20px';
        body.style.textAlign = 'center';
        body.style.fontSize = '14px';
        body.style.color = '#333';
    
        const footer = document.createElement('div');
        footer.style.display = 'flex';
        footer.style.justifyContent = 'space-between';
        footer.style.padding = '10px 20px 20px 20px';
    
        const btnCancelar = document.createElement('button');
        btnCancelar.textContent = 'CANCELAR';
        btnCancelar.style.backgroundColor = '#4e6ef2';
        btnCancelar.style.color = 'white';
        btnCancelar.style.border = 'none';
        btnCancelar.style.padding = '10px 20px';
        btnCancelar.style.borderRadius = '6px';
        btnCancelar.style.cursor = 'pointer';
        btnCancelar.style.flex = '1';
        btnCancelar.style.marginRight = '10px';
        btnCancelar.style.fontWeight = 'bold';
    
        const btnConfirmar = document.createElement('button');
        btnConfirmar.textContent = 'CONFIRMAR';
        btnConfirmar.style.backgroundColor = '#d63333';
        btnConfirmar.style.color = 'white';
        btnConfirmar.style.border = 'none';
        btnConfirmar.style.padding = '10px 20px';
        btnConfirmar.style.borderRadius = '6px';
        btnConfirmar.style.cursor = 'pointer';
        btnConfirmar.style.flex = '1';
        btnConfirmar.style.fontWeight = 'bold';
    
        footer.appendChild(btnCancelar);
        footer.appendChild(btnConfirmar);
    
        modal.appendChild(header);
        modal.appendChild(body);
        modal.appendChild(footer);
        overlay.appendChild(modal);
        document.body.appendChild(overlay);
    
        return new Promise((resolve) => {
            if (btnConfirmar) {
                btnConfirmar.addEventListener('click', () => {
                    overlay.remove();
                    resolve(true);
                });
            }
            if (btnCancelar) {
                btnCancelar.addEventListener('click', () => {
                    overlay.remove();
                    resolve(false);
                });
            }
        });
    }
    

    async function manejarReduccionEjemplares(valorActual) {
        cantEjemplaresInput.value = valorAnterior;

        const confirmado = await mostrarAlerta();

        if (confirmado) {
            cantEjemplaresInput.value = valorActual;
            valorAnterior = valorActual;
            updateRows();
        } else {
            cantEjemplaresInput.value = valorAnterior;
        }
    }

    if (cantEjemplaresInput) {
        cantEjemplaresInput.addEventListener('change', async function () {
            const valorActual = parseInt(cantEjemplaresInput.value) || 1;
            if (valorActual < valorAnterior) {
                await manejarReduccionEjemplares(valorActual);
            } else if (valorActual > valorAnterior) {
                valorAnterior = valorActual;
                updateRows();
            }
        });
    }

    // Manejar cambios en el tipo de material

    if (tipoMaterialSelect) {
        tipoMaterialSelect.addEventListener('change', async function () {
            const tipo = tipoMaterialSelect.value;
            if (cantEjemplaresContainer) cantEjemplaresContainer.style.display = tipo ? 'block' : 'none';

            if (!tipo) {
                if (formContainer) formContainer.innerHTML = '';
                if (typeof ejemplaresContainer !== 'undefined' && ejemplaresContainer) {
                    ejemplaresContainer.innerHTML = '';
                    ejemplaresContainer.style.display = 'none';
                }
                if (typeof buttonsContainer !== 'undefined' && buttonsContainer) {
                    buttonsContainer.style.display = 'none';
                }
                return;
            }

            const templateContent = await loadMaterialTemplate(tipo);
            if (templateContent && formContainer) {
                formContainer.innerHTML = templateContent;
            }

            valorAnterior = cantEjemplaresInput ? (parseInt(cantEjemplaresInput.value) || 1) : 1;
            updateRows();
        });
    }

    // Limpiar todos los campos al enviar el formulario
    const form = document.getElementById('form_alta_material');
    if (form) {
        form.addEventListener('submit', function(e) {
            // Espera un poco para no interferir con el submit real (por si es AJAX o normal)
            setTimeout(function() {
                // Limpiar todos los inputs y textareas manualmente
                form.querySelectorAll('input[type="text"], input[type="number"], textarea').forEach(function(input) {
                    input.value = '';
                });
                // Limpiar selects
                form.querySelectorAll('select').forEach(function(select) {
                    select.selectedIndex = 0;
                });
            }, 100);
        });
    }
    if (tipoMaterialSelect.value) {
        updateRows();
    }

    // --- INICIO: Carga y previsualización de imagen en upload_box_container ---
    let imagenSeleccionada = null;
    // Obtener referencias solo una vez
    const uploadBox = document.getElementById('upload_box'); // Declaración agregada para evitar ReferenceError
    // arriba ya existe uploadSimple
    const fileInput = document.getElementById('file_upload_input');
    const urlInput = document.getElementById('url_upload_input');
    const simpleFileInput = document.getElementById('cargar_imagen');
    let imagenSimpleSeleccionada = null;

    if (fileInput && uploadBox) {
        let preview = document.getElementById('img_preview_upload_box');
        if (!preview) {
            preview = document.createElement('img');
            preview.id = 'img_preview_upload_box';
            preview.style.maxWidth = '100%';
            preview.style.marginTop = '10px';
            preview.style.display = 'none';
            if (uploadBox) {
            uploadBox.querySelector('.custom-upload-box').appendChild(preview);
        }
        }
        // Crear/obtener el mensaje de error
        let errorMsg = document.getElementById('img_error_msg');
        if (!errorMsg) {
            errorMsg = document.createElement('div');
            errorMsg.id = 'img_error_msg';
            errorMsg.style.color = 'red';
            errorMsg.style.fontSize = '0.9em';
            errorMsg.style.display = 'none';
            if (uploadBox) {
            uploadBox.querySelector('.custom-upload-box').appendChild(errorMsg);
        }
        }
        // Crear/obtener el botón de eliminar foto (como una X en la esquina superior izquierda)
        let deleteBtn = document.getElementById('img_delete_btn');
        if (!deleteBtn) {
            deleteBtn = document.createElement('button');
            deleteBtn.id = 'img_delete_btn';
            deleteBtn.type = 'button';
            deleteBtn.innerHTML = '&times;'; // X grande
            deleteBtn.setAttribute('aria-label', 'Eliminar foto');
            deleteBtn.style.position = 'absolute';
            deleteBtn.style.top = '6px';
            deleteBtn.style.left = '6px';
            deleteBtn.style.background = 'rgba(255,255,255,0.7)';
            deleteBtn.style.border = 'none';
            deleteBtn.style.color = '#c00';
            deleteBtn.style.fontWeight = 'bold';
            deleteBtn.style.fontSize = '1.5em';
            deleteBtn.style.cursor = 'pointer';
            deleteBtn.style.zIndex = '10';
            deleteBtn.style.display = 'none';
            // Crear un contenedor relativo para el preview y el botón
            let previewContainer = document.getElementById('img_preview_container');
            if (!previewContainer) {
                previewContainer = document.createElement('div');
                previewContainer.id = 'img_preview_container';
                previewContainer.style.position = 'relative';
                previewContainer.style.display = 'inline-block';
                previewContainer.style.width = '100%';
                // Mover el preview dentro del contenedor
                preview.parentNode.insertBefore(previewContainer, preview);
                previewContainer.appendChild(preview);
            }
            previewContainer.appendChild(deleteBtn);
            // Ocultar la X por defecto
            deleteBtn.style.display = 'none';
            // Mostrar la X al pasar el mouse por encima del contenedor
            previewContainer.addEventListener('mouseenter', function() {
                if (preview.style.display === 'block') {
                    deleteBtn.style.display = 'block';
                }
            });
            previewContainer.addEventListener('mouseleave', function() {
                deleteBtn.style.display = 'none';
            });
        }

        function limpiarImagen() {
            preview.src = '';
            preview.style.display = 'none';
            deleteBtn.style.display = 'none';
            errorMsg.style.display = 'none';
            if (fileInput) fileInput.value = '';
            if (urlInput) urlInput.value = '';
            imagenSeleccionada = null;
        }

        deleteBtn.onclick = limpiarImagen;

        function mostrarPreviewArchivo(file) {
            if (file && file.type.startsWith('image/')) {
                imagenSeleccionada = file;
                const reader = new FileReader();
                reader.onload = function (e) {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                    errorMsg.style.display = 'none';
                    // deleteBtn.style.display = 'block'; // Ya no mostrar siempre
                };
                reader.readAsDataURL(file);
            } else {
                limpiarImagen();
            }
        }

        function mostrarPreviewUrl(url) {
            if (url && (url.startsWith('http://') || url.startsWith('https://'))) {
                imagenSeleccionada = null;
                preview.src = url;
                preview.style.display = 'block';
                errorMsg.style.display = 'none';
                // deleteBtn.style.display = 'block'; // Ya no mostrar siempre
            } else if (!fileInput.value) {
                limpiarImagen();
            }
        }

        preview.onerror = function() {
            preview.style.display = 'none';
            errorMsg.textContent = 'No se pudo cargar la imagen. Verifica el enlace o la imagen.';
            errorMsg.style.display = 'block';
            // deleteBtn.style.display = 'block'; // Ya no mostrar siempre
        };
        preview.onload = function() {
            errorMsg.style.display = 'none';
        };

        fileInput.addEventListener('change', function (event) {
            if (urlInput && urlInput.value.trim() !== '') return;
            const file = event.target.files[0];
            mostrarPreviewArchivo(file);
        });

        if (urlInput) {
            urlInput.addEventListener('input', function (event) {
                const url = event.target.value.trim();
                if (url) {
                    mostrarPreviewUrl(url);
                } else {
                    if (fileInput.files && fileInput.files[0]) {
                        mostrarPreviewArchivo(fileInput.files[0]);
                    } else {
                        limpiarImagen();
                    }
                }
            });
            urlInput.addEventListener('keydown', function(event) {
                if (event.key === 'Enter') {
                    event.preventDefault();
                }
            });
        }
    }
    // --- FIN: Carga y previsualización de imagen en upload_box_container ---

    // --- INICIO: Carga y previsualización de imagen en upload_simple_container ---
    if (simpleFileInput && uploadSimple) {
        // Crear contenedor para preview, X y nombre de archivo
        let simplePreview = document.getElementById('img_simple_preview');
        let simpleDeleteBtn = document.getElementById('img_simple_delete_btn');
        let simplePreviewContainer = document.getElementById('img_simple_preview_container');
        let simpleFileName = document.getElementById('nombre_archivo_carga_simple');
        if (!simpleFileName) {
            // Ya existe en el HTML, solo lo limpiamos
            simpleFileName = document.createElement('div');
        }
        if (!simplePreviewContainer) {
            simplePreviewContainer = document.createElement('div');
            simplePreviewContainer.id = 'img_simple_preview_container';
            simplePreviewContainer.style.position = 'relative';
            simplePreviewContainer.style.display = 'inline-block';
            simplePreviewContainer.style.width = '100%';
            uploadSimple.querySelector('.upload-box').appendChild(simplePreviewContainer);
        }
        if (!simplePreview) {
            simplePreview = document.createElement('img');
            simplePreview.id = 'img_simple_preview';
            simplePreview.style.maxWidth = '100%';
            simplePreview.style.marginTop = '10px';
            simplePreview.style.display = 'none';
            simplePreviewContainer.appendChild(simplePreview);
        }
        if (!simpleFileName) {
            simpleFileName = document.createElement('div');
            simpleFileName.id = 'nombre_archivo_carga_simple';
            simpleFileName.style.textAlign = 'center';
            simpleFileName.style.fontSize = '0.92em';
            simpleFileName.style.color = '#444';
            simpleFileName.style.marginTop = '6px';
            simpleFileName.style.marginBottom = '2px';
            simpleFileName.style.wordBreak = 'break-all';
            simplePreviewContainer.appendChild(simpleFileName);
        }
        if (!simpleDeleteBtn) {
            simpleDeleteBtn = document.createElement('button');
            simpleDeleteBtn.id = 'img_simple_delete_btn';
            simpleDeleteBtn.type = 'button';
            simpleDeleteBtn.innerHTML = '&times;';
            simpleDeleteBtn.setAttribute('aria-label', 'Eliminar foto');
            simpleDeleteBtn.style.position = 'absolute';
            simpleDeleteBtn.style.top = '6px';
            simpleDeleteBtn.style.left = '6px';
            simpleDeleteBtn.style.background = 'rgba(255,255,255,0.7)';
            simpleDeleteBtn.style.border = 'none';
            simpleDeleteBtn.style.color = '#c00';
            simpleDeleteBtn.style.fontWeight = 'bold';
            simpleDeleteBtn.style.fontSize = '1.5em';
            simpleDeleteBtn.style.cursor = 'pointer';
            simpleDeleteBtn.style.zIndex = '10';
            simpleDeleteBtn.style.display = 'none';
            simplePreviewContainer.appendChild(simpleDeleteBtn);
        }
        // Mostrar la X solo cuando el mouse está sobre la imagen o la X
        simplePreviewContainer.addEventListener('mouseenter', function() {
            if (simplePreview.style.display === 'block') {
                simpleDeleteBtn.style.display = 'block';
            }
        });
        simplePreviewContainer.addEventListener('mouseleave', function() {
            simpleDeleteBtn.style.display = 'none';
        });
        function limpiarSimpleImagen() {
            simplePreview.src = '';
            simplePreview.style.display = 'none';
            simpleDeleteBtn.style.display = 'none';
            simpleFileName.textContent = '';
            if (simpleFileInput) simpleFileInput.value = '';
            imagenSimpleSeleccionada = null;
        }
        simpleDeleteBtn.onclick = limpiarSimpleImagen;
        simpleFileInput.addEventListener('change', function (event) {
            const file = event.target.files[0];
            if (file) {
                simpleFileName.textContent = file.name;
            } else {
                simpleFileName.textContent = '';
            }
            // No preview para CSV/Excel
            if (file && file.type.startsWith('image/')) {
                imagenSimpleSeleccionada = file;
                const reader = new FileReader();
                reader.onload = function (e) {
                    simplePreview.src = e.target.result;
                    simplePreview.style.display = 'block';
                };
                reader.readAsDataURL(file);
            } else {
                simplePreview.style.display = 'none';
                simplePreview.src = '';
            }
        });
    }
    // --- FIN: Carga y previsualización de imagen en upload_simple_container ---
});
