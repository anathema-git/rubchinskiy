"""
Генерация множества S всех распределений неделимых пунктов
"""
from typing import List, Tuple


def build_s_set(a_w: List[float], b_w: List[float]) -> List[Tuple[float, float, List[int]]]:
    """
    Построение множества S всех возможных распределений неделимых пунктов
    
    Для каждой комбинации σ ∈ {0,1}^M вычисляем:
    x = sum(a_w[i] * σ[i]) - выигрыш A
    y = sum(b_w[i] * (1 - σ[i])) - выигрыш B
    
    где σ[i] = 1 означает, что пункт i получает A
          σ[i] = 0 означает, что пункт i получает B
    
    Args:
        a_w: оценки участника A для неделимых пунктов
        b_w: оценки участника B для неделимых пунктов
        
    Returns:
        Список точек [(x, y, σ), ...] где σ - список из 0 и 1
    """
    M = len(a_w)
    
    if M == 0:
        return [(0.0, 0.0, [])]
    
    S = []
    
    # Перебор всех 2^M комбинаций
    for mask in range(1 << M):  # 2^M
        x = 0.0  # выигрыш A
        y = 0.0  # выигрыш B
        sigma = []
        
        for i in range(M):
            if mask & (1 << i):
                # Пункт i получает A
                sigma.append(1)
                x += a_w[i]
            else:
                # Пункт i получает B
                sigma.append(0)
                y += b_w[i]
        
        S.append((x, y, sigma))
    
    return S
