// Глобальные переменные
let currentL = 3;
let currentM = 4;

// Инициализация при загрузке страницы
window.addEventListener('DOMContentLoaded', () => {
    generateTables();
    loadExample();
});

// Переключение видимости примеров
function toggleExamples() {
    const content = document.getElementById('examples-content');
    content.classList.toggle('open');
}

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

// Загрузка примера из ТЗ (оставляем для совместимости)
function loadExample() {
    loadExample1();
}

// Example 1 - Divorce Arrangement (все делимые)
function loadExample1() {
    document.getElementById('L').value = 5;
    document.getElementById('M').value = 0;
    document.getElementById('H').value = 100;
    
    generateTables();
    
    // Retirement, House, Cottage, Portfolio, Other
    const a_d = [50, 20, 15, 10, 5];
    const b_d = [40, 30, 10, 10, 10];
    
    for (let i = 0; i < a_d.length; i++) {
        document.getElementById(`a_d_${i}`).value = a_d[i];
        document.getElementById(`b_d_${i}`).value = b_d[i];
    }
    
    showNotification('Загружен Example 1: Развод (56.67/56.67)');
}

// Example 2 - Mergers (1 делимый, 4 неделимых)
function loadExample2() {
    document.getElementById('L').value = 1;
    document.getElementById('M').value = 4;
    document.getElementById('H').value = 100;
    
    generateTables();
    
    // Laying off (делимый)
    const a_d = [30];
    const b_d = [10];
    
    // CEO, President, Headquarters, Name (неделимые)
    const a_w = [25, 15, 20, 10];
    const b_w = [10, 20, 35, 25];
    
    for (let i = 0; i < a_d.length; i++) {
        document.getElementById(`a_d_${i}`).value = a_d[i];
        document.getElementById(`b_d_${i}`).value = b_d[i];
    }
    
    for (let i = 0; i < a_w.length; i++) {
        document.getElementById(`a_w_${i}`).value = a_w[i];
        document.getElementById(`b_w_${i}`).value = b_w[i];
    }
    
    showNotification('Загружен Example 2: Слияние компаний (62.5/62.5)');
}

// Example 3 - No Fair Division (2 делимых, 3 неделимых)
function loadExample3() {
    document.getElementById('L').value = 2;
    document.getElementById('M').value = 3;
    document.getElementById('H').value = 100;
    
    generateTables();
    
    const a_d = [10, 10];
    const b_d = [30, 20];
    
    const a_w = [35, 30, 15];
    const b_w = [18, 20, 12];
    
    for (let i = 0; i < a_d.length; i++) {
        document.getElementById(`a_d_${i}`).value = a_d[i];
        document.getElementById(`b_d_${i}`).value = b_d[i];
    }
    
    for (let i = 0; i < a_w.length; i++) {
        document.getElementById(`a_w_${i}`).value = a_w[i];
        document.getElementById(`b_w_${i}`).value = b_w[i];
    }
    
    showNotification('Загружен Example 3: Пропорциональный есть, fair нет');
}

// Example 4 - No Proportional (1 делимый, 4 неделимых)
function loadExample4() {
    document.getElementById('L').value = 1;
    document.getElementById('M').value = 4;
    document.getElementById('H').value = 100;
    
    generateTables();
    
    const a_d = [1];
    const b_d = [1];
    
    const a_w = [45, 30, 15, 9];
    const b_w = [30, 25, 22, 22];
    
    for (let i = 0; i < a_d.length; i++) {
        document.getElementById(`a_d_${i}`).value = a_d[i];
        document.getElementById(`b_d_${i}`).value = b_d[i];
    }
    
    for (let i = 0; i < a_w.length; i++) {
        document.getElementById(`a_w_${i}`).value = a_w[i];
        document.getElementById(`b_w_${i}`).value = b_w[i];
    }
    
    showNotification('Загружен Example 4: Пропорциональный делёж не существует');
}

// Example 5 - Proportional, No Equitable (1 делимый, 4 неделимых)
function loadExample5() {
    document.getElementById('L').value = 1;
    document.getElementById('M').value = 4;
    document.getElementById('H').value = 100;
    
    generateTables();
    
    const a_d = [3];
    const b_d = [3];
    
    const a_w = [45, 30, 20, 2];
    const b_w = [17, 20, 22, 38];
    
    for (let i = 0; i < a_d.length; i++) {
        document.getElementById(`a_d_${i}`).value = a_d[i];
        document.getElementById(`b_d_${i}`).value = b_d[i];
    }
    
    for (let i = 0; i < a_w.length; i++) {
        document.getElementById(`a_w_${i}`).value = a_w[i];
        document.getElementById(`b_w_${i}`).value = b_w[i];
    }
    
    showNotification('Загружен Example 5: Есть пропорциональный, нет равноценного');
}

// Example 6 - Equitable Not Efficient (1 делимый, 4 неделимых)
function loadExample6() {
    document.getElementById('L').value = 1;
    document.getElementById('M').value = 4;
    document.getElementById('H').value = 100;
    
    generateTables();
    
    const a_d = [5];
    const b_d = [5];
    
    const a_w = [40, 10, 20, 25];
    const b_w = [49, 1, 25, 20];
    
    for (let i = 0; i < a_d.length; i++) {
        document.getElementById(`a_d_${i}`).value = a_d[i];
        document.getElementById(`b_d_${i}`).value = b_d[i];
    }
    
    for (let i = 0; i < a_w.length; i++) {
        document.getElementById(`a_w_${i}`).value = a_w[i];
        document.getElementById(`b_w_${i}`).value = b_w[i];
    }
    
    showNotification('Загружен Example 6: Равноценный есть, но неэффективен');
}

// Example 7 - Fair Division Exists (1 делимый, 4 неделимых)
function loadExample7() {
    document.getElementById('L').value = 1;
    document.getElementById('M').value = 4;
    document.getElementById('H').value = 100;
    
    generateTables();
    
    const a_d = [17];
    const b_d = [17];
    
    const a_w = [42, 37, 2, 2];
    const b_w = [45, 34, 2, 2];
    
    for (let i = 0; i < a_d.length; i++) {
        document.getElementById(`a_d_${i}`).value = a_d[i];
        document.getElementById(`b_d_${i}`).value = b_d[i];
    }
    
    for (let i = 0; i < a_w.length; i++) {
        document.getElementById(`a_w_${i}`).value = a_w[i];
        document.getElementById(`b_w_${i}`).value = b_w[i];
    }
    
    showNotification('Загружен Example 7: Fair division существует (51.5/51.5)');
}

// Example 8 - Only Indivisible (только неделимые)
function loadExample8() {
    document.getElementById('L').value = 0;
    document.getElementById('M').value = 3;
    document.getElementById('H').value = 100;
    
    generateTables();
    
    const a_w = [51, 45, 4];
    const b_w = [40, 50, 10];
    
    for (let i = 0; i < a_w.length; i++) {
        document.getElementById(`a_w_${i}`).value = a_w[i];
        document.getElementById(`b_w_${i}`).value = b_w[i];
    }
    
    showNotification('Загружен Example 8: Только неделимые пункты');
}

// Показать уведомление
function showNotification(message) {
    // Создаем элемент уведомления
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    document.body.appendChild(notification);
    
    // Показываем уведомление
    setTimeout(() => notification.classList.add('show'), 100);
    
    // Скрываем и удаляем через 3 секунды
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
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
// Отображение классификации решения
function renderStatement1Classification(result) {
    if (!result.statement1_sets) {
        return '';
    }
    
    const sets = result.statement1_sets;
    const belongs = result.belongs_to_sets || 'U(S)';
    
    // statement1_sets - массив строк типа ['E(S)', 'P(S)', 'Q(S)', 'F(S)']
    // или используем has_* флаги
    const hasF = result.has_fair || sets.includes('F(S)');
    const hasQ = result.has_equitable || sets.includes('Q(S)');
    const hasP = result.has_proportional || sets.includes('P(S)');
    const hasE = result.has_efficient || sets.includes('E(S)');
    
    // Определяем класс на основе наивысшего множества
    let mainClass = 'statement1-u';
    let mainLabel = 'U(S)';
    let mainDescription = 'Универсум';
    
    if (hasF) {
        mainClass = 'statement1-f';
        mainLabel = 'F(S)';
        mainDescription = 'Fair — Справедливое решение';
    } else if (hasQ) {
        mainClass = 'statement1-q';
        mainLabel = 'Q(S)';
        mainDescription = 'Equitable — Равноценное решение';
    } else if (hasP) {
        mainClass = 'statement1-p';
        mainLabel = 'P(S)';
        mainDescription = 'Proportional — Пропорциональное решение';
    } else if (hasE) {
        mainClass = 'statement1-e';
        mainLabel = 'E(S)';
        mainDescription = 'Efficient — Эффективное решение';
    }
    
    return `
        <div class="statement1-classification ${mainClass}">
            <div class="statement1-header">
                <div class="statement1-badge">${mainLabel}</div>
                <div class="statement1-description">${mainDescription}</div>
            </div>
            
            <div class="statement1-formula">
                F(S) ⊆ Q(S) ⊆ P(S) ⊆ E(S) = U(S)
            </div>
            
            <div class="statement1-grid">
                <div class="statement1-item ${hasE ? 'active' : 'inactive'}">
                    <div class="statement1-icon">${hasE ? '✓' : '✗'}</div>
                    <div class="statement1-label">E(S)</div>
                    <div class="statement1-desc">Efficient<br><small>Парето-оптимальное</small></div>
                </div>
                
                <div class="statement1-item ${hasP ? 'active' : 'inactive'}">
                    <div class="statement1-icon">${hasP ? '✓' : '✗'}</div>
                    <div class="statement1-label">P(S)</div>
                    <div class="statement1-desc">Proportional<br><small>GA≥H/2, GB≥H/2</small></div>
                </div>
                
                <div class="statement1-item ${hasQ ? 'active' : 'inactive'}">
                    <div class="statement1-icon">${hasQ ? '✓' : '✗'}</div>
                    <div class="statement1-label">Q(S)</div>
                    <div class="statement1-desc">Equitable<br><small>GA = GB</small></div>
                </div>
                
                <div class="statement1-item ${hasF ? 'active' : 'inactive'}">
                    <div class="statement1-icon">${hasF ? '✓' : '✗'}</div>
                    <div class="statement1-label">F(S)</div>
                    <div class="statement1-desc">Fair<br><small>E ∩ P ∩ Q</small></div>
                </div>
            </div>
            
            <div class="statement1-euler">
                <div class="euler-diagram">
                    <div class="euler-circle euler-e ${hasE ? 'active' : ''}">
                        <span>E</span>
                        <div class="euler-circle euler-p ${hasP ? 'active' : ''}">
                            <span>P</span>
                            <div class="euler-circle euler-q ${hasQ ? 'active' : ''}">
                                <span>Q</span>
                                <div class="euler-circle euler-f ${hasF ? 'active' : ''}">
                                    <span>F</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="euler-legend">
                    <p><strong>Диаграмма Эйлера</strong></p>
                    <p>Решение принадлежит множеству: <strong>${belongs}</strong></p>
                </div>
            </div>
        </div>
    `;
}

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
                    
                    ${renderStatement1Classification(result)}
                    
                    ${renderDivisibleDistribution(result.division.divisible_A, result.division.divisible_B)}
                    ${renderIndivisibleDistribution(result.division.indivisible)}
                    
                    <div class="method-info">
                        Метод: ${result.method}
                        ${result.sp_point ? ` | SP-точка: (${result.sp_point.x}, ${result.sp_point.y})` : ''}
                    </div>
                </div>
                
                <div style="margin-top: 1.5rem; display: flex; gap: 1rem;">
                    <button onclick="downloadJSON(${JSON.stringify(result).replace(/"/g, '&quot;')})" class="btn btn-secondary">
                        Скачать JSON
                    </button>
                    <button onclick="showAdGraph()" class="btn btn-secondary">
                        График Ad
                    </button>
                </div>
            </div>
            
            ${result.debug ? renderDebugInfo(result.debug) : ''}
            
            <div id="graph-container" style="margin-top: 2rem;"></div>
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
    
    // Автоматически показываем график Ad
    if (result.proportional_exists) {
        setTimeout(() => showAdGraph(), 500);
    }
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

// Показать график области достижимости Ad
async function showAdGraph() {
    const data = collectData();
    const graphContainer = document.getElementById('graph-container');
    
    graphContainer.innerHTML = '<div style="text-align: center; padding: 2rem;"><span class="loading"></span> Построение графика...</div>';
    
    try {
        // Запрос графика с SP-точками (более полный)
        const response = await fetch('/api/plot/ad-with-sp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.detail || 'Ошибка построения графика');
        }
        
        if (result.success) {
            graphContainer.innerHTML = `
                <div style="background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h3 style="text-align: center; margin-bottom: 1rem; color: var(--primary-color);">
                        График области достижимости Ad
                    </h3>
                    <div style="text-align: center;">
                        <img src="data:image/png;base64,${result.image}" 
                             alt="График Ad" 
                             style="max-width: 100%; height: auto; border: 1px solid #e2e8f0; border-radius: 4px;">
                    </div>
                    <div style="margin-top: 1rem; text-align: center; color: var(--text-secondary); font-size: 0.9rem;">
                        <p>Чёрная ломаная R — область достижимости для делимых пунктов</p>
                        <p>Красные квадраты — Парето-оптимальные точки SP от неделимых (найдено: ${result.sp_count})</p>
                        <p>Синяя пунктирная линия — смещённая ломаная R* для точки решения</p>
                        <p>Оранжевые линии — пороги пропорциональности (x=50, y=50)</p>
                        <p><strong>Зелёная звезда ⭐ — итоговое решение задачи (лежит на синей R*)</strong></p>
                    </div>
                    <div style="margin-top: 1rem; text-align: center;">
                        <button onclick="showSimpleAdGraph()" class="btn btn-secondary">
                            Показать только ломаную R
                        </button>
                    </div>
                </div>
            `;
            
            // Прокрутка к графику
            graphContainer.scrollIntoView({ behavior: 'smooth' });
        }
        
    } catch (error) {
        graphContainer.innerHTML = `
            <div class="result-error">
                <div class="result-title">✗ Ошибка</div>
                <p>${error.message}</p>
            </div>
        `;
    }
}

// Показать простой график только с ломаной R
async function showSimpleAdGraph() {
    const data = collectData();
    const graphContainer = document.getElementById('graph-container');
    
    graphContainer.innerHTML = '<div style="text-align: center; padding: 2rem;"><span class="loading"></span> Построение графика...</div>';
    
    try {
        const response = await fetch('/api/plot/ad', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.detail || 'Ошибка построения графика');
        }
        
        if (result.success) {
            graphContainer.innerHTML = `
                <div style="background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h3 style="text-align: center; margin-bottom: 1rem; color: var(--primary-color);">
                        График области достижимости Ad (ломаная R)
                    </h3>
                    <div style="text-align: center;">
                        <img src="data:image/png;base64,${result.image}" 
                             alt="График Ad" 
                             style="max-width: 100%; height: auto; border: 1px solid #e2e8f0; border-radius: 4px;">
                    </div>
                    <div style="margin-top: 1rem; text-align: center; color: var(--text-secondary); font-size: 0.9rem;">
                        <p>Ломаная R построена после сортировки делимых пунктов по убыванию a<sub>i</sub>/b<sub>i</sub></p>
                        <p>Пунктирные линии показывают структуру распределения пунктов</p>
                    </div>
                    <div style="margin-top: 1rem; text-align: center;">
                        <button onclick="showAdGraph()" class="btn btn-secondary">
                            Показать с SP-точками
                        </button>
                    </div>
                </div>
            `;
            
            graphContainer.scrollIntoView({ behavior: 'smooth' });
        }
        
    } catch (error) {
        graphContainer.innerHTML = `
            <div class="result-error">
                <div class="result-title">✗ Ошибка</div>
                <p>${error.message}</p>
            </div>
        `;
    }
}
