"""
Проверка пропорциональности и поиск справедливого дележа
Реализует алгоритмы из секции 4 методички
"""
from typing import List, Tuple, Optional, Dict, Any
from .utils import safe_divide


def check_vertex_proportionality(R_star: List[Tuple[float, float]], 
                                  threshold: float = 50.0) -> Optional[int]:
    """
    Проверка условий пропорциональности в вершинах (8a, 8b)
    
    Проверяем для каждой точки (u_i, v_i) из R*:
        u_i ≥ threshold (обычно H/2 = 50)
        v_i ≥ threshold
    
    Args:
        R_star: смещённая ломаная
        threshold: порог пропорциональности (H/2)
        
    Returns:
        индекс i вершины, где выполняется условие, или None
    """
    for i, (u, v) in enumerate(R_star):
        if u >= threshold and v >= threshold:
            return i
    return None


def check_segment_proportionality(p1: Tuple[float, float], 
                                   p2: Tuple[float, float], 
                                   threshold: float = 50.0) -> Optional[Tuple[float, float]]:
    """
    Геометрическая проверка пропорциональности на отрезке
    
    Проверяем пересечение отрезка с вертикалью x = threshold или горизонталью y = threshold
    Используем формулы (10)-(11) из методички:
    
    Уравнение прямой через две точки:
        y = kx + b
        k = (y2 - y1) / (x2 - x1)
        b = y1 - k*x1
    
    Подставляем x = threshold и проверяем, что y ≥ threshold
    
    Args:
        p1: первая точка отрезка (x1, y1)
        p2: вторая точка отрезка (x2, y2)
        threshold: порог пропорциональности (H/2)
        
    Returns:
        точка пересечения (x, y) если найдена, иначе None
    """
    x1, y1 = p1
    x2, y2 = p2
    
    # Проверяем, пересекает ли отрезок вертикаль x = threshold
    if (x1 <= threshold <= x2) or (x2 <= threshold <= x1):
        # Вычисляем наклон k
        k = safe_divide(y2 - y1, x2 - x1, 0.0)
        
        # y = kx + b, где b = y1 - k*x1
        b = y1 - k * x1
        
        # Подставляем x = threshold
        y_at_threshold = k * threshold + b
        
        # Проверяем условие Q = y ≥ threshold
        if y_at_threshold >= threshold:
            return (threshold, y_at_threshold)
    
    return None


def find_proportional_division(L: int, M: int, 
                               a_d: List[float], b_d: List[float],
                               a_w: List[float], b_w: List[float],
                               R: List[Tuple[float, float]],
                               sorted_indices: List[int],
                               SP: List[Tuple[float, float, List[int]]],
                               H: float = 100.0) -> Optional[Dict[str, Any]]:
    """
    Главный алгоритм поиска пропорционального дележа
    
    Псевдокод (раздел 8 ТЗ):
        для каждой точки (x*, y*, σ) из SP:
            построить R* = R + (x*, y*)
            проверить вершины: если u_i ≥ H/2 и v_i ≥ H/2 → найден делёж
            проверить отрезки: если отрезок пересекает x=H/2 при y≥H/2 → найден делёж
        если не найдено → вернуть None
    
    Args:
        L: количество делимых пунктов
        M: количество неделимых пунктов
        a_d: оценки A для делимых пунктов
        b_d: оценки B для делимых пунктов
        a_w: оценки A для неделимых пунктов
        b_w: оценки B для неделимых пунктов
        R: ломаная для делимых пунктов
        sorted_indices: индексы отсортированных делимых пунктов
        SP: Парето-множество
        H: сумма оценок (обычно 100)
        
    Returns:
        Словарь с результатами дележа или None если пропорциональный делёж не существует
    """
    from .pareto import shift_r_polygon
    
    threshold = H / 2.0
    
    # Перебираем все точки Парето-множества
    for x_star, y_star, sigma in SP:
        # Строим смещённую ломаную R*
        R_star = shift_r_polygon(R, x_star, y_star)
        
        # Проверка вершин (условия 8a, 8b)
        vertex_idx = check_vertex_proportionality(R_star, threshold)
        
        if vertex_idx is not None:
            # Найден пропорциональный делёж в вершине
            division = build_division_from_vertex(
                vertex_idx, sigma, L, M, a_d, b_d, a_w, b_w, 
                sorted_indices, x_star, y_star
            )
            division['method'] = 'vertex'
            return division
        
        # Проверка отрезков (геометрическая проверка)
        for k in range(len(R_star) - 1):
            p1 = R_star[k]
            p2 = R_star[k + 1]
            
            intersection = check_segment_proportionality(p1, p2, threshold)
            
            if intersection is not None:
                # Найден пропорциональный делёж на отрезке
                division = build_division_from_segment(
                    k, sigma, L, M, a_d, b_d, a_w, b_w,
                    sorted_indices, x_star, y_star, p1, p2, intersection
                )
                division['method'] = 'segment intersection'
                return division
    
    # Пропорциональный делёж не найден
    return None


def build_division_from_vertex(vertex_idx: int, sigma: List[int],
                               L: int, M: int,
                               a_d: List[float], b_d: List[float],
                               a_w: List[float], b_w: List[float],
                               sorted_indices: List[int],
                               x_star: float, y_star: float) -> Dict[str, Any]:
    """
    Построение результата дележа из вершины ломаной R*
    
    Участник A получает:
        - первые vertex_idx делимых пунктов (после сортировки)
        - все неделимые пункты где σ[i] = 1
    
    Args:
        vertex_idx: индекс вершины в R*
        sigma: распределение неделимых пунктов
        остальные параметры: данные задачи
        
    Returns:
        словарь с полным описанием дележа
    """
    # Распределение делимых пунктов
    divisible_to_A = {}
    divisible_to_B = {}
    
    for i in range(L):
        original_idx = sorted_indices[i]
        if i < vertex_idx:
            # Пункт полностью к A
            divisible_to_A[f"item_{original_idx+1}"] = 1.0
            divisible_to_B[f"item_{original_idx+1}"] = 0.0
        else:
            # Пункт полностью к B
            divisible_to_A[f"item_{original_idx+1}"] = 0.0
            divisible_to_B[f"item_{original_idx+1}"] = 1.0
    
    # Вычисляем выигрыши
    gain_A = x_star  # от неделимых
    gain_B = y_star  # от неделимых
    
    for i in range(vertex_idx):
        original_idx = sorted_indices[i]
        gain_A += a_d[original_idx]
        
    for i in range(vertex_idx, L):
        original_idx = sorted_indices[i]
        gain_B += b_d[original_idx]
    
    return {
        "proportional_exists": True,
        "division": {
            "divisible_A": divisible_to_A,
            "divisible_B": divisible_to_B,
            "indivisible": sigma
        },
        "gains": {
            "A": round(gain_A, 2),
            "B": round(gain_B, 2)
        },
        "vertex_index": vertex_idx,
        "sp_point": {
            "x": round(x_star, 2),
            "y": round(y_star, 2)
        }
    }


def build_division_from_segment(segment_idx: int, sigma: List[int],
                                L: int, M: int,
                                a_d: List[float], b_d: List[float],
                                a_w: List[float], b_w: List[float],
                                sorted_indices: List[int],
                                x_star: float, y_star: float,
                                p1: Tuple[float, float], p2: Tuple[float, float],
                                intersection: Tuple[float, float]) -> Dict[str, Any]:
    """
    Построение результата дележа из пересечения отрезка с линией пропорциональности
    
    На отрезке между двумя вершинами один делимый пункт делится между участниками.
    
    Args:
        segment_idx: индекс начала отрезка
        sigma: распределение неделимых пунктов
        p1, p2: концы отрезка в R*
        intersection: точка пересечения (threshold, y)
        остальные параметры: данные задачи
        
    Returns:
        словарь с полным описанием дележа
    """
    threshold, y_intersection = intersection
    
    # Участник A получает первые segment_idx пунктов полностью
    # Пункт segment_idx делится
    # Остальные пункты полностью к B
    
    divisible_to_A = {}
    divisible_to_B = {}
    
    # Вычисляем долю делимого пункта segment_idx для A
    # p1 соответствует состоянию после передачи segment_idx пунктов к A
    # p2 соответствует состоянию после передачи segment_idx+1 пунктов к A
    
    # x_star + sum(a_d[sorted_indices[0..segment_idx-1]]) = p1[0]
    # x_star + sum(a_d[sorted_indices[0..segment_idx]]) = p2[0]
    
    # На пересечении: x = threshold
    # Находим долю α пункта segment_idx, которую получает A
    
    original_idx = sorted_indices[segment_idx]
    a_item = a_d[original_idx]
    b_item = b_d[original_idx]
    
    # p1[0] + α * a_item = threshold
    alpha = safe_divide(threshold - p1[0], a_item, 0.0)
    alpha = max(0.0, min(1.0, alpha))  # Ограничиваем [0, 1]
    
    for i in range(L):
        original_idx = sorted_indices[i]
        if i < segment_idx:
            divisible_to_A[f"item_{original_idx+1}"] = 1.0
            divisible_to_B[f"item_{original_idx+1}"] = 0.0
        elif i == segment_idx:
            divisible_to_A[f"item_{original_idx+1}"] = round(alpha, 4)
            divisible_to_B[f"item_{original_idx+1}"] = round(1.0 - alpha, 4)
        else:
            divisible_to_A[f"item_{original_idx+1}"] = 0.0
            divisible_to_B[f"item_{original_idx+1}"] = 1.0
    
    # Вычисляем выигрыши
    gain_A = x_star
    gain_B = y_star
    
    for i in range(L):
        original_idx = sorted_indices[i]
        if i < segment_idx:
            gain_A += a_d[original_idx]
        elif i == segment_idx:
            gain_A += a_d[original_idx] * alpha
            gain_B += b_d[original_idx] * (1.0 - alpha)
        else:
            gain_B += b_d[original_idx]
    
    return {
        "proportional_exists": True,
        "division": {
            "divisible_A": divisible_to_A,
            "divisible_B": divisible_to_B,
            "indivisible": sigma
        },
        "gains": {
            "A": round(gain_A, 2),
            "B": round(gain_B, 2)
        },
        "segment_index": segment_idx,
        "split_fraction": round(alpha, 4),
        "sp_point": {
            "x": round(x_star, 2),
            "y": round(y_star, 2)
        },
        "intersection_point": {
            "x": round(intersection[0], 2),
            "y": round(intersection[1], 2)
        }
    }
