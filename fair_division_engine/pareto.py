"""
Выделение Парето-множества SP из множества S
Алгоритм из методички
"""
from typing import List, Tuple


def pareto_filter(S: List[Tuple[float, float, List[int]]]) -> List[Tuple[float, float, List[int]]]:
    """
    Выделение Парето-множества SP
    
    Алгоритм из методички:
    1. Сортируем S по убыванию x
    2. Добавляем первую точку S₀ в SP
    3. Для остальных точек: если y > предыдущего y в SP, то точка является Парето-точкой
    
    Точка (x, y) является Парето-оптимальной, если не существует другой точки (x', y'),
    где x' ≥ x и y' ≥ y, причём хотя бы одно неравенство строгое.
    
    Args:
        S: множество всех распределений неделимых пунктов
        
    Returns:
        Парето-множество SP ⊆ S
    """
    if not S:
        return []
    
    # Шаг 1: Сортировка по убыванию x (затем по убыванию y для стабильности)
    sorted_S = sorted(S, key=lambda p: (p[0], p[1]), reverse=True)
    
    # Шаг 2: Первая точка всегда в SP (максимальный x)
    SP = [sorted_S[0]]
    max_y = sorted_S[0][1]
    
    # Шаг 3: Проход по остальным точкам
    for i in range(1, len(sorted_S)):
        x, y, sigma = sorted_S[i]
        
        # Если y больше максимального y среди уже добавленных в SP,
        # то это Парето-точка
        if y > max_y:
            SP.append((x, y, sigma))
            max_y = y
    
    return SP


def shift_r_polygon(R: List[Tuple[float, float]], x_star: float, y_star: float) -> List[Tuple[float, float]]:
    """
    Построение смещённой ломаной R*
    
    R* = R + (x*, y*) где (x*, y*) - точка из SP
    
    Формула (6) из методички:
    R*_i = (x* + u_i, y* + v_i) для каждой точки (u_i, v_i) из R
    
    Args:
        R: исходная ломаная для делимых пунктов
        x_star: смещение по x (выигрыш A от неделимых)
        y_star: смещение по y (выигрыш B от неделимых)
        
    Returns:
        Смещённая ломаная R*
    """
    return [(x + x_star, y + y_star) for x, y in R]
