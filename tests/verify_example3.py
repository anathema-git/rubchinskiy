"""
Проверка Example 3 детально - есть ли он действительно Fair или нет
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fair_division_engine.r_polygon import build_r_polygon
from fair_division_engine.indivisible import build_s_set
from fair_division_engine.pareto import pareto_filter
from fair_division_engine.equitable import find_equitable_division

# Example 3
L, M, H = 2, 3, 100
a_d = [10, 10]
b_d = [30, 20]
a_w = [35, 30, 15]
b_w = [18, 20, 12]

print("Example 3: No Fair Division (из статьи)")
print("="*60)
print("\nОценки:")
print("Делимые:")
print(f"  Item 1: A={a_d[0]}, B={b_d[0]}")
print(f"  Item 2: A={a_d[1]}, B={b_d[1]}")
print("\nНеделимые:")
print(f"  Item 3: A={a_w[0]}, B={b_w[0]}")
print(f"  Item 4: A={a_w[1]}, B={b_w[1]}")
print(f"  Item 5: A={a_w[2]}, B={b_w[2]}")

# Строим S и SP
S = build_s_set(a_w, b_w)
SP = pareto_filter(S)

print(f"\n{'='*60}")
print(f"S-множество (все распределения неделимых): {len(S)} точек")
print(f"SP (Парето-множество): {len(SP)} точек")
print()

print("Парето-оптимальные точки:")
for i, (x_star, y_star, sigma) in enumerate(SP, 1):
    print(f"{i}. σ={sigma}, x*={x_star}, y*={y_star}")
    print(f"   A получает:", end="")
    for j in range(3):
        if sigma[j] == 1:
            print(f" item{j+3}", end="")
    print(f" → A={x_star}, B={y_star}")

# Находим решение
R, sorted_indices = build_r_polygon(a_d, b_d)
result = find_equitable_division(L, M, a_d, b_d, a_w, b_w, R, sorted_indices, SP, H)

print(f"\n{'='*60}")
if result:
    print("Найденное решение:")
    print(f"  GA = {result['gains']['A']:.2f}")
    print(f"  GB = {result['gains']['B']:.2f}")
    print(f"  σ = {result['division']['indivisible']}")
    
    if "sp_point" in result:
        print(f"  Используемая точка SP: ({result['sp_point']['x']}, {result['sp_point']['y']})")
    
    if "statement1_sets" in result:
        sets = result["statement1_sets"]
        print(f"\n  E(S): {sets['E']}")
        print(f"  P(S): {sets['P']}")
        print(f"  Q(S): {sets['Q']}")
        print(f"  F(S): {sets['F']}")
else:
    print("Решение не найдено")

# Проверим вручную - в статье говорится о точке (65, 62)
print(f"\n{'='*60}")
print("Проверка из статьи:")
print("Утверждается, что есть делёж (65, 62), доминирующий равноценный (56.67, 56.67)")
print()

# Проверяем все возможные дележи
from itertools import product

best_efficient = []
for sigma in product([0, 1], repeat=3):
    sigma_list = list(sigma)
    # Выигрыш от неделимых
    ga_ind = sum(a_w[j] * sigma[j] for j in range(3))
    gb_ind = sum(b_w[j] * (1-sigma[j]) for j in range(3))
    
    # Максимальный выигрыш от делимых (жадно)
    # A получает всё где оценивает больше
    ga_max = ga_ind + sum(a_d)  # Максимум если A получает всё
    gb_max = gb_ind + sum(b_d)  # Максимум если B получает всё
    
    # Проверяем, является ли эта точка SP парето-оптимальной
    is_pareto = any(
        abs(sp_x - ga_ind) < 0.01 and abs(sp_y - gb_ind) < 0.01
        for sp_x, sp_y, _ in SP
    )
    
    if is_pareto:
        # Оптимальное распределение делимых для максимизации суммы
        total_max = ga_ind + gb_ind + sum(a_d) + sum(b_d)
        best_efficient.append((sigma_list, ga_ind, gb_ind, total_max))

print(f"Найдено {len(best_efficient)} эффективных базовых распределений неделимых")
for sigma, ga_ind, gb_ind, total in best_efficient:
    print(f"  σ={sigma}: от неделимых A={ga_ind}, B={gb_ind}")
    # Добавляем делимые оптимально
    if a_d[0] >= b_d[0]:  # Item 1: 10 vs 30 - отдаём B
        ga_d = 0
        gb_d = b_d[0]
    else:
        ga_d = a_d[0]
        gb_d = 0
    
    if a_d[1] >= b_d[1]:  # Item 2: 10 vs 20 - отдаём B
        ga_d += 0
        gb_d += b_d[1]
    else:
        ga_d += a_d[1]
        gb_d += 0
    
    print(f"    + оптимальные делимые: A+={ga_d}, B+={gb_d}")
    print(f"    = Итого: ({ga_ind + ga_d}, {gb_ind + gb_d})")
