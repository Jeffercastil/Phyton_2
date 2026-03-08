/*
===============================================
MAIN.JS - JavaScript Principal del Sistema
===============================================
Este archivo contiene funciones globales que se usan
en todas las páginas del sistema
*/

/* 
DOMContentLoaded se ejecuta cuando el HTML está completamente cargado
Es como el "document ready" de jQuery
*/
document.addEventListener('DOMContentLoaded', function() {
    console.log('Sistema de Movimientos - JavaScript cargado correctamente');
    
    // Inicializar funciones cuando la página carga
    inicializarSistema();
});

/* 
===============================================
FUNCIÓN DE INICIALIZACIÓN
===============================================
Se ejecuta al cargar la página
*/
function inicializarSistema() {
    // Marcar el link activo en la navbar
    marcarLinkActivo();
    
    // Configurar cierre de modales con tecla ESC
    configurarTeclaEscape();
    
    // Mostrar mensaje de bienvenida en consola
    mostrarMensajeBienvenida();
}

/* 
===============================================
NAVEGACIÓN: MARCAR LINK ACTIVO
===============================================
Resalta el link del menú que corresponde a la página actual
*/
function marcarLinkActivo() {
    // window.location.pathname obtiene la ruta actual
    // Ejemplo: si estás en http://localhost:8000/dashboard/
    // pathname será "/dashboard/"
    const rutaActual = window.location.pathname;
    
    // Obtenemos todos los links del menú de navegación
    // querySelectorAll busca TODOS los elementos que coincidan
    const linksMenu = document.querySelectorAll('.navbar-menu a');
    
    // Iteramos sobre cada link
    // forEach es como un "for" pero más moderno
    linksMenu.forEach(link => {
        // link.getAttribute('href') obtiene el valor del atributo href
        const hrefLink = link.getAttribute('href');
        
        // Si la ruta actual incluye el href del link
        if (rutaActual.includes(hrefLink) && hrefLink !== '/') {
            // classList.add agrega una clase CSS
            link.classList.add('active');
            // También podemos cambiar el estilo directamente
            link.style.backgroundColor = 'rgba(255,255,255,0.3)';
        }
    });
}

/* 
===============================================
MODALES: CERRAR CON TECLA ESC
===============================================
Permite cerrar cualquier modal presionando la tecla Escape
*/
function configurarTeclaEscape() {
    // addEventListener escucha eventos (keydown = cuando presionas una tecla)
    document.addEventListener('keydown', function(evento) {
        // evento.key contiene la tecla presionada
        if (evento.key === 'Escape' || evento.key === 'Esc') {
            // Buscamos todos los modales que estén visibles
            const modalesAbiertos = document.querySelectorAll('.modal[style*="display: flex"]');
            
            // Cerramos cada modal abierto
            modalesAbiertos.forEach(modal => {
                modal.style.display = 'none';
            });
        }
    });
}

/* 
===============================================
UTILIDADES: FORMATEAR DINERO
===============================================
Convierte un número a formato de dinero colombiano
Ejemplo: 1500000.5 → "$1,500,000.50"
*/
function formatearDinero(numero) {
    // toLocaleString formatea números según la región
    // 'es-CO' = español de Colombia
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',  // Formato de moneda
        currency: 'COP',    // Pesos colombianos
        minimumFractionDigits: 2  // Mínimo 2 decimales
    }).format(numero);
}

/* 
===============================================
UTILIDADES: FORMATEAR FECHA
===============================================
Convierte una fecha a formato legible
Ejemplo: "2024-01-15T10:30:00" → "15 de enero de 2024, 10:30"
*/
function formatearFecha(fechaTexto) {
    // new Date() convierte texto a objeto Date de JavaScript
    const fecha = new Date(fechaTexto);
    
    // Opciones de formato
    const opciones = {
        year: 'numeric',   // Año completo (2024)
        month: 'long',     // Mes completo (enero)
        day: 'numeric',    // Día (15)
        hour: '2-digit',   // Hora (10)
        minute: '2-digit'  // Minutos (30)
    };
    
    // toLocaleDateString formatea la fecha según la región
    return fecha.toLocaleDateString('es-CO', opciones);
}

/* 
===============================================
VALIDACIÓN: VERIFICAR EMAIL
===============================================
Verifica si un email tiene formato válido
Retorna true o false
*/
function esEmailValido(email) {
    // Expresión regular (regex) para validar emails
    // ^ = inicio de la cadena
    // [^\s@]+ = uno o más caracteres que no sean espacio ni @
    // @ = arroba literal
    // \. = punto literal
    // $ = fin de la cadena
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    // test() verifica si el email coincide con el patrón
    return regex.test(email);
}

/* 
===============================================
VALIDACIÓN: VERIFICAR NÚMERO DE TELÉFONO
===============================================
Verifica si un teléfono tiene formato válido (Colombia)
Acepta: 3001234567, 300 123 4567, 300-123-4567
*/
function esTelefonoValido(telefono) {
    // Quitamos espacios y guiones
    // replace() reemplaza texto
    // /\s|-/g es una expresión regular que busca espacios y guiones
    // g = global (todos, no solo el primero)
    const telefonoLimpio = telefono.replace(/\s|-/g, '');
    
    // Verificamos que tenga 10 dígitos y empiece con 3
    // length obtiene la longitud de la cadena
    // startsWith() verifica si empieza con cierto texto
    return telefonoLimpio.length === 10 && telefonoLimpio.startsWith('3');
}

/* 
===============================================
NOTIFICACIONES: MOSTRAR ALERTA PERSONALIZADA
===============================================
Muestra una notificación bonita en lugar del alert() feo del navegador
tipo puede ser: 'success', 'error', 'warning', 'info'
*/
function mostrarNotificacion(mensaje, tipo = 'info') {
    // Creamos un elemento div nuevo
    const notificacion = document.createElement('div');
    
    // classList.add agrega clases CSS
    notificacion.classList.add('notificacion', `notificacion-${tipo}`);
    
    // innerHTML define el contenido HTML del elemento
    // Template literals (` `) permiten incluir variables con ${}
    notificacion.innerHTML = `
        <i class="fas fa-${obtenerIconoNotificacion(tipo)}"></i>
        <span>${mensaje}</span>
    `;
    
    // Aplicamos estilos directamente (en lugar de CSS)
    Object.assign(notificacion.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        padding: '1rem 1.5rem',
        borderRadius: '8px',
        backgroundColor: obtenerColorNotificacion(tipo),
        color: 'white',
        boxShadow: '0 4px 12px rgba(0,0,0,0.2)',
        zIndex: '10000',
        animation: 'slideInRight 0.3s ease',
        display: 'flex',
        alignItems: 'center',
        gap: '0.5rem'
    });
    
    // Agregamos la notificación al body
    // document.body es el elemento <body> del HTML
    // appendChild() agrega un hijo al final
    document.body.appendChild(notificacion);
    
    // setTimeout ejecuta código después de X milisegundos
    // 3000ms = 3 segundos
    setTimeout(() => {
        // Fade out (desvanecimiento)
        notificacion.style.opacity = '0';
        notificacion.style.transform = 'translateX(100px)';
        
        // Después de la animación, eliminamos el elemento
        setTimeout(() => {
            // remove() elimina el elemento del DOM
            notificacion.remove();
        }, 300);
    }, 3000);
}

/* 
Función auxiliar: obtiene el icono según el tipo
*/
function obtenerIconoNotificacion(tipo) {
    // Switch es como múltiples if-else
    switch(tipo) {
        case 'success': return 'check-circle';
        case 'error': return 'exclamation-circle';
        case 'warning': return 'exclamation-triangle';
        case 'info': return 'info-circle';
        default: return 'bell';
    }
}

/* 
Función auxiliar: obtiene el color según el tipo
*/
function obtenerColorNotificacion(tipo) {
    switch(tipo) {
        case 'success': return '#10b981';  // Verde
        case 'error': return '#ef4444';    // Rojo
        case 'warning': return '#f59e0b';  // Naranja
        case 'info': return '#3b82f6';     // Azul
        default: return '#6b7280';         // Gris
    }
}

/* 
===============================================
CONFIRMACIÓN: DIÁLOGO DE CONFIRMACIÓN BONITO
===============================================
Muestra un diálogo de confirmación personalizado
Retorna una Promise que resuelve true o false
*/
function confirmar(mensaje, titulo = '¿Estás seguro?') {
    // Promise es un objeto para manejar operaciones asíncronas
    // resolve se ejecuta cuando el usuario confirma
    // reject se ejecuta cuando el usuario cancela
    return new Promise((resolve) => {
        // Creamos el HTML del diálogo
        const dialogoHTML = `
            <div id="dialogoConfirmacion" class="modal" style="display: flex;">
                <div class="modal-overlay"></div>
                <div class="modal-content" style="max-width: 400px;">
                    <div class="modal-header">
                        <h2><i class="fas fa-question-circle"></i> ${titulo}</h2>
                    </div>
                    <div class="modal-body">
                        <p style="font-size: 1.1rem; color: #374151;">${mensaje}</p>
                        <div class="form-actions" style="margin-top: 2rem;">
                            <button class="btn btn-secondary" onclick="cerrarDialogoConfirmacion(false)">
                                <i class="fas fa-times"></i> Cancelar
                            </button>
                            <button class="btn btn-primary" onclick="cerrarDialogoConfirmacion(true)">
                                <i class="fas fa-check"></i> Confirmar
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Insertamos el diálogo en el body
        document.body.insertAdjacentHTML('beforeend', dialogoHTML);
        
        // Función global para cerrar el diálogo
        // window.cerrarDialogoConfirmacion la hace accesible desde el HTML
        window.cerrarDialogoConfirmacion = function(confirmado) {
            // Buscamos el diálogo por su ID
            const dialogo = document.getElementById('dialogoConfirmacion');
            // Lo eliminamos del DOM
            dialogo.remove();
            // Resolvemos la promesa con el resultado
            resolve(confirmado);
        };
    });
}

/* 
===============================================
DEBUGGING: MENSAJE DE BIENVENIDA
===============================================
Muestra un mensaje bonito en la consola del navegador
F12 o Ctrl+Shift+I para abrir la consola
*/
function mostrarMensajeBienvenida() {
    // console.log muestra mensajes en la consola del navegador
    // %c permite aplicar estilos CSS a los mensajes
    console.log(
        '%c🚀 Sistema de Movimientos %cv1.0',
        'background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 10px 20px; border-radius: 5px; font-size: 16px; font-weight: bold;',
        'background: #333; color: #10b981; padding: 10px; border-radius: 5px; margin-left: 10px;'
    );
    console.log('%cDesarrollado por Jeff 💻', 'color: #667eea; font-size: 12px;');
    console.log('%cEsta aplicación gestiona clientes y transacciones', 'color: #6b7280; font-size: 11px;');
}

/* 
===============================================
UTILIDADES: COPIAR AL PORTAPAPELES
===============================================
Copia texto al portapapeles del sistema
*/
async function copiarAlPortapapeles(texto) {
    try {
        // navigator.clipboard es la API moderna para copiar
        // await espera a que la operación termine
        await navigator.clipboard.writeText(texto);
        mostrarNotificacion('Copiado al portapapeles', 'success');
        return true;
    } catch (error) {
        // Si falla, usamos el método antiguo
        // Este es un fallback para navegadores antiguos
        const textarea = document.createElement('textarea');
        textarea.value = texto;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        
        try {
            document.execCommand('copy');
            mostrarNotificacion('Copiado al portapapeles', 'success');
            return true;
        } catch (err) {
            mostrarNotificacion('Error al copiar', 'error');
            return false;
        } finally {
            // finally se ejecuta siempre, haya error o no
            textarea.remove();
        }
    }
}

/* 
===============================================
UTILIDADES: DEBOUNCE
===============================================
Retrasa la ejecución de una función hasta que
el usuario deje de hacer algo (útil para búsquedas)
*/
function debounce(funcion, tiempo = 300) {
    // Variable para guardar el timeout
    let timeout;
    
    // Retornamos una nueva función
    return function(...args) {
        // clearTimeout cancela el timeout anterior
        clearTimeout(timeout);
        
        // setTimeout ejecuta la función después de X tiempo
        timeout = setTimeout(() => {
            // apply ejecuta la función con los argumentos originales
            funcion.apply(this, args);
        }, tiempo);
    };
}

/* 
Ejemplo de uso de debounce:
const buscarConRetraso = debounce(function(termino) {
    console.log('Buscando:', termino);
}, 500);

// Solo se ejecutará 500ms después de que el usuario deje de escribir
inputBusqueda.addEventListener('input', (e) => {
    buscarConRetraso(e.target.value);
});
*/

/* 
===============================================
EXPORTAR FUNCIONES (OPCIONAL)
===============================================
Si usas módulos de JavaScript, puedes exportar así:
*/
// export { formatearDinero, formatearFecha, mostrarNotificacion, confirmar };

/* 
===============================================
NOTAS IMPORTANTES PARA EL APRENDIZAJE
===============================================

1. COMENTARIOS:
   // Comentario de una línea
   /* Comentario de múltiples líneas */

/*
2. VARIABLES:
   const = constante (no se puede reasignar)
   let = variable (se puede cambiar)
   var = variable antigua (evitar usar)

3. FUNCIONES:
   function nombre() { }  // Declaración tradicional
   const nombre = () => { }  // Arrow function (moderna)

4. SELECTORES DOM:
   document.getElementById('id')  // Un elemento por ID
   document.querySelector('.clase')  // Primer elemento que coincida
   document.querySelectorAll('.clase')  // Todos los elementos

5. EVENTOS:
   elemento.addEventListener('click', function)
   onclick="function()"  // En HTML (menos recomendado)

6. PROMESAS Y ASYNC/AWAIT:
   Úsalas para operaciones que toman tiempo
   (peticiones al servidor, lectura de archivos)

7. CONSOLE:
   console.log() // Ver valores
   console.error() // Ver errores
   console.table() // Ver tablas de datos
*/