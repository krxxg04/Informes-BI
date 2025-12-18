// Función para enviar formulario
function enviarFormulario(tipo, data = null) {
    const form = document.getElementById('formulario');
    const mensaje = document.getElementById('mensaje');
    const submitButton = form.querySelector('button[type="submit"]');
    
    // Si no se proporciona data, recopilar del formulario
    if (!data) {
        const formData = new FormData(form);
        data = {};
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
    }
    
    // Deshabilitar botón y mostrar loading
    submitButton.disabled = true;
    submitButton.innerHTML = '<span class="loading"></span> Generando...';
    
    // Enviar datos
    fetch(`/generar/${tipo}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            mensaje.className = 'mensaje success';
            mensaje.innerHTML = `
                ✓ ¡Documento generado exitosamente!<br>
                <a href="${result.download_url}" download>Haz clic aquí para descargar</a>
            `;
            
            // Auto-descargar
            setTimeout(() => {
                window.location.href = result.download_url;
            }, 500);
            
            // Limpiar formulario después de un momento
            setTimeout(() => {
                if (confirm('¿Deseas crear otro documento del mismo tipo?')) {
                    form.reset();
                    mensaje.style.display = 'none';
                    submitButton.disabled = false;
                    submitButton.textContent = 'Generar Documento';
                } else {
                    window.location.href = '/';
                }
            }, 2000);
        } else {
            throw new Error(result.error || 'Error desconocido');
        }
    })
    .catch(error => {
        mensaje.className = 'mensaje error';
        mensaje.textContent = `✗ Error al generar el documento: ${error.message}`;
        submitButton.disabled = false;
        submitButton.textContent = 'Generar Documento';
    });
}

// Manejar submit de formularios simples
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('formulario');
    
    if (form && !form.hasAttribute('data-custom-submit')) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Determinar tipo de formulario desde la URL
            const path = window.location.pathname;
            const tipo = path.split('/').pop();
            
            enviarFormulario(tipo);
        });
    }
});

// Validación en tiempo real
document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('input[required], textarea[required]');
    
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value.trim() === '') {
                this.style.borderColor = '#dc3545';
            } else {
                this.style.borderColor = '#28a745';
            }
        });
        
        input.addEventListener('focus', function() {
            this.style.borderColor = '#667eea';
        });
    });
});

// Prevenir pérdida de datos
let formModified = false;

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('formulario');
    
    if (form) {
        form.addEventListener('input', function() {
            formModified = true;
        });
        
        form.addEventListener('submit', function() {
            formModified = false;
        });
    }
});

window.addEventListener('beforeunload', function(e) {
    if (formModified) {
        e.preventDefault();
        e.returnValue = '';
        return '';
    }
});

// Función para formatear fecha en español
function formatearFecha(fecha) {
    const meses = [
        'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
        'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
    ];
    
    const date = new Date(fecha);
    const dia = date.getDate();
    const mes = meses[date.getMonth()];
    const anio = date.getFullYear();
    
    return `${dia} de ${mes} de ${anio}`;
}

// Auto-guardado en localStorage (opcional)
function autoGuardar() {
    const form = document.getElementById('formulario');
    if (!form) return;
    
    const tipo = window.location.pathname.split('/').pop();
    const key = `borrador_${tipo}`;
    
    // Cargar borrador si existe
    const borrador = localStorage.getItem(key);
    if (borrador) {
        if (confirm('Se encontró un borrador guardado. ¿Deseas cargarlo?')) {
            const data = JSON.parse(borrador);
            Object.keys(data).forEach(key => {
                const input = form.elements[key];
                if (input) input.value = data[key];
            });
        }
    }
    
    // Guardar automáticamente cada 30 segundos
    setInterval(() => {
        if (formModified) {
            const formData = new FormData(form);
            const data = {};
            for (let [key, value] of formData.entries()) {
                data[key] = value;
            }
            localStorage.setItem(key, JSON.stringify(data));
            console.log('Borrador guardado automáticamente');
        }
    }, 30000);
}

// Iniciar auto-guardado
document.addEventListener('DOMContentLoaded', autoGuardar);
