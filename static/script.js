// Глобальные переменные
let currentL = 3;
let currentM = 4;

// Инициализация при загрузке страницы
window.addEventListener('DOMContentLoaded', () => {
    generateTables();
    loadExample();
});

// Генерация таблиц для ввода оценок
function generateTables() {
    const L = parseInt(document.getElementById('L').value);
    const M = parseInt(document.getElementById('M').value);
    
    if (L < 0 || L > 50) {
        alert('L должно быть от 0 до 50');
        return;
    }
    
    if (M < 0 || M > 20) {
        alert('M должно быть от 0 до 20');
        return;
    }
    
    currentL = L;
    currentM = M;
    
    const container = document.getElementById('tables-container');
    container.innerHTML = '';
    
    // Таблица для делимых пунктов
    if (L > 0) {
        const divisibleWrapper = document.createElement('div');
        divisibleWrapper.className = 'table-wrapper';
        divisibleWrapper.innerHTML = `
            <h3>Оценки делимых пунктов</h3>
            <table>
                <thead>
                    <tr>
                        <th>Пункт</th>
                        ${Array.from({length: L}, (_, i) => `<th>D${i+1}</th>`).join('')}
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Участник A (a_d)</strong></td>
                        ${Array.from({length: L}, (_, i) => 
                            `<td><input type="number" id="a_d_${i}" min="0" step="0.1" value="0"></td>`
                        ).join('')}
                    </tr>
                    <tr>
                        <td><strong>Участник B (b_d)</strong></td>
                        ${Array.from({length: L}, (_, i) => 
                            `<td><input type="number" id="b_d_${i}" min="0" step="0.1" value="0"></td>`
                        ).join('')}
                    </tr>
                </tbody>
            </table>
        `;
        container.appendChild(divisibleWrapper);
    }
    
    // Таблица для неделимых пунктов
    if (M > 0) {
        const indivisibleWrapper = document.createElement('div');
        indivisibleWrapper.className = 'table-wrapper';
        indivisibleWrapper.innerHTML = `
            <h3>Оценки неделимых пунктов</h3>
            <table>
                <thead>
                    <tr>
                        <th>Пункт</th>
                        ${Array.from({length: M}, (_, i) => `<th>W${i+1}</th>`).join('')}
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Участник A (a_w)</strong></td>
                        ${Array.from({length: M}, (_, i) => 
                            `<td><input type="number" id="a_w_${i}" min="0" step="0.1" value="0"></td>`
                        ).join('')}
                    </tr>
                    <tr>
                        <td><strong>Участник B (b_w)</strong></td>
                        ${Array.from({length: M}, (_, i) => 
                            `<td><input type="number" id="b_w_${i}" min="0" step="0.1" value="0"></td>`
                        ).join('')}
                    </tr>
                </tbody>
            </table>
        `;
        container.appendChild(indivisibleWrapper);
    }
}

// Загрузка примера из ТЗ
function loadExample() {
    // Пример из раздела 6 ТЗ
    document.getElementById('L').value = 3;
    document.getElementById('M').value = 4;
    document.getElementById('H').value = 100;
    
    generateTables();
    
    // Делимые пункты
    const a_d = [10, 20, 30];
    const b_d = [15, 15, 20];
    
    // Неделимые пункты
    const a_w = [35, 30, 15, 20];
    const b_w = [18, 20, 12, 25];
    
    // Заполнение таблиц
    for (let i = 0; i < a_d.length; i++) {
        document.getElementById(`a_d_${i}`).value = a_d[i];
        document.getElementById(`b_d_${i}`).value = b_d[i];
    }
    
    for (let i = 0; i < a_w.length; i++) {
        document.getElementById(`a_w_${i}`).value = a_w[i];
        document.getElementById(`b_w_${i}`).value = b_w[i];
    }
}

// Сбор данных из формы
function collectData() {
    const L = currentL;
    const M = currentM;
    const H = parseFloat(document.getElementById('H').value);
    
    const a_d = [];
    const b_d = [];
    for (let i = 0; i < L; i++) {
        a_d.push(parseFloat(document.getElementById(`a_d_${i}`).value) || 0);
        b_d.push(parseFloat(document.getElementById(`b_d_${i}`).value) || 0);
    }
    
    const a_w = [];
    const b_w = [];
    for (let i = 0; i < M; i++) {
        a_w.push(parseFloat(document.getElementById(`a_w_${i}`).value) || 0);
        b_w.push(parseFloat(document.getElementById(`b_w_${i}`).value) || 0);
    }
    
    return { L, M, H, a_d, b_d, a_w, b_w };
}

// Решение задачи
async function solveProblem() {
    const data = collectData();
    
    // Валидация
    const sum_a = data.a_d.reduce((a, b) => a + b, 0) + data.a_w.reduce((a, b) => a + b, 0);
    const sum_b = data.b_d.reduce((a, b) => a + b, 0) + data.b_w.reduce((a, b) => a + b, 0);
    
    if (Math.abs(sum_a - data.H) > 0.1 || Math.abs(sum_b - data.H) > 0.1) {
        alert(`Сумма оценок должна быть равна H=${data.H}.\nТекущие суммы: A=${sum_a.toFixed(2)}, B=${sum_b.toFixed(2)}`);
        return;
    }
    
    // Показать индикатор загрузки
    const button = event.target;
    const originalText = button.innerHTML;
    button.disabled = true;
    button.innerHTML = '<span class="loading"></span> Вычисление...';
    
    try {
        const response = await fetch('/api/solve?debug=true', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.detail || 'Ошибка сервера');
        }
        
        displayResult(result);
        
    } catch (error) {
        displayError(error.message);
    } finally {
        button.disabled = false;
        button.innerHTML = originalText;
    }
}

// Отображение результата
function displayResult(result) {
    const outputSection = document.getElementById('output-section');
    const container = document.getElementById('result-container');
    
    outputSection.style.display = 'block';
    
    if (result.proportional_exists) {
        container.innerHTML = `
            <div class="result-success">
                <div class="result-title">✓ Пропорциональный делёж найден!</div>
                
                <div class="result-details">
                    <div class="detail-group">
                        <h4>Выигрыши участников</h4>
                        <div class="gains">
                            <div class="gain-item">
                                <div class="label">Участник A</div>
                                <div class="value">${result.gains.A}</div>
                            </div>
                            <div class="gain-item">
                                <div class="label">Участник B</div>
                                <div class="value">${result.gains.B}</div>
                            </div>
                        </div>
                    </div>
                    
                    ${renderDivisibleDistribution(result.division.divisible_A, result.division.divisible_B)}
                    ${renderIndivisibleDistribution(result.division.indivisible)}
                    
                    <div class="method-info">
                        Метод: ${result.method}
                        ${result.sp_point ? ` | SP-точка: (${result.sp_point.x}, ${result.sp_point.y})` : ''}
                    </div>
                </div>
                
                <div style="margin-top: 1.5rem;">
                    <button onclick="downloadJSON(${JSON.stringify(result).replace(/"/g, '&quot;')})" class="btn btn-secondary">
                        Скачать JSON
                    </button>
                </div>
            </div>
            
            ${result.debug ? renderDebugInfo(result.debug) : ''}
        `;
    } else {
        container.innerHTML = `
            <div class="result-error">
                <div class="result-title">✗ Пропорциональный делёж не существует</div>
                <p>${result.error || 'Для данных входных данных невозможно найти пропорциональный делёж.'}</p>
            </div>
        `;
    }
    
    // Прокрутка к результату
    outputSection.scrollIntoView({ behavior: 'smooth' });
}

// Отображение распределения делимых пунктов
function renderDivisibleDistribution(divisible_A, divisible_B) {
    if (Object.keys(divisible_A).length === 0) {
        return '';
    }
    
    const items = Object.keys(divisible_A).sort();
    
    return `
        <div class="detail-group">
            <h4>Распределение делимых пунктов</h4>
            <table>
                <thead>
                    <tr>
                        <th>Пункт</th>
                        <th>Участник A</th>
                        <th>Участник B</th>
                    </tr>
                </thead>
                <tbody>
                    ${items.map(item => `
                        <tr>
                            <td>${item}</td>
                            <td>${(divisible_A[item] * 100).toFixed(1)}%</td>
                            <td>${(divisible_B[item] * 100).toFixed(1)}%</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;
}

// Отображение распределения неделимых пунктов
function renderIndivisibleDistribution(sigma) {
    if (sigma.length === 0) {
        return '';
    }
    
    return `
        <div class="detail-group">
            <h4>Распределение неделимых пунктов</h4>
            <div class="indivisible-grid">
                ${sigma.map((owner, i) => `
                    <div class="indivisible-item ${owner === 1 ? 'to-a' : 'to-b'}">
                        W${i+1} → ${owner === 1 ? 'A' : 'B'}
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

// Отображение отладочной информации
function renderDebugInfo(debug) {
    return `
        <details style="margin-top: 1.5rem;">
            <summary style="cursor: pointer; font-weight: 600; padding: 0.5rem; background: #f1f5f9; border-radius: 4px;">
                Отладочная информация
            </summary>
            <div style="margin-top: 1rem; padding: 1rem; background: #f8fafc; border-radius: 4px; font-family: monospace; font-size: 0.875rem;">
                <p><strong>Ломаная R:</strong> ${debug.R_polygon.length} точек</p>
                <p><strong>Размер множества S:</strong> ${debug.S_size}</p>
                <p><strong>Размер Парето-множества SP:</strong> ${debug.SP_size}</p>
                <p><strong>Отсортированные индексы:</strong> [${debug.sorted_indices.join(', ')}]</p>
                <details style="margin-top: 0.5rem;">
                    <summary style="cursor: pointer;">SP-точки</summary>
                    <pre style="margin-top: 0.5rem; overflow-x: auto;">${JSON.stringify(debug.SP_points, null, 2)}</pre>
                </details>
            </div>
        </details>
    `;
}

// Отображение ошибки
function displayError(message) {
    const outputSection = document.getElementById('output-section');
    const container = document.getElementById('result-container');
    
    outputSection.style.display = 'block';
    container.innerHTML = `
        <div class="result-error">
            <div class="result-title">✗ Ошибка</div>
            <p>${message}</p>
        </div>
    `;
    
    outputSection.scrollIntoView({ behavior: 'smooth' });
}

// Скачать результат в JSON
function downloadJSON(data) {
    const json = JSON.stringify(data, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = `fair_division_result_${new Date().getTime()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}
