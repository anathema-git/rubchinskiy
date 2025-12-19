"""
Визуализация области достижимости Ad для делимых пунктов
Построение графика ломаной R согласно методичке
"""
import matplotlib
matplotlib.use('Agg')  # Для работы без GUI
import matplotlib.pyplot as plt
import io
import base64
from typing import List, Tuple


def plot_ad_region(a_d: List[float], b_d: List[float], 
                   sorted_indices: List[int] = None) -> str:
    """
    Строит график области достижимости для делимых пунктов.
    
    График показывает ломаную R - верхнюю границу области достижимости Ad,
    построенную после сортировки пунктов по убыванию a_i/b_i.
    
    Args:
        a_d: оценки участника A для делимых пунктов (исходный порядок)
        b_d: оценки участника B для делимых пунктов (исходный порядок)
        sorted_indices: индексы после сортировки (опционально)
        
    Returns:
        base64-encoded строка с PNG изображением
    """
    from .r_polygon import build_r_polygon
    from .utils import safe_divide
    
    if len(a_d) == 0:
        # Пустой график для случая L=0
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.plot([0], [0], 'ko', markersize=8)
        ax.text(0.5, 0.5, 'Нет делимых пунктов', 
                ha='center', va='center', fontsize=12)
        ax.set_xlim(-0.5, 1)
        ax.set_ylim(-0.5, 1)
        ax.set_xlabel('x (выигрыш A)', fontsize=11)
        ax.set_ylabel('y (выигрыш B)', fontsize=11)
        ax.set_aspect('equal')
        ax.grid(False)
    else:
        # Построение ломаной R
        R, sorted_idx = build_r_polygon(a_d, b_d)
        if sorted_indices is None:
            sorted_indices = sorted_idx
        
        # Создание фигуры
        fig, ax = plt.subplots(figsize=(6, 6))
        
        # Извлечение координат
        x_coords = [p[0] for p in R]
        y_coords = [p[1] for p in R]
        
        Ad = sum(a_d)
        Bd = sum(b_d)
        
        # Основная ломаная R (жирная чёрная линия)
        ax.plot(x_coords, y_coords, 'k-', linewidth=2.5, zorder=3)
        
        # Точки на ломаной (чёрные кружки)
        ax.plot(x_coords, y_coords, 'ko', markersize=8, zorder=4)
        
        # Вертикальные линии (пунктирные) для каждого сегмента
        for i in range(1, len(R)):
            x = R[i][0]
            # Линия от оси x до точки на ломаной
            ax.plot([x, x], [0, R[i][1]], 'k:', linewidth=0.8, alpha=0.5, zorder=1)
        
        # Горизонтальные линии (пунктирные) для каждого сегмента
        for i in range(1, len(R)):
            y = R[i][1]
            # Линия от оси y до точки на ломаной
            ax.plot([0, R[i][0]], [y, y], 'k:', linewidth=0.8, alpha=0.5, zorder=1)
        
        # Малые стрелки показывающие направление изменения
        # Добавляем аннотации для первых нескольких сегментов
        for i in range(min(len(R)-1, 5)):
            x1, y1 = R[i]
            x2, y2 = R[i+1]
            
            # Середина сегмента
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            
            # Вектор направления
            dx = x2 - x1
            dy = y2 - y1
            
            # Нормализация
            length = (dx**2 + dy**2)**0.5
            if length > 0:
                dx_norm = dx / length * 3
                dy_norm = dy / length * 3
                
                # Малая стрелка
                ax.arrow(mid_x - dx_norm/2, mid_y - dy_norm/2,
                        dx_norm, dy_norm,
                        head_width=2, head_length=1.5,
                        fc='gray', ec='gray', alpha=0.4, zorder=2)
        
        # Подписи значений a_i и b_i на сегментах (опционально для первых 3-4)
        for i in range(min(len(sorted_indices), 4)):
            idx = sorted_indices[i]
            x1, y1 = R[i]
            x2, y2 = R[i+1]
            
            # Подпись a_i рядом с сегментом
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            
            ai = a_d[idx]
            bi = b_d[idx]
            
            # Подпись для a_i (снизу от линии)
            offset_y = -3 if i % 2 == 0 else -5
            ax.text(mid_x, 0, f'a{idx+1}={ai:.1f}', 
                   ha='center', va='top', fontsize=8, 
                   color='darkblue', alpha=0.7)
            
            # Подпись для b_i (слева от линии)
            offset_x = -3 if i % 2 == 0 else -5
            ax.text(0, mid_y, f'b{idx+1}={bi:.1f}', 
                   ha='right', va='center', fontsize=8, 
                   color='darkred', alpha=0.7)
        
        # Настройка осей
        ax.set_xlim(-5, Ad + 10)
        ax.set_ylim(-5, Bd + 10)
        
        # Подписи осей
        ax.set_xlabel('x (выигрыш участника A)', fontsize=11, fontweight='bold')
        ax.set_ylabel('y (выигрыш участника B)', fontsize=11, fontweight='bold')
        
        # Заголовок
        ax.set_title('График области достижимости Ad\n(Ломаная R для делимых пунктов)', 
                    fontsize=12, fontweight='bold', pad=15)
        
        # Равные пропорции
        ax.set_aspect('equal', adjustable='box')
        
        # Отключение сетки
        ax.grid(False)
        
        # Тонкие серые оси
        ax.spines['bottom'].set_color('gray')
        ax.spines['left'].set_color('gray')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Добавление легенды с информацией
        legend_text = f'L = {len(a_d)}\n'
        legend_text += f'Ad = {Ad:.1f}\n'
        legend_text += f'Bd = {Bd:.1f}\n'
        legend_text += f'Сортировка: по a/b ↓'
        
        ax.text(0.98, 0.98, legend_text,
               transform=ax.transAxes,
               fontsize=9,
               verticalalignment='top',
               horizontalalignment='right',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    # Сохранение в буфер
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    
    # Конвертация в base64
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    
    plt.close(fig)
    
    return img_base64


def plot_ad_region_with_sp(a_d: List[float], b_d: List[float],
                           a_w: List[float], b_w: List[float],
                           SP: List[Tuple[float, float, List[int]]],
                           threshold: float = 50.0,
                           solution_point: Tuple[float, float] = None) -> str:
    """
    Строит график области достижимости с точками SP и линией пропорциональности.
    
    Args:
        a_d, b_d: оценки для делимых пунктов
        a_w, b_w: оценки для неделимых пунктов
        SP: Парето-множество точек
        threshold: порог пропорциональности (обычно H/2)
        solution_point: итоговое решение (GA, GB) для отображения на графике
        
    Returns:
        base64-encoded строка с PNG изображением
    """
    from .r_polygon import build_r_polygon
    from .pareto import shift_r_polygon
    
    # Построение базовой ломаной R
    R, sorted_indices = build_r_polygon(a_d, b_d)
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Основная ломаная R
    x_coords = [p[0] for p in R]
    y_coords = [p[1] for p in R]
    ax.plot(x_coords, y_coords, 'k-', linewidth=2, label='R (делимые)', zorder=2)
    ax.plot(x_coords, y_coords, 'ko', markersize=6, zorder=3)
    
    # Точки SP
    solution_sp_index = None
    if SP:
        sp_x = [p[0] for p in SP]
        sp_y = [p[1] for p in SP]
        ax.scatter(sp_x, sp_y, c='red', s=100, marker='s', 
                  label='SP (Парето-точки)', zorder=4, edgecolors='darkred', linewidth=1.5)
        
        # Если есть точка решения, найдём на какой SP она находится
        if solution_point is not None:
            sol_x, sol_y = solution_point
            # Ищем SP точку, на смещённой ломаной которой находится решение
            for i, (sp_x_val, sp_y_val, sigma) in enumerate(SP):
                R_star = shift_r_polygon(R, sp_x_val, sp_y_val)
                
                # Проверяем, лежит ли решение на этой R*
                for j in range(len(R_star) - 1):
                    x1, y1 = R_star[j]
                    x2, y2 = R_star[j+1]
                    
                    # Проверка принадлежности к отрезку или вершине
                    min_x, max_x = min(x1, x2), max(x1, x2)
                    min_y, max_y = min(y1, y2), max(y1, y2)
                    
                    # Проверяем вершины
                    if (abs(x1 - sol_x) < 0.1 and abs(y1 - sol_y) < 0.1) or \
                       (abs(x2 - sol_x) < 0.1 and abs(y2 - sol_y) < 0.1):
                        solution_sp_index = i
                        break
                    
                    # Проверяем отрезок
                    if min_x <= sol_x <= max_x and min_y <= sol_y <= max_y:
                        if abs(x2 - x1) > 0.001:
                            t = (sol_x - x1) / (x2 - x1)
                            expected_y = y1 + t * (y2 - y1)
                            if abs(expected_y - sol_y) < 0.1:
                                solution_sp_index = i
                                break
                        elif abs(y2 - y1) > 0.001:
                            t = (sol_y - y1) / (y2 - y1)
                            expected_x = x1 + t * (x2 - x1)
                            if abs(expected_x - sol_x) < 0.1:
                                solution_sp_index = i
                                break
                
                if solution_sp_index is not None:
                    break
        
        # Показываем смещённую ломаную R* для решения или первые 3
        if solution_sp_index is not None:
            # Показываем только ту R*, на которой находится решение
            x_star, y_star, sigma = SP[solution_sp_index]
            R_star = shift_r_polygon(R, x_star, y_star)
            rs_x = [p[0] for p in R_star]
            rs_y = [p[1] for p in R_star]
            ax.plot(rs_x, rs_y, '--', color='blue', 
                   linewidth=2.5, alpha=0.8, 
                   label=f'R* (решение на SP[{solution_sp_index}])', zorder=2)
        else:
            # Если решение не найдено, показываем первые 3 как раньше
            colors = ['blue', 'green', 'purple']
            for i, (x_star, y_star, sigma) in enumerate(SP[:3]):
                R_star = shift_r_polygon(R, x_star, y_star)
                rs_x = [p[0] for p in R_star]
                rs_y = [p[1] for p in R_star]
                ax.plot(rs_x, rs_y, '--', color=colors[i % len(colors)], 
                       linewidth=1.5, alpha=0.6, 
                       label=f'R* (SP_{i+1})', zorder=2)
    
    # Линия пропорциональности x = threshold
    max_y = max(max(y_coords), threshold + 20)
    ax.axvline(x=threshold, color='orange', linestyle='-.', linewidth=2, 
              label=f'x = {threshold} (пропорц.)', zorder=1, alpha=0.7)
    
    # Линия пропорциональности y = threshold
    max_x = max(max(x_coords), threshold + 20)
    ax.axhline(y=threshold, color='orange', linestyle='-.', linewidth=2, 
              label=f'y = {threshold} (пропорц.)', zorder=1, alpha=0.7)
    
    # Итоговое решение (если передано)
    if solution_point is not None:
        sol_x, sol_y = solution_point
        ax.scatter([sol_x], [sol_y], c='lime', s=300, marker='*', 
                  label=f'Решение ({sol_x:.1f}, {sol_y:.1f})', 
                  zorder=5, edgecolors='darkgreen', linewidth=2)
    
    # Настройка осей
    ax.set_xlabel('x (выигрыш участника A)', fontsize=11, fontweight='bold')
    ax.set_ylabel('y (выигрыш участника B)', fontsize=11, fontweight='bold')
    ax.set_title('График области достижимости с SP-точками\nи линиями пропорциональности', 
                fontsize=12, fontweight='bold', pad=15)
    
    ax.legend(loc='upper right', fontsize=9)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_aspect('equal', adjustable='box')
    
    # Сохранение
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    
    return img_base64
