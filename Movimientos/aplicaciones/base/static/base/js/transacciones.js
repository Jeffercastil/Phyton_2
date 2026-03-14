/*
===============================================
TRANSACCIONES.JS - Lógica de Transacciones
===============================================
Requiere: Chart.js cargado antes de este archivo
Variables Django en el HTML:
  <div id="transaccionesData"
       data-total-ingresos="{{ total_ingresos }}"
       data-total-gastos="{{ total_gastos }}"
       data-top-categorias="{{ top_categorias_json|safe }}"
       data-top-valores="{{ top_valores_json|safe }}"
       data-csrf="{{ csrf_token }}">
  </div>
*/

document.addEventListener('DOMContentLoaded', function () {

    // ── DATOS DJANGO ──────────────────────────────────────────────
    const dataEl = document.getElementById('transaccionesData');
    const csrf   = dataEl ? dataEl.dataset.csrf : '';

    // ── GRÁFICAS ──────────────────────────────────────────────────
    if (dataEl) {
        const totalIngresos = parseFloat(dataEl.dataset.totalIngresos || '0');
        const totalGastos   = parseFloat(dataEl.dataset.totalGastos   || '0');
        const topLabels     = JSON.parse(dataEl.dataset.topCategorias || '[]');
        const topValores    = JSON.parse(dataEl.dataset.topValores    || '[]');

        const colores = [
            '#6366f1','#f59e0b','#10b981','#ef4444',
            '#06b6d4','#8b5cf6','#f97316','#84cc16'
        ];

        // Gráfica Ingresos vs Gastos
        const ctx1 = document.getElementById('graficaIngresosGastos');
        if (ctx1) {
            new Chart(ctx1, {
                type: 'bar',
                data: {
                    labels: ['Ingresos', 'Gastos'],
                    datasets: [{
                        data: [totalIngresos, totalGastos],
                        backgroundColor: ['#10b981cc', '#ef4444cc'],
                        borderColor:     ['#10b981',   '#ef4444'],
                        borderWidth: 2,
                        borderRadius: 12,
                        borderSkipped: false,
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            backgroundColor: '#1e293b',
                            padding: 12,
                            callbacks: { label: ctx => ' $' + ctx.parsed.y.toLocaleString('es-CO') }
                        }
                    },
                    scales: {
                        x: { grid: { display: false }, ticks: { color: '#64748b' } },
                        y: {
                            beginAtZero: true,
                            grid: { color: '#f1f5f9' },
                            ticks: { color: '#64748b', callback: v => '$' + v.toLocaleString('es-CO') }
                        }
                    }
                }
            });
        }

        // Gráfica Top Categorías
        const ctx2 = document.getElementById('graficaTopGastos');
        if (ctx2 && topLabels.length > 0) {
            new Chart(ctx2, {
                type: 'bar',
                data: {
                    labels: topLabels,
                    datasets: [{
                        data: topValores,
                        backgroundColor: colores.map(c => c + 'cc'),
                        borderColor: colores,
                        borderWidth: 2,
                        borderRadius: 8,
                        borderSkipped: false,
                    }]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            backgroundColor: '#1e293b',
                            padding: 12,
                            callbacks: { label: ctx => ' $' + ctx.parsed.x.toLocaleString('es-CO') }
                        }
                    },
                    scales: {
                        x: {
                            beginAtZero: true,
                            grid: { color: '#f1f5f9' },
                            ticks: { color: '#64748b', callback: v => '$' + v.toLocaleString('es-CO') }
                        },
                        y: { grid: { display: false }, ticks: { color: '#334155', font: { size: 11 } } }
                    }
                }
            });
        } else if (ctx2) {
            ctx2.parentElement.innerHTML =
                '<p style="color:#94a3b8; text-align:center; padding-top:4rem;">Sin datos de gastos</p>';
        }
    }

    // ── MODAL NUEVA TRANSACCIÓN ───────────────────────────────────
    window.abrirModalTransaccion = function () {
        document.getElementById('modalTransaccion').style.display = 'flex';
    };

    window.cerrarModalTransaccion = function () {
        document.getElementById('modalTransaccion').style.display = 'none';
        document.getElementById('formTransaccion').reset();
        // Resetear color del select tipo
        const sel = document.getElementById('tipo');
        if (sel) { sel.style.backgroundColor = ''; sel.style.color = ''; }
    };

    window.cambiarColorTipo = function () {
        const sel = document.getElementById('tipo');
        if (!sel) return;
        if (sel.value === 'INGRESO') {
            sel.style.backgroundColor = '#d1fae5';
            sel.style.color = '#065f46';
        } else if (sel.value === 'GASTO') {
            sel.style.backgroundColor = '#fee2e2';
            sel.style.color = '#991b1b';
        } else {
            sel.style.backgroundColor = '';
            sel.style.color = '';
        }
    };

    window.toggleFechaInput = function () {
        const checkbox = document.getElementById('usar_fecha_actual');
        const input    = document.getElementById('fecha');
        if (!checkbox || !input) return;
        input.disabled = checkbox.checked;
        if (checkbox.checked) input.value = '';
    };

    function getFechaActual() {
        const hoy = new Date();
        const anio = hoy.getFullYear();
        const mes  = String(hoy.getMonth() + 1).padStart(2, '0');
        const dia  = String(hoy.getDate()).padStart(2, '0');
        return `${anio}-${mes}-${dia}`;
    }

    window.guardarTransaccion = function (event) {
        event.preventDefault();
        const usarFechaActual  = document.getElementById('usar_fecha_actual').checked;
        const fechaSeleccionada = document.getElementById('fecha').value;
        const datos = {
            tipo:        document.getElementById('tipo').value,
            categoria:   document.getElementById('categoria').value,
            monto:       document.getElementById('monto').value,
            fecha:       usarFechaActual ? getFechaActual() : fechaSeleccionada,
            descripcion: document.getElementById('descripcion').value
        };

        fetch(window.URLS.crearTransaccion, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf },
            body: JSON.stringify(datos)
        })
        .then(r => r.json())
        .then(data => {
            if (data.success) { alert('Transacción creada exitosamente'); location.reload(); }
            else { alert('Error al crear la transacción'); }
        })
        .catch(() => alert('Error al conectar con el servidor'));
    };

    // ── ELIMINAR ──────────────────────────────────────────────────
    window.eliminarTransaccion = function (id) {
        if (!confirm('¿Eliminar esta transacción? Esta acción no se puede deshacer.')) return;
        fetch(`/api/eliminar-transaccion/${id}/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf }
        })
        .then(r => r.json())
        .then(data => {
            if (data.success) { alert('Transacción eliminada'); location.reload(); }
            else { alert('Error: ' + (data.error || 'No se pudo eliminar')); }
        })
        .catch(() => alert('Error al conectar con el servidor'));
    };

    // ── VER / EDITAR ──────────────────────────────────────────────
    let datosOriginales = null;

    window.verTransaccion = function (id) {
        fetch(`/api/obtener-transaccion/${id}/`)
        .then(r => r.json())
        .then(data => {
            if (!data.success) return;
            datosOriginales = data.transaccion;
            document.getElementById('edit_id').value          = datosOriginales.id;
            document.getElementById('edit_fecha').value       = datosOriginales.fecha;
            document.getElementById('edit_tipo').value        = datosOriginales.tipo;
            document.getElementById('edit_categoria').value   = datosOriginales.categoria;
            document.getElementById('edit_monto').value       = datosOriginales.monto;
            document.getElementById('edit_descripcion').value = datosOriginales.descripcion;
            document.getElementById('tituloModal').innerHTML  = '<i class="fas fa-eye"></i> Ver Transacción';
            document.getElementById('botonesVer').style.display     = 'flex';
            document.getElementById('botonesEditar').style.display  = 'none';
            _setReadOnly(true);
            document.getElementById('modalVerEditar').style.display = 'flex';
        });
    };

    window.editarTransaccion = function (id) {
        window.verTransaccion(id);
        setTimeout(window.habilitarEdicion, 150);
    };

    window.habilitarEdicion = function () {
        document.getElementById('tituloModal').innerHTML = '<i class="fas fa-edit"></i> Editar Transacción';
        document.getElementById('botonesVer').style.display    = 'none';
        document.getElementById('botonesEditar').style.display = 'flex';
        _setReadOnly(false);
    };

    window.cancelarEdicion = function () {
        if (datosOriginales) {
            document.getElementById('edit_categoria').value   = datosOriginales.categoria;
            document.getElementById('edit_monto').value       = datosOriginales.monto;
            document.getElementById('edit_descripcion').value = datosOriginales.descripcion;
        }
        document.getElementById('tituloModal').innerHTML = '<i class="fas fa-eye"></i> Ver Transacción';
        document.getElementById('botonesVer').style.display    = 'flex';
        document.getElementById('botonesEditar').style.display = 'none';
        _setReadOnly(true);
    };

    window.cerrarModalVerEditar = function () {
        document.getElementById('modalVerEditar').style.display = 'none';
        datosOriginales = null;
    };

    window.guardarEdicion = function (event) {
        event.preventDefault();
        const id = document.getElementById('edit_id').value;
        const datos = {
            categoria:   document.getElementById('edit_categoria').value,
            monto:       document.getElementById('edit_monto').value,
            descripcion: document.getElementById('edit_descripcion').value
        };
        fetch(`/api/editar-transaccion/${id}/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf },
            body: JSON.stringify(datos)
        })
        .then(r => r.json())
        .then(data => {
            if (data.success) { alert('Transacción actualizada'); location.reload(); }
            else { alert('Error al actualizar'); }
        });
    };

    function _setReadOnly(readonly) {
        ['edit_categoria', 'edit_monto', 'edit_descripcion'].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.readOnly = readonly;
        });
    }
});