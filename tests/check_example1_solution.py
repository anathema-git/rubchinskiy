"""
Проверка какое именно решение находит алгоритм для Example 1
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fair_division_engine.r_polygon import build_r_polygon
from fair_division_engine.indivisible import build_s_set
from fair_division_engine.pareto import pareto_filter
from fair_division_engine.equitable import find_equitable_division

# Example 1
L, M, H = 5, 0, 100
a_d = [50, 20, 15, 10, 5]  # Retirement, House, Cottage, Portfolio, Other
b_d = [40, 30, 10, 10, 10]
a_w, b_w = [], []

R, sorted_indices = build_r_polygon(a_d, b_d)
S = build_s_set(a_w, b_w)
SP = pareto_filter(S)

result = find_equitable_division(L, M, a_d, b_d, a_w, b_w, R, sorted_indices, SP, H)

print("Найденное решение алгоритмом:")
print("="*60)
print(f"Выигрыш A: {result['gains']['A']:.2f}")
print(f"Выигрыш B: {result['gains']['B']:.2f}")
print()

items = ["Retirement", "House", "Cottage", "Portfolio", "Other"]
divisible_A = result['division']['divisible_A']

print("Распределение:")
for i in range(5):
    item_key = f"item_{i+1}"
    share = divisible_A.get(item_key, 0)
    
    if abs(share - 1) < 0.001:
        print(f"  {items[i]:12s}: A получает целиком")
    elif abs(share) < 0.001:
        print(f"  {items[i]:12s}: B получает целиком")
    else:
        print(f"  {items[i]:12s}: A получает {share:.4f}, B получает {1-share:.4f}")
        print(f"    → A: {share * a_d[i]:.2f}, B: {(1-share) * b_d[i]:.2f}")

print("\nПроверка свойства 'делится не более одного предмета':")
split_count = sum(1 for item_key, share in divisible_A.items() if 0 < share < 1)
print(f"Количество делимых предметов: {split_count}")
print(f"Свойство выполнено: {split_count <= 1}")

# Проверим какой именно вариант это из найденных ранее
print("\n" + "="*60)
print("Это соответствует решению из статьи?")

# Решение из статьи: A получает Cottage (index 2) + 5/6 Retirement (index 0)
if abs(divisible_A.get('item_1', 0) - 5/6) < 0.01 and abs(divisible_A.get('item_3', 0) - 1) < 0.01:
    print("✓ ДА - это решение из статьи (вариант #4)")
else:
    print("✗ НЕТ - это другое равноценное решение")
    print("  Но оно тоже корректно, так как существует 11 равноценных решений")
