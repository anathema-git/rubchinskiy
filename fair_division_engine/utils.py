"""
Вспомогательные функции для fair_division_engine
"""
from typing import List, Tuple


def validate_input(L: int, M: int, a_d: List[float], b_d: List[float], 
                   a_w: List[float], b_w: List[float], H: float = 100.0) -> None:
    """
    Проверка корректности входных данных
    
    Args:
        L: количество делимых пунктов
        M: количество неделимых пунктов
        a_d: оценки A для делимых пунктов
        b_d: оценки B для делимых пунктов
        a_w: оценки A для неделимых пунктов
        b_w: оценки B для неделимых пунктов
        H: сумма всех оценок (обычно 100)
        
    Raises:
        ValueError: если данные некорректны
    """
    if L < 0 or M < 0:
        raise ValueError("L и M должны быть неотрицательными")
    
    if len(a_d) != L:
        raise ValueError(f"Длина a_d должна быть равна L={L}")
    
    if len(b_d) != L:
        raise ValueError(f"Длина b_d должна быть равна L={L}")
    
    if len(a_w) != M:
        raise ValueError(f"Длина a_w должна быть равна M={M}")
    
    if len(b_w) != M:
        raise ValueError(f"Длина b_w должна быть равна M={M}")
    
    # Проверка неотрицательности
    if any(x < 0 for x in a_d + b_d + a_w + b_w):
        raise ValueError("Все оценки должны быть неотрицательными")
    
    # Проверка сумм (с допуском на погрешность)
    sum_a = sum(a_d) + sum(a_w)
    sum_b = sum(b_d) + sum(b_w)
    
    epsilon = 0.01
    if abs(sum_a - H) > epsilon:
        raise ValueError(f"Сумма оценок A должна быть равна H={H}, получено {sum_a}")
    
    if abs(sum_b - H) > epsilon:
        raise ValueError(f"Сумма оценок B должна быть равна H={H}, получено {sum_b}")


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Безопасное деление с защитой от деления на 0
    
    Args:
        numerator: числитель
        denominator: знаменатель
        default: значение по умолчанию при делении на 0
        
    Returns:
        результат деления или default
    """
    if abs(denominator) < 1e-10:
        return default
    return numerator / denominator
