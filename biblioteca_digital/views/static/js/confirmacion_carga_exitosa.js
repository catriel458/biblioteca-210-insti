// confirmacion_carga_exitosa.js
// Lógica para mostrar el modal de confirmación de carga exitosa
// Se asume que Bootstrap 5 está disponible globalmente
// Juni: puedes setear el ID del material recién creado en esta variable
let idMaterialRecienCargado = null; // Asignar dinámicamente tras guardar

// Función para mostrar el modal de éxito
function mostrarModalCargaExitosa(idMaterial) {
  idMaterialRecienCargado = idMaterial;
  
  // Configurar el modal para que no se pueda cerrar con ESC o clic afuera
  const modal = new bootstrap.Modal(document.getElementById('modalConfirmacionCargaExitosa'), {
    backdrop: 'static', // No permite cerrar haciendo clic afuera
    keyboard: false     // No permite cerrar con ESC
  });
  
  modal.show();
  
  // Prevenir el cierre del modal con cualquier método que no sean los botones internos
  const modalElement = document.getElementById('modalConfirmacionCargaExitosa');
  
  // Remover cualquier evento de cierre existente
  modalElement.addEventListener('hide.bs.modal', function (event) {
    // Solo permitir el cierre si viene de nuestros botones
    if (!event.target.dataset.allowClose) {
      event.preventDefault();
      event.stopPropagation();
    }
  });
}

// Función para cerrar el modal de forma segura
function cerrarModalCargaExitosa() {
  const modalElement = document.getElementById('modalConfirmacionCargaExitosa');
  const modal = bootstrap.Modal.getInstance(modalElement);
  
  if (modal) {
    // Marcar que el cierre está permitido
    modalElement.dataset.allowClose = 'true';
    modal.hide();
    
    // Limpiar el flag después del cierre
    modalElement.addEventListener('hidden.bs.modal', function() {
      delete modalElement.dataset.allowClose;
    }, { once: true });
  }
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
    btnVolverInicio.addEventListener('click', function(e) {
      e.preventDefault();
      cerrarModalCargaExitosa();
      
      // Esperar a que el modal se cierre antes de navegar
      setTimeout(() => {
        window.location.href = '/'; // Ajusta la URL según tu sistema
      }, 300);
    });
  }
  
  if (btnVolverAltaMaterial) {
    btnVolverAltaMaterial.addEventListener('click', function(e) {
      e.preventDefault();
      cerrarModalCargaExitosa();
      
      // Esperar a que el modal se cierre antes de navegar
      setTimeout(() => {
        window.location.href = '/alta_material/';
      }, 300);
    });
  }
  
  if (btnVerEditarMaterial) {
    btnVerEditarMaterial.addEventListener('click', function(e) {
      e.preventDefault();
      cerrarModalCargaExitosa();
      
      if (idMaterialRecienCargado) {
        // Esperar a que el modal se cierre antes de navegar
        setTimeout(() => {
          window.location.href = `/materiales/editar-libro/${idMaterialRecienCargado}/`;
        }, 300);
      }
    });
  }
}

// Prevenir el cierre accidental del modal una vez que esté en el DOM
function configurarProteccionModal() {
  const modalElement = document.getElementById('modalConfirmacionCargaExitosa');
  
  if (modalElement) {
    // Prevenir cierre con ESC a nivel de documento cuando el modal esté abierto
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && modalElement.classList.contains('show')) {
        e.preventDefault();
        e.stopPropagation();
      }
    });
    
    // Prevenir cierre por clic en el backdrop
    modalElement.addEventListener('click', function(e) {
      if (e.target === modalElement) {
        e.preventDefault();
        e.stopPropagation();
      }
    });
  }
}

// Ejecutar al cargar el DOM
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', function() {
    asignarEventosModalCargaExitosa();
    configurarProteccionModal();
  });
} else {
  asignarEventosModalCargaExitosa();
  configurarProteccionModal();
}