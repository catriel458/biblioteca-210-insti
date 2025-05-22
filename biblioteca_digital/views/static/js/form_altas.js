// === PROYECTOR === 
// @returns {string} HTML del bloque de ejemplar de proyector.
function plantillaEjemplarProyector(idx) {
    return `
    <div class="row mb-2">
        <div class="col-md-3">
            <label for="sede_${idx}">Sede:</label>
            <input type="text" class="form-control" id="sede_${idx}" name="sede_${idx}" required placeholder="Sede...">
        </div>
        <div class="col-md-3">
            <label for="n_registro_${idx}">N° de registro:</label>
            <input type="text" class="form-control" id="n_registro_${idx}" name="n_registro_${idx}" required placeholder="N° de registro...">
        </div>
        <div class="col-md-3">
            <label for="modelo_${idx}">Modelo:</label>
            <input type="text" class="form-control" id="modelo_${idx}" name="modelo_${idx}" required placeholder="Modelo..." />
        </div>
    </div>
    `;
}

// === Generador dinámico de ejemplares de proyector ===
window.updateRowsProyector = function () {
    const cantidad = parseInt(document.getElementById('cant_ejemplares').value) || 1;
    const container = document.getElementById('contenedor-ejemplares-proyector');
    container.innerHTML = ''; // Limpiar anteriores

    for (let i = 1; i <= cantidad; i++) {
        container.insertAdjacentHTML('beforeend', plantillaEjemplarProyector(i));
    }
};

// === Inicializar evento al cargar ===
document.addEventListener('DOMContentLoaded', function () {
    const inputCantidadProyector = document.querySelector('input[name="cant_ejemplares"]');
    if (inputCantidadProyector) {
        inputCantidadProyector.addEventListener('input', window.updateRowsProyector);
        window.updateRowsProyector(); // Generar bloque inicial
    }
});
