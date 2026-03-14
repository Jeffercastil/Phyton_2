/*
===============================================
DASHBOARD.JS - Lógica del Dashboard
===============================================
Requiere: Chart.js cargado antes de este archivo
Variables Django que deben estar en el HTML como data-attributes:
  <div id="dashboardData"
       data-categorias="{{ categorias_json|safe }}"
       data-valores="{{ valores_json|safe }}"
       data-total-gastos="{{ total_gastos }}"
       data-total-ingresos="{{ total_ingresos }}">
  </div>
*/

// Patrón robusto: funciona sin importar si Chart.js cargó antes o después
function initDashboard() {
    if (typeof Chart === 'undefined') {
        // Chart.js aún no cargó, esperar 50ms e intentar de nuevo
        return setTimeout(initDashboard, 50);
    }

    // ── LEER DATOS DESDE EL DOM (inyectados por Django) ──────────
    const dataEl = document.getElementById('dashboardData');
    if (!dataEl) return; // Si no hay dashboard, salir

    const rawCategorias = dataEl.dataset.categorias || '[]';
    const rawValores    = dataEl.dataset.valores    || '[]';

    let labels = [], valores = [];
    try { labels  = JSON.parse(rawCategorias); } catch(e) { console.warn('categorias JSON inválido:', rawCategorias); }
    try { valores = JSON.parse(rawValores);    } catch(e) { console.warn('valores JSON inválido:', rawValores); }
    const totalGastos   = parseFloat(dataEl.dataset.totalGastos   || '0');
    const totalIngresos = parseFloat(dataEl.dataset.totalIngresos || '0');

    const coloresPaleta = [
        '#6366f1','#10b981','#f59e0b','#ef4444',
        '#06b6d4','#8b5cf6','#f97316','#84cc16','#d946ef','#14b8a6'
    ];

    // ── GRÁFICA DE BARRAS: Gastos por Categoría ──────────────────
    const ctxBar = document.getElementById('graficaCategorias');
    if (ctxBar && labels.length > 0) {
        new Chart(ctxBar, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Gasto ($)',
                    data: valores,
                    backgroundColor: coloresPaleta.map(c => c + 'cc'),
                    borderColor: coloresPaleta,
                    borderWidth: 2,
                    borderRadius: 10,
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
                        grid: { color: '#f1f5f9' },
                        ticks: {
                            color: '#64748b',
                            callback: v => '$' + v.toLocaleString('es-CO')
                        }
                    }
                }
            }
        });
    }

    // ── GRÁFICA DONUT: Ingresos vs Gastos ────────────────────────
    const ctxDonut = document.getElementById('graficaDonut');
    if (ctxDonut) {
        new Chart(ctxDonut, {
            type: 'doughnut',
            data: {
                labels: ['Ingresos', 'Gastos'],
                datasets: [{
                    data: [totalIngresos, totalGastos],
                    backgroundColor: ['#10b981cc', '#ef4444cc'],
                    borderColor:     ['#10b981',   '#ef4444'],
                    borderWidth: 2,
                    hoverOffset: 10,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '70%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: '#475569', padding: 16, font: { size: 13 } }
                    },
                    tooltip: {
                        backgroundColor: '#1e293b',
                        padding: 12,
                        cornerRadius: 10,
                        callbacks: {
                            label: ctx => ' $' + ctx.parsed.toLocaleString('es-CO')
                        }
                    }
                }
            }
        });
    }

    // ── LISTA DE CATEGORÍAS ───────────────────────────────────────
    const lista = document.getElementById('listaCategorias');
    if (lista && labels.length > 0) {
        const maxValor = Math.max(...valores);
        labels.forEach((label, i) => {
            const porcentaje = totalGastos > 0
                ? ((valores[i] / totalGastos) * 100).toFixed(1)
                : 0;
            const barWidth = maxValor > 0 ? (valores[i] / maxValor * 100).toFixed(0) : 0;
            const color = coloresPaleta[i % coloresPaleta.length];
            lista.innerHTML += `
                <div style="margin-bottom: 0.9rem;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:0.3rem;">
                        <span style="color:#334155; font-size:0.88rem; font-weight:500;">
                            <span style="display:inline-block; width:10px; height:10px;
                                         border-radius:50%; background:${color};
                                         margin-right:6px;"></span>
                            ${label}
                        </span>
                        <span style="color:#64748b; font-size:0.85rem;">
                            $${valores[i].toLocaleString('es-CO')}
                            <span style="color:#94a3b8;">(${porcentaje}%)</span>
                        </span>
                    </div>
                    <div style="background:#f1f5f9; border-radius:99px; height:6px;">
                        <div style="width:${barWidth}%; height:100%; border-radius:99px;
                                    background:${color}; transition:width 0.6s ease;"></div>
                    </div>
                </div>`;
        });
    }
}

window.addEventListener('load', initDashboard);