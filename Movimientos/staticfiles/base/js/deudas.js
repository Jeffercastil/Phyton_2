/*
===============================================
DEUDAS.JS - Gestión de Deudas
===============================================
Requiere: Chart.js cargado en base.html (sin defer)
Requiere en el HTML:
  <div id="deudasData"
       data-nombres='...'
       data-pendientes='...'
       data-pagados='...'
       data-csrf="...">
  </div>
  <script> window.URLS = { crearDeuda: "..." }; </script>
*/

function initDeudas() {
    if (typeof Chart === 'undefined') {
        return setTimeout(initDeudas, 50);
    }

    // ── DATOS DEL DOM ─────────────────────────────────────────────
    const dataEl = document.getElementById('deudasData');
    const csrf   = dataEl ? dataEl.dataset.csrf : '';

    // ── GRÁFICA DE BARRAS ─────────────────────────────────────────
    if (dataEl) {
        let nombres   = [], pendiente = [], pagado = [];
        try { nombres   = JSON.parse(dataEl.dataset.nombres    || '[]'); } catch(e) {}
        try { pendiente = JSON.parse(dataEl.dataset.pendientes || '[]'); } catch(e) {}
        try { pagado    = JSON.parse(dataEl.dataset.pagados    || '[]'); } catch(e) {}

        const ctx = document.getElementById('graficaDeudas');
        if (ctx && nombres.length > 0) {
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: nombres,
                    datasets: [
                        {
                            label: 'Pagado',
                            data: pagado,
                            backgroundColor: '#10b981cc',
                            borderColor: '#10b981',
                            borderWidth: 2,
                            borderRadius: 8,
                        },
                        {
                            label: 'Pendiente',
                            data: pendiente,
                            backgroundColor: '#ef4444cc',
                            borderColor: '#ef4444',
                            borderWidth: 2,
                            borderRadius: 8,
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'top' },
                        tooltip: {
                            backgroundColor: '#1e293b',
                            padding: 12,
                            cornerRadius: 10,
                            callbacks: {
                                label: ctx => ' $' + ctx.parsed.y.toLocaleString('es-CO')
                            }
                        }
                    },
                    scales: {
                        x: { grid: { display: false }, ticks: { color: '#64748b' } },
                        y: {
                            beginAtZero: true,
                            ticks: {
                                color: '#64748b',
                                callback: v => '$' + v.toLocaleString('es-CO')
                            }
                        }
                    }
                }
            });
        }
    }

    // ── MINI GRÁFICAS DONA POR DEUDA ─────────────────────────────
    document.querySelectorAll('canvas[id^="miniChart_"]').forEach(function(canvas) {
        const pagado    = parseFloat(canvas.dataset.pagado)    || 0;
        const pendiente = parseFloat(canvas.dataset.pendiente) || 0;
        const total = pagado + pendiente;
        new Chart(canvas, {
            type: 'doughnut',
            data: {
                labels: ['Pagado', 'Pendiente'],
                datasets: [{
                    data: total > 0 ? [pagado, pendiente] : [0, 1],
                    backgroundColor: total > 0 ? ['#10b981', '#ef4444'] : ['#e2e8f0', '#e2e8f0'],
                    borderWidth: 0,
                }]
            },
            options: {
                responsive: false,
                cutout: '70%',
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: ctx => ' $' + ctx.parsed.toLocaleString('es-CO')
                        }
                    }
                }
            }
        });
    });

    // ══════════════════════════════════════════
    // MODAL NUEVA DEUDA
    // ══════════════════════════════════════════

    window.abrirModalDeuda = function () {
        document.getElementById('d_fecha').value = hoy();
        // Limpiar campos
        ['d_nombre','d_valor_inicial','d_valor_total','d_meses','d_cuota','d_descripcion']
            .forEach(id => { const el = document.getElementById(id); if(el) el.value = ''; });
        document.getElementById('d_tipo').value = 'DEUDA';
        document.getElementById('resumenInteres').style.display = 'none';
        document.getElementById('modalDeuda').style.display = 'flex';
    };

    window.cerrarModalDeuda = function () {
        document.getElementById('modalDeuda').style.display = 'none';
    };

    window.calcularCuota = function () {
        const total   = parseFloat(document.getElementById('d_valor_total').value)   || 0;
        const inicial = parseFloat(document.getElementById('d_valor_inicial').value) || 0;
        const meses   = parseInt(document.getElementById('d_meses').value)           || 0;

        if (total > 0 && meses > 0) {
            document.getElementById('d_cuota').value = (total / meses).toFixed(2);
        }
        if (total > 0 && inicial > 0) {
            const interes = total - inicial;
            const tasa    = ((interes / inicial) * 100).toFixed(1);
            document.getElementById('montoInteres').textContent = '$' + interes.toLocaleString('es-CO');
            document.getElementById('tasaInteres').textContent  = tasa + '%';
            document.getElementById('resumenInteres').style.display = 'block';
        }
    };

    window.guardarDeuda = function () {
        const nombre      = document.getElementById('d_nombre').value.trim();
        const valor_ini   = document.getElementById('d_valor_inicial').value;
        const valor_total = document.getElementById('d_valor_total').value;
        const meses       = document.getElementById('d_meses').value;
        const cuota       = document.getElementById('d_cuota').value;
        const fecha       = document.getElementById('d_fecha').value;

        if (!nombre || !valor_ini || !valor_total || !meses || !cuota || !fecha) {
            alert('Por favor completa todos los campos obligatorios.');
            return;
        }

        const datos = {
            nombre,
            tipo:               document.getElementById('d_tipo').value,
            valor_inicial:      valor_ini,
            valor_total_a_pagar: valor_total,
            cuota_mensual:      cuota,
            total_meses:        meses,
            fecha_inicio:       fecha,
            descripcion:        document.getElementById('d_descripcion').value,
        };

        fetch(window.URLS.crearDeuda, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf },
            body: JSON.stringify(datos)
        })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                cerrarModalDeuda();
                location.reload();
            } else {
                alert('Error: ' + (data.error || 'No se pudo guardar'));
            }
        })
        .catch(() => alert('Error de conexión al guardar la deuda.'));
    };

    // ══════════════════════════════════════════
    // MODAL EDITAR DEUDA
    // ══════════════════════════════════════════

    window.abrirEditar = function (id, nombre, tipo, valorInicial, valorTotal, cuota, meses, fecha, descripcion) {
        document.getElementById('e_id').value          = id;
        document.getElementById('e_nombre').value      = nombre;
        document.getElementById('e_tipo').value        = tipo;
        document.getElementById('e_valor_inicial').value = valorInicial;
        document.getElementById('e_valor_total').value = valorTotal;
        document.getElementById('e_cuota').value       = cuota;
        document.getElementById('e_meses').value       = meses;
        document.getElementById('e_fecha').value       = fecha;
        document.getElementById('e_descripcion').value = descripcion || '';
        document.getElementById('modalEditar').style.display = 'flex';
    };

    window.cerrarEditar = function () {
        document.getElementById('modalEditar').style.display = 'none';
    };

    window.guardarEdicion = function () {
        const id     = document.getElementById('e_id').value;
        const nombre = document.getElementById('e_nombre').value.trim();
        if (!nombre) { alert('El nombre es obligatorio.'); return; }

        const datos = {
            nombre,
            tipo:               document.getElementById('e_tipo').value,
            valor_inicial:      document.getElementById('e_valor_inicial').value,
            valor_total_a_pagar: document.getElementById('e_valor_total').value,
            cuota_mensual:      document.getElementById('e_cuota').value,
            total_meses:        document.getElementById('e_meses').value,
            fecha_inicio:       document.getElementById('e_fecha').value,
            descripcion:        document.getElementById('e_descripcion').value,
        };

        fetch(`/api/editar-deuda/${id}/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf },
            body: JSON.stringify(datos)
        })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                cerrarEditar();
                location.reload();
            } else {
                alert('Error: ' + (data.error || 'No se pudo guardar'));
            }
        })
        .catch(() => alert('Error de conexión al editar la deuda.'));
    };

    // ══════════════════════════════════════════
    // MODAL PAGO
    // ══════════════════════════════════════════

    window.abrirPago = function (id, nombre, cuota) {
        document.getElementById('pago_deuda_id').value       = id;
        document.getElementById('pagoNombreDeuda').textContent = '💳 Deuda: ' + nombre;
        document.getElementById('pago_monto').value          = cuota;
        document.getElementById('pago_fecha').value          = hoy();
        document.getElementById('modalPago').style.display   = 'flex';
    };

    window.cerrarPago = function () {
        document.getElementById('modalPago').style.display = 'none';
    };

    window.registrarPago = function () {
        const id    = document.getElementById('pago_deuda_id').value;
        const monto = document.getElementById('pago_monto').value;
        const fecha = document.getElementById('pago_fecha').value;

        if (!monto || !fecha) { alert('Completa el monto y la fecha.'); return; }

        fetch(`/api/pagar-deuda/${id}/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf },
            body: JSON.stringify({ monto, fecha })
        })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                alert('✅ Pago registrado. Saldo pendiente: $' + data.saldo_pendiente.toLocaleString('es-CO'));
                cerrarPago();
                location.reload();
            } else {
                alert('Error: ' + (data.error || 'No se pudo registrar'));
            }
        })
        .catch(() => alert('Error de conexión al registrar el pago.'));
    };

    // ══════════════════════════════════════════
    // ELIMINAR DEUDA
    // ══════════════════════════════════════════

    window.eliminarDeuda = function (id) {
        if (!confirm('¿Archivar esta deuda? No se eliminará del historial.')) return;
        fetch(`/api/eliminar-deuda/${id}/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf }
        })
        .then(r => r.json())
        .then(data => { if (data.success) location.reload(); })
        .catch(() => alert('Error de conexión al eliminar.'));
    };

    // ══════════════════════════════════════════
    // UTILIDAD
    // ══════════════════════════════════════════
    function hoy() {
        return new Date().toISOString().split('T')[0];
    }
}


    // ══════════════════════════════════════════
    // CALCULADORA
    // ══════════════════════════════════════════

    let calcValor1    = null;
    let calcOperacion = null;
    let calcEsperandoV2 = false;
    let calcResultado = '0';

    window.abrirCalculadora = function() {
        calcClear();
        document.getElementById('modalCalculadora').style.display = 'flex';
    };
    window.cerrarCalculadora = function() {
        document.getElementById('modalCalculadora').style.display = 'none';
    };

    function calcActualizar(texto) {
        calcResultado = texto;
        document.getElementById('calc_display').textContent = parseFloat(texto).toLocaleString('es-CO', {maximumFractionDigits: 10});
    }

    window.calcNum = function(n) {
        if (calcEsperandoV2) {
            calcResultado = n;
            calcEsperandoV2 = false;
        } else {
            calcResultado = calcResultado === '0' ? n : calcResultado + n;
        }
        document.getElementById('calc_display').textContent = calcResultado;
    };

    window.calcPunto = function() {
        if (calcEsperandoV2) { calcResultado = '0'; calcEsperandoV2 = false; }
        if (!calcResultado.includes('.')) calcResultado += '.';
        document.getElementById('calc_display').textContent = calcResultado;
    };

    window.calcOperador = function(op) {
        calcValor1    = parseFloat(calcResultado);
        calcOperacion = op;
        calcEsperandoV2 = true;
        const simbolos = { '+': '+', '-': '−', '*': '×', '/': '÷' };
        document.getElementById('calc_historial').textContent =
            calcValor1.toLocaleString('es-CO') + ' ' + simbolos[op];
    };

    window.calcIgual = function() {
        if (calcValor1 === null || calcOperacion === null) return;
        const v2 = parseFloat(calcResultado);
        let res;
        if      (calcOperacion === '+') res = calcValor1 + v2;
        else if (calcOperacion === '-') res = calcValor1 - v2;
        else if (calcOperacion === '*') res = calcValor1 * v2;
        else if (calcOperacion === '/') res = v2 !== 0 ? calcValor1 / v2 : 0;
        const simbolos = { '+': '+', '-': '−', '*': '×', '/': '÷' };
        document.getElementById('calc_historial').textContent =
            calcValor1.toLocaleString('es-CO') + ' ' + simbolos[calcOperacion] + ' ' + v2.toLocaleString('es-CO') + ' =';
        calcActualizar(String(parseFloat(res.toFixed(10))));
        calcValor1    = null;
        calcOperacion = null;
        calcEsperandoV2 = true;
    };

    window.calcPorcentaje = function() {
        const v = parseFloat(calcResultado);
        if (calcValor1 !== null) {
            // Porcentaje de la base: ej. 9553122 * 15% = cuánto es el 15%
            const pct = (calcValor1 * v) / 100;
            document.getElementById('calc_historial').textContent =
                calcValor1.toLocaleString('es-CO') + ' × ' + v + '% =';
            calcActualizar(String(parseFloat(pct.toFixed(10))));
            calcValor1 = null; calcOperacion = null; calcEsperandoV2 = true;
        } else {
            calcActualizar(String(parseFloat((v / 100).toFixed(10))));
        }
    };

    window.calcClear = function() {
        calcValor1 = null; calcOperacion = null; calcEsperandoV2 = false;
        calcResultado = '0';
        document.getElementById('calc_display').textContent  = '0';
        document.getElementById('calc_historial').textContent = '';
    };

    window.calcCopiarResultado = function() {
        // Pregunta en qué campo poner el resultado
        const valor = parseFloat(calcResultado);
        if (isNaN(valor)) return;

        // Si el modal de nueva deuda está abierto, llenar el campo activo
        const modalDeuda   = document.getElementById('modalDeuda');
        const modalEditar  = document.getElementById('modalEditar');

        let campos = [];
        if (modalDeuda && modalDeuda.style.display === 'flex') {
            campos = [
                { id: 'd_valor_inicial', label: 'Valor inicial' },
                { id: 'd_valor_total',   label: 'Valor total a pagar' },
                { id: 'd_cuota',         label: 'Cuota mensual' },
            ];
        } else if (modalEditar && modalEditar.style.display === 'flex') {
            campos = [
                { id: 'e_valor_inicial', label: 'Valor inicial' },
                { id: 'e_valor_total',   label: 'Valor total a pagar' },
                { id: 'e_cuota',         label: 'Cuota mensual' },
            ];
        }

        if (campos.length === 0) {
            alert('Resultado: $' + valor.toLocaleString('es-CO') + '\n\nAbre el formulario de deuda primero para poder usarlo.');
            return;
        }

        // Mostrar opciones
        let opciones = campos.map((c, i) => (i + 1) + ') ' + c.label).join('\n');
        const seleccion = prompt(
            'Resultado: $' + valor.toLocaleString('es-CO') +
            '\n\n¿En qué campo deseas colocar este valor?\n\n' + opciones +
            '\n\nEscribe el número:'
        );
        const idx = parseInt(seleccion) - 1;
        if (idx >= 0 && idx < campos.length) {
            document.getElementById(campos[idx].id).value = valor;
            calcularCuota(); // Recalcular si aplica
            cerrarCalculadora();
        }
    };


window.addEventListener('load', initDeudas);