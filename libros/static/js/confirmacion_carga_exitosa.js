// confirmacion_carga_exitosa.js
// Lógica para mostrar el modal de confirmación de carga exitosa
// Se asume que Bootstrap 5 está disponible globalmente
// Juni: puedes setear el ID del material recién creado en esta variable
let idMaterialRecienCargado = null; // Asignar dinámicamente tras guardar

// Función para mostrar el modal de éxito
function mostrarModalCargaExitosa(idMaterial) {
  idMaterialRecienCargado = idMaterial;
  const modal = new bootstrap.Modal(document.getElementById('modalConfirmacionCargaExitosa'));
  modal.show();
}

// Asignar evento al botón de confirmación del alta de material
const btnConfirmarAlta = document.getElementById('btnConfirmarAltaMaterial');
if (btnConfirmarAlta) {
  btnConfirmarAlta.addEventListener('click', function() {
    // Aquí deberías primero guardar el material vía AJAX o form
    // Suponemos que el guardado fue exitoso y tenemos el ID
    // Por ejemplo:
    // guardarMaterial().then(id => mostrarModalCargaExitosa(id));
    // Por ahora, para demo:
    mostrarModalCargaExitosa(123); // Reemplaza 123 por el ID real
  });
}

// Asignar eventos a los botones del modal
function asignarEventosModalCargaExitosa() {
  const btnVolverInicio = document.getElementById('btnVolverInicio');
  const btnVolverAltaMaterial = document.getElementById('btnVolverAltaMaterial');
  const btnVerEditarMaterial = document.getElementById('btnVerEditarMaterial');

  if (btnVolverInicio) {
    btnVolverInicio.addEventListener('click', function() {
      window.location.href = '/'; // Ajusta la URL según tu sistema
    });
  }
  if (btnVolverAltaMaterial) {
    btnVolverAltaMaterial.addEventListener('click', function() {
      window.location.href = '/alta_material/';
    });
  }
  if (btnVerEditarMaterial) {
    btnVerEditarMaterial.addEventListener('click', function() {
      if (idMaterialRecienCargado) {
        window.location.href = `/materiales/editar-libro/${idMaterialRecienCargado}/`;
      }
    });
  }
}
// Ejecutar al cargar el DOM
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', asignarEventosModalCargaExitosa);
} else {
  asignarEventosModalCargaExitosa();
}
