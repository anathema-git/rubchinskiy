"""
Comprehensive Fair Division Solver
Реализует Statement 1: F(S) ⊆ Q(S) ⊆ P(S) ⊆ E(S) = U(S)

Находит все типы решений:
- Efficient (E): Парето-оптимальные
- Proportional (P): GA ≥ H/2 и GB ≥ H/2
- Equitable (Q): GA = GB
- Fair (F): E ∩ P ∩ Q
"""
from typing import List, Tuple, Optional, Dict
from .pareto import pareto_filter
from .proportional import find_proportional_division
from .equitable import find_equitable_division


def _add_statement1_classification(result: Dict) -> None:
    """
    Добавляет классификацию по Statement 1: F(S) ⊆ Q(S) ⊆ P(S) ⊆ E(S) = U(S)
    
    Определяет к каким множествам принадлежит найденное решение
    """
    # Проверяем существование каждого типа
    result['efficient_exists'] = result['has_efficient']
    result['proportional_exists'] = result['has_proportional']
    result['equitable_exists'] = result['has_equitable']
    result['fair_exists'] = result['has_fair']
    
    # Определяем множества Statement 1
    statement1_sets = []
    if result['has_efficient']:
        statement1_sets.append('E(S)')
    if result['has_proportional']:
        statement1_sets.append('P(S)')
    if result['has_equitable']:
        statement1_sets.append('Q(S)')
    if result['has_fair']:
        statement1_sets.append('F(S)')
    
    result['statement1_sets'] = statement1_sets
    
    # Определяем к какому множеству принадлежит основное решение
    # Приоритет: Fair > Equitable > Proportional > Efficient
    if result['has_fair']:
        belongs_to = 'F(S) - Fair Division (Справедливый дележ)'
    elif result['has_equitable']:
        belongs_to = 'Q(S) - Equitable Division (Равноценный дележ)'
    elif result['has_proportional']:
        belongs_to = 'P(S) - Proportional Division (Пропорциональный дележ)'
    elif result['has_efficient']:
        belongs_to = 'E(S) - Efficient Division (Эффективный дележ)'
    else:
        belongs_to = 'U(S) - No Solution (Решение не найдено)'
    
    result['belongs_to_sets'] = belongs_to


def calculate_gains(a_d: List[float], b_d: List[float], 
                    a_w: List[float], b_w: List[float],
                    x: List[float], sigma: List[int]) -> Tuple[float, float]:
    """
    Вычисление выигрышей GA и GB для дележа (x, σ)
    
    Args:
        a_d, b_d: оценки делимых пунктов
        a_w, b_w: оценки неделимых пунктов
        x: доли делимых пунктов для A
        sigma: распределение неделимых (1=A, 0=B)
        
    Returns:
        (GA, GB) - выигрыши участников
    """
    L = len(a_d)
    M = len(a_w)
    
    # Выигрыш A от делимых
    ga_divisible = sum(a_d[i] * x[i] for i in range(L)) if L > 0 else 0
    # Выигрыш A от неделимых
    ga_indivisible = sum(a_w[j] * sigma[j] for j in range(M)) if M > 0 else 0
    GA = ga_divisible + ga_indivisible
    
    # Выигрыш B от делимых
    gb_divisible = sum(b_d[i] * (1 - x[i]) for i in range(L)) if L > 0 else 0
    # Выигрыш B от неделимых
    gb_indivisible = sum(b_w[j] * (1 - sigma[j]) for j in range(M)) if M > 0 else 0
    GB = gb_divisible + gb_indivisible
    
    return GA, GB


def is_efficient(a_d: List[float], b_d: List[float],
                a_w: List[float], b_w: List[float],
                x: List[float], sigma: List[int],
                all_pareto_points: List[Tuple[float, float, List[int]]]) -> bool:
    """
    Проверка эффективности (Парето-оптимальности) дележа
    
    Делёж эффективен если не существует другого дележа который строго доминирует его
    """
    # Вычисляем полные выигрыши для данного дележа
    GA, GB = calculate_gains(a_d, b_d, a_w, b_w, x, sigma)
    
    # Проверяем все точки из SP - можно ли улучшить оба выигрыша
    for sp_x, sp_y, sp_sigma in all_pareto_points:
        # Для каждой точки SP пытаемся найти распределение делимых
        # которое даст строго лучшие выигрыши
        
        # Строим смещенную R-ломаную от этой SP-точки
        L = len(a_d)
        if L == 0:
            # Только неделимые - сравниваем напрямую
            if sp_x > GA + 1e-6 and sp_y > GB + 1e-6:
                # Есть строго доминирующее распределение
                return False
            continue
        
        # Проверяем все вершины R-ломаной для этого sigma
        # Вершины R дают все возможные комбинации распределения делимых
        from .r_polygon import build_r_polygon
        R, _ = build_r_polygon(a_d, b_d)
        
        for r_a, r_b in R:
            # Полные выигрыши если использовать эту вершину R и sp_sigma
            total_A = r_a + sp_x
            total_B = r_b + sp_y
            
            # Если оба выигрыша строго больше - текущий делёж не эффективен
            if total_A > GA + 1e-6 and total_B > GB + 1e-6:
                return False
    
    return True


def is_proportional(GA: float, GB: float, H: float) -> bool:
    """Проверка пропорциональности: GA ≥ H/2 и GB ≥ H/2"""
    return GA >= H / 2 - 1e-9 and GB >= H / 2 - 1e-9


def is_equitable(GA: float, GB: float) -> bool:
    """Проверка равноценности: GA = GB"""
    return abs(GA - GB) < 1e-9


def find_all_division_types(a_d: List[float], b_d: List[float],
                            a_w: List[float], b_w: List[float],
                            H: float) -> Dict:
    """
    Полное решение задачи справедливого дележа
    Находит все типы решений: Efficient, Proportional, Equitable, Fair
    
    Returns:
        Dict с ключами:
        - has_efficient, has_proportional, has_equitable, has_fair: bool
        - efficient_division, proportional_division, equitable_division, fair_division: Optional[Tuple]
        - efficient_gains, proportional_gains, equitable_gains, fair_gains: Optional[Tuple]
        - sp_points_count: int
    """
    from .r_polygon import build_r_polygon
    from .indivisible import build_s_set
    
    L = len(a_d)
    M = len(a_w)
    
    # Построение R-polygon и S-множества
    R, sorted_indices = build_r_polygon(a_d, b_d)
    
    # Генерируем все распределения неделимых и Парето-множество
    if M > 0:
        S = build_s_set(a_w, b_w)
        SP = pareto_filter(S)
    else:
        S = [(0, 0, [])]
        SP = [(0, 0, [])]
    
    result = {
        'has_efficient': False,
        'has_proportional': False,
        'has_equitable': False,
        'has_fair': False,
        'efficient_division': None,
        'proportional_division': None,
        'equitable_division': None,
        'fair_division': None,
        'efficient_gains': None,
        'proportional_gains': None,
        'equitable_gains': None,
        'fair_gains': None,
        'sp_points_count': len(SP)
    }
    
    # 1. Сначала ищем EQUITABLE (может быть fair если эффективен и пропорционален)
    equit_result = find_equitable_division(
        L, M, a_d, b_d, a_w, b_w, R, sorted_indices, SP, H
    )
    
    if equit_result:
        # Извлекаем данные из результата
        div_data = equit_result['division']
        # Ключи могут быть 'item_X' или 'D{X}'
        first_key = list(div_data['divisible_A'].keys())[0] if div_data['divisible_A'] else None
        
        if first_key:
            x = [div_data['divisible_A'][key] for key in sorted(div_data['divisible_A'].keys())]
        else:
            x = []
        
        sigma = div_data['indivisible']
        ga = equit_result['gains']['A']
        gb = equit_result['gains']['B']
        
        result['has_equitable'] = True
        result['equitable_division'] = (x, sigma)
        result['equitable_gains'] = (ga, gb)
        
        # Проверяем пропорциональность
        if is_proportional(ga, gb, H):
            result['has_proportional'] = True
            result['proportional_division'] = (x, sigma)
            result['proportional_gains'] = (ga, gb)
        
        # Проверяем эффективность
        if is_efficient(a_d, b_d, a_w, b_w, x, sigma, SP):
            result['has_efficient'] = True
            result['efficient_division'] = (x, sigma)
            result['efficient_gains'] = (ga, gb)
            
            # Если equitable + proportional + efficient = FAIR
            if result['has_proportional']:
                result['has_fair'] = True
                result['fair_division'] = (x, sigma)
                result['fair_gains'] = (ga, gb)
                # Добавляем классификацию Statement 1 перед возвратом
                _add_statement1_classification(result)
                return result
    
    # 2. Если EQUITABLE не найден или не пропорционален, ищем PROPORTIONAL
    if not result['has_proportional']:
        prop_result = find_proportional_division(
            L, M, a_d, b_d, a_w, b_w, R, sorted_indices, SP, H
        )
        
        if prop_result:
            div_data = prop_result['division']
            first_key = list(div_data['divisible_A'].keys())[0] if div_data['divisible_A'] else None
            
            if first_key:
                x = [div_data['divisible_A'][key] for key in sorted(div_data['divisible_A'].keys())]
            else:
                x = []
            
            sigma = div_data['indivisible']
            ga = prop_result['gains']['A']
            gb = prop_result['gains']['B']
            
            result['has_proportional'] = True
            result['proportional_division'] = (x, sigma)
            result['proportional_gains'] = (ga, gb)
            
            # Проверяем эффективность
            if is_efficient(a_d, b_d, a_w, b_w, x, sigma, SP):
                result['has_efficient'] = True
                result['efficient_division'] = (x, sigma)
                result['efficient_gains'] = (ga, gb)
    
    # 3. Ищем любое EFFICIENT (E) - берём лучшую точку из SP
    if not result['has_efficient'] and len(SP) > 0:
        # Берём точку с максимальной суммой выигрышей
        best_sp = max(SP, key=lambda p: p[0] + p[1])
        x_star, y_star, sigma = best_sp
        
        # Находим оптимальное распределение делимых для этой точки
        # Используем жадный алгоритм: отдаём пункты тому, кто ценит их больше
        x = []
        for i in range(L):
            if a_d[i] >= b_d[i]:
                x.append(1.0)  # Отдаём A
            else:
                x.append(0.0)  # Отдаём B
        
        ga, gb = calculate_gains(a_d, b_d, a_w, b_w, x, sigma)
        
        result['has_efficient'] = True
        result['efficient_division'] = (x, sigma)
        result['efficient_gains'] = (ga, gb)
    
    # Добавляем классификацию Statement 1
    _add_statement1_classification(result)
    
    return result
