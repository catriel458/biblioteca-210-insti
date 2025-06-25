document.addEventListener('DOMContentLoaded', () => {
    const buscadorInput = document.querySelector('input[name="q"]');
    const tipoMaterialSelect = document.getElementById('tipo_material');
    const contenedorFormulario = document.getElementById('formulario-especifico');
    const sugerenciasContainer = document.createElement('div');
    sugerenciasContainer.classList.add('sugerencias-container');
    buscadorInput.parentNode.appendChild(sugerenciasContainer);

    let debounceTimeout;

    function debounce(func, delay) {
        return (...args) => {
            clearTimeout(debounceTimeout);
            debounceTimeout = setTimeout(() => func.apply(this, args), delay);
        };
    }

    function limpiarSugerencias() {
        sugerenciasContainer.innerHTML = '';
        sugerenciasContainer.style.display = 'none';
    }

    function mostrarSugerencias(items) {
        if (!items.length) {
            limpiarSugerencias();
            return;
        }
        sugerenciasContainer.innerHTML = '';
        items.forEach(item => {
            const div = document.createElement('div');
            div.classList.add('sugerencia-item');
            div.textContent = item.nombre; // asumiendo que backend envía campo 'nombre'
            div.dataset.id = item.id;
            div.addEventListener('click', () => {
                cargarFormulario(item.id);
                limpiarSugerencias();
                buscadorInput.value = item.nombre;
            });
            sugerenciasContainer.appendChild(div);
        });
        sugerenciasContainer.style.display = 'block';
    }

    async function buscarSugerencias(query) {
        if (!query.trim()) {
            limpiarSugerencias();
            return;
        }
        const tipo = tipoMaterialSelect.value;
        try {
            const url = new URL('/materiales/api/buscar/', window.location.origin);
            url.searchParams.append('q', query);
            if (tipo) url.searchParams.append('tipo_material', tipo);
            const response = await fetch(url);
            if (!response.ok) throw new Error('Error al buscar');
            const data = await response.json();
            mostrarSugerencias(data.resultados);
        } catch (error) {
            console.error('Error en búsqueda:', error);
            limpiarSugerencias();
        }
    }

    // Carga el formulario para un material específico
    async function cargarFormulario(materialId) {
        try {
            // Corrección: uso de backticks para interpolación
            const response = await fetch(`/materiales/formulario/${materialId}/`);
            if (!response.ok) throw new Error('No se pudo cargar el formulario');
            const html = await response.text();
            contenedorFormulario.innerHTML = html;
        } catch (error) {
            contenedorFormulario.innerHTML = `<div class="alert alert-danger">${error.message}</div>`;
        }
    }

    const debouncedBuscar = debounce((e) => {
        buscarSugerencias(e.target.value);
    }, 300);

    buscadorInput.addEventListener('input', debouncedBuscar);

    // También podes limpiar sugerencias si clickeas fuera
    document.addEventListener('click', (e) => {
        if (!sugerenciasContainer.contains(e.target) && e.target !== buscadorInput) {
            limpiarSugerencias();
        }
    });
});