"""
Поиск равноценного дележа (equitable division)
Алгоритм AW (Adjusted Winner) из статьи
"""
from typing import List, Tuple, Optional, Dict, Any
from .utils import safe_divide


def _add_statement1_classification(result: Dict[str, Any]) -> None:
    """
    Добавляет классификацию по Statement 1: F(S) ⊆ Q(S) ⊆ P(S) ⊆ E(S) = U(S)
    
    - E(S): Efficient - Парето-оптимальные (efficient_exists)
    - P(S): Proportional - GA ≥ H/2 и GB ≥ H/2
    - Q(S): Equitable - GA = GB
    - F(S): Fair - E ∩ P ∩ Q
    """
    ga = result["gains"]["A"]
    gb = result["gains"]["B"]
    
    # Всегда True для найденного решения (из SP)
    result["efficient_exists"] = True
    
    # Проверка пропорциональности
    result["proportional_exists"] = result.get("proportional_exists", False)
    
    # Проверка равноценности
    result["equitable_exists"] = result.get("equitable_exists", False)
    
    # Fair = Efficient ∩ Proportional ∩ Equitable
    result["fair_exists"] = (
        result["efficient_exists"] and 
        result["proportional_exists"] and 
        result["equitable_exists"]
    )
    
    # Добавляем информацию о множествах
    result["statement1_sets"] = {
        "E": result["efficient_exists"],      # Efficient (Парето-оптимальный)
        "P": result["proportional_exists"],   # Proportional (GA ≥ H/2, GB ≥ H/2)
        "Q": result["equitable_exists"],      # Equitable (GA = GB)
        "F": result["fair_exists"]            # Fair (E ∩ P ∩ Q)
    }
    
    # Текстовое описание
    sets_list = []
    if result["fair_exists"]:
        sets_list.append("F(S)")  # Fair включает все остальные
    if result["equitable_exists"] and not result["fair_exists"]:
        sets_list.append("Q(S)")  # Equitable но не Fair
    if result["proportional_exists"] and not result["equitable_exists"]:
        sets_list.append("P(S)")  # Proportional но не Equitable
    if result["efficient_exists"] and not result["proportional_exists"]:
        sets_list.append("E(S)")  # Efficient но не Proportional
    
    result["belongs_to_sets"] = " ⊆ ".join(sets_list) if sets_list else "U(S) only"


def find_equitable_division(L: int, M: int,
                            a_d: List[float], b_d: List[float],
                            a_w: List[float], b_w: List[float],
                            R: List[Tuple[float, float]],
                            sorted_indices: List[int],
                            SP: List[Tuple[float, float, List[int]]],
                            H: float = 100.0) -> Optional[Dict[str, Any]]:
    """
    Поиск равноценного дележа (где выигрыши A и B равны)
    
    Алгоритм:
    1. Для каждой точки (x*, y*, σ) из Парето-множества SP
    2. Строим смещённую ломаную R* = R + (x*, y*)
    3. Ищем пересечение R* с диагональю u = v
    4. Выбираем делёж с максимальным общим выигрышем
    
    Args:
        L: количество делимых пунктов
        M: количество неделимых пунктов
        a_d: оценки A для делимых
        b_d: оценки B для делимых
        a_w: оценки A для неделимых
        b_w: оценки B для неделимых
        R: ломаная для делимых
        sorted_indices: индексы отсортированных делимых
        SP: Парето-множество
        H: сумма оценок
        
    Returns:
        Словарь с результатом или None
    """
    from .pareto import shift_r_polygon
    
    best_result = None
    max_gain = 0.0
    
    # Перебираем все точки Парето-множества
    for x_star, y_star, sigma in SP:
        # Строим смещённую ломаную R*
        R_star = shift_r_polygon(R, x_star, y_star)
        
        # Проверяем вершины на равенство u = v
        for i, (u, v) in enumerate(R_star):
            diff = abs(u - v)
            if diff < 0.01:  # Практически равны
                gain = (u + v) / 2.0
                # Equitable не требует пропорциональности, только GA = GB
                if gain > max_gain:
                    max_gain = gain
                    best_result = build_equitable_division_from_vertex(
                        i, sigma, L, M, a_d, b_d, a_w, b_w,
                        sorted_indices, x_star, y_star, gain
                    )
                    best_result['method'] = 'vertex_equitable'
                    # Проверяем пропорциональность отдельно
                    best_result['proportional_exists'] = (gain >= H / 2.0)
        
        # Проверяем отрезки на пересечение с диагональю u = v
        for k in range(len(R_star) - 1):
            p1 = R_star[k]
            p2 = R_star[k + 1]
            
            intersection = find_diagonal_intersection(p1, p2)
            
            if intersection is not None:
                u_eq, v_eq = intersection
                gain = (u_eq + v_eq) / 2.0
                
                # Equitable требует только GA = GB, пропорциональность проверяется отдельно
                if gain > max_gain:
                    max_gain = gain
                    best_result = build_equitable_division_from_segment(
                        k, sigma, L, M, a_d, b_d, a_w, b_w,
                        sorted_indices, x_star, y_star, p1, p2, intersection
                    )
                    best_result['method'] = 'segment_equitable'
                    best_result['equitable'] = True
                    # Проверяем пропорциональность отдельно
                    best_result['proportional_exists'] = (gain >= H / 2.0)
    
    return best_result


def find_diagonal_intersection(p1: Tuple[float, float],
                               p2: Tuple[float, float]) -> Optional[Tuple[float, float]]:
    """
    Находит пересечение отрезка с диагональю u = v
    
    Отрезок задан точками p1=(u1,v1) и p2=(u2,v2)
    Диагональ: v = u
    
    Args:
        p1: первая точка отрезка
        p2: вторая точка отрезка
        
    Returns:
        Точка пересечения (u, v) или None
    """
    u1, v1 = p1
    u2, v2 = p2
    
    # Параметрическое уравнение отрезка:
    # u(t) = u1 + t*(u2-u1)
    # v(t) = v1 + t*(v2-v1)
    # где t ∈ [0, 1]
    
    # Пересечение с v = u:
    # v1 + t*(v2-v1) = u1 + t*(u2-u1)
    # v1 - u1 = t*(u2-u1) - t*(v2-v1)
    # v1 - u1 = t*((u2-u1) - (v2-v1))
    # t = (v1 - u1) / ((u2-u1) - (v2-v1))
    
    denominator = (u2 - u1) - (v2 - v1)
    
    if abs(denominator) < 1e-10:
        # Отрезок параллелен диагонали
        # Проверяем, лежит ли на диагонали
        if abs(v1 - u1) < 1e-10:
            return p1  # Весь отрезок на диагонали
        return None
    
    t = (v1 - u1) / denominator
    
    # Проверяем, что t ∈ [0, 1] (пересечение внутри отрезка)
    if 0 <= t <= 1:
        u = u1 + t * (u2 - u1)
        v = v1 + t * (v2 - v1)
        return (u, v)
    
    return None


def build_equitable_division_from_vertex(vertex_idx: int, sigma: List[int],
                                        L: int, M: int,
                                        a_d: List[float], b_d: List[float],
                                        a_w: List[float], b_w: List[float],
                                        sorted_indices: List[int],
                                        x_star: float, y_star: float,
                                        gain: float) -> Dict[str, Any]:
    """
    Построение равноценного дележа из вершины
    """
    divisible_to_A = {}
    divisible_to_B = {}
    
    for i in range(L):
        original_idx = sorted_indices[i]
        if i < vertex_idx:
            divisible_to_A[f"item_{original_idx+1}"] = 1.0
            divisible_to_B[f"item_{original_idx+1}"] = 0.0
        else:
            divisible_to_A[f"item_{original_idx+1}"] = 0.0
            divisible_to_B[f"item_{original_idx+1}"] = 1.0
    
    result = {
        "proportional_exists": True,
        "equitable_exists": True,
        "division": {
            "divisible_A": divisible_to_A,
            "divisible_B": divisible_to_B,
            "indivisible": sigma
        },
        "gains": {
            "A": round(gain, 2),
            "B": round(gain, 2)
        },
        "vertex_index": vertex_idx,
        "sp_point": {
            "x": round(x_star, 2),
            "y": round(y_star, 2)
        }
    }
    
    # Добавляем классификацию по множествам Statement 1
    _add_statement1_classification(result)
    return result


def build_equitable_division_from_segment(segment_idx: int, sigma: List[int],
                                         L: int, M: int,
                                         a_d: List[float], b_d: List[float],
                                         a_w: List[float], b_w: List[float],
                                         sorted_indices: List[int],
                                         x_star: float, y_star: float,
                                         p1: Tuple[float, float], p2: Tuple[float, float],
                                         intersection: Tuple[float, float]) -> Dict[str, Any]:
    """
    Построение равноценного дележа из пересечения отрезка с диагональю
    """
    u_eq, v_eq = intersection
    
    divisible_to_A = {}
    divisible_to_B = {}
    
    # Находим долю делимого пункта segment_idx для A
    original_idx = sorted_indices[segment_idx]
    a_item = a_d[original_idx]
    b_item = b_d[original_idx]
    
    # p1[0] + α * a_item = u_eq
    alpha = safe_divide(u_eq - p1[0], a_item, 0.0)
    alpha = max(0.0, min(1.0, alpha))
    
    for i in range(L):
        original_idx = sorted_indices[i]
        if i < segment_idx:
            divisible_to_A[f"item_{original_idx+1}"] = 1.0
            divisible_to_B[f"item_{original_idx+1}"] = 0.0
        elif i == segment_idx:
            divisible_to_A[f"item_{original_idx+1}"] = round(alpha, 6)
            divisible_to_B[f"item_{original_idx+1}"] = round(1.0 - alpha, 6)
        else:
            divisible_to_A[f"item_{original_idx+1}"] = 0.0
            divisible_to_B[f"item_{original_idx+1}"] = 1.0
    
    # Вычисляем точные выигрыши
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
    
    result = {
        "proportional_exists": True,
        "equitable_exists": True,
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
        "split_fraction": round(alpha, 6),
        "sp_point": {
            "x": round(x_star, 2),
            "y": round(y_star, 2)
        },
        "intersection_point": {
            "x": round(u_eq, 2),
            "y": round(v_eq, 2)
        }
    }
    
    # Добавляем классификацию по множествам Statement 1
    _add_statement1_classification(result)
    return result
