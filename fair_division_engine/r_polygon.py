"""
Построение ломаной R (Ad - attainable set for divisible items)
Соответствует формулам (1)-(4) из методички
"""
from typing import List, Tuple
from .utils import safe_divide


def build_r_polygon(a_d: List[float], b_d: List[float]) -> Tuple[List[Tuple[float, float]], List[int]]:
    """
    Построение ломаной R для делимых пунктов
    
    Алгоритм:
    1. Сортировка делимых пунктов по убыванию a_i / b_i (формула (1))
    2. Построение ломаной от (0, Bd) до (Ad, 0) согласно формулам (3)-(4)
    
    Args:
        a_d: оценки участника A для делимых пунктов
        b_d: оценки участника B для делимых пунктов
        
    Returns:
        Tuple[List[Tuple[float, float]], List[int]]:
            - список точек ломаной [(u0, v0), (u1, v1), ..., (uL, vL)]
            - индексы отсортированных пунктов
    """
    L = len(a_d)
    
    if L == 0:
        return [(0.0, 0.0)], []
    
    # Создаём список (индекс, a_i, b_i, ratio)
    items = []
    for i in range(L):
        ratio = safe_divide(a_d[i], b_d[i], float('inf'))
        items.append((i, a_d[i], b_d[i], ratio))
    
    # Сортировка по убыванию a_i / b_i (формула (1))
    # При равенстве ratio сортируем по убыванию a_i для стабильности
    items.sort(key=lambda x: (x[3], x[1]), reverse=True)
    
    # Вычисляем Ad и Bd
    Ad = sum(a_d)
    Bd = sum(b_d)
    
    # Строим ломаную R
    # Начальная точка (0, Bd) - участник A получает 0, участник B получает всё
    polygon = [(0.0, Bd)]
    
    curr_x = 0.0
    curr_y = Bd
    
    sorted_indices = []
    
    for idx, ai, bi, _ in items:
        sorted_indices.append(idx)
        # Добавляем пункт к участнику A
        curr_x += ai  # A получает ai
        curr_y -= bi  # B теряет bi
        polygon.append((curr_x, curr_y))
    
    return polygon, sorted_indices


def check_r_monotonicity(polygon: List[Tuple[float, float]]) -> bool:
    """
    Проверка строгой монотонности ломаной R
    
    R должна быть строго возрастающей по x и убывающей по y
    
    Args:
        polygon: ломаная R
        
    Returns:
        True если ломаная строго монотонна
    """
    if len(polygon) < 2:
        return True
    
    for i in range(1, len(polygon)):
        x_prev, y_prev = polygon[i-1]
        x_curr, y_curr = polygon[i]
        
        # x должен строго возрастать, y должен убывать (или оставаться равным)
        if x_curr <= x_prev:
            return False
        if y_curr > y_prev:
            return False
    
    return True
