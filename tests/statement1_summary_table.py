"""
Итоговая таблица результатов для всех примеров из статьи
с классификацией по Statement 1: F(S) ⊆ Q(S) ⊆ P(S) ⊆ E(S) = U(S)
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fair_division_engine.r_polygon import build_r_polygon
from fair_division_engine.indivisible import build_s_set
from fair_division_engine.pareto import pareto_filter
from fair_division_engine.proportional import find_proportional_division
from fair_division_engine.equitable import find_equitable_division


def solve_fair_division(L, M, a_d, b_d, a_w, b_w, H=100):
    """Вспомогательная функция для решения задачи fair division"""
    R, sorted_indices = build_r_polygon(a_d, b_d)
    S = build_s_set(a_w, b_w)
    SP = pareto_filter(S)
    
    # Сначала пытаемся найти равноценный
    result = find_equitable_division(L, M, a_d, b_d, a_w, b_w, R, sorted_indices, SP, H)
    
    # Если не найден, ищем просто пропорциональный
    if result is None:
        result = find_proportional_division(L, M, a_d, b_d, a_w, b_w, R, sorted_indices, SP, H)
    
    return result


examples = [
    {
        "num": 1,
        "name": "Divorce Arrangement",
        "L": 5, "M": 0, "H": 100,
        "a_d": [50, 20, 15, 10, 5],
        "b_d": [40, 30, 10, 10, 10],
        "a_w": [], "b_w": []
    },
    {
        "num": 2,
        "name": "Mergers",
        "L": 1, "M": 4, "H": 100,
        "a_d": [30],
        "b_d": [10],
        "a_w": [25, 15, 20, 10],
        "b_w": [10, 20, 35, 25]
    },
    {
        "num": 3,
        "name": "No Fair Division",
        "L": 2, "M": 3, "H": 100,
        "a_d": [10, 10],
        "b_d": [30, 20],
        "a_w": [35, 30, 15],
        "b_w": [18, 20, 12]
    },
    {
        "num": 4,
        "name": "No Proportional",
        "L": 1, "M": 4, "H": 100,
        "a_d": [1],
        "b_d": [1],
        "a_w": [45, 30, 15, 9],
        "b_w": [30, 25, 22, 22]
    },
    {
        "num": 5,
        "name": "Proportional No Equitable",
        "L": 1, "M": 4, "H": 100,
        "a_d": [3],
        "b_d": [3],
        "a_w": [45, 30, 20, 2],
        "b_w": [17, 20, 22, 38]
    },
    {
        "num": 6,
        "name": "Equitable Not Efficient",
        "L": 1, "M": 4, "H": 100,
        "a_d": [5],
        "b_d": [5],
        "a_w": [40, 10, 20, 25],
        "b_w": [49, 1, 25, 20]
    },
    {
        "num": 7,
        "name": "Fair Division Exists",
        "L": 1, "M": 4, "H": 100,
        "a_d": [17],
        "b_d": [17],
        "a_w": [42, 37, 2, 2],
        "b_w": [45, 34, 2, 2]
    },
    {
        "num": 8,
        "name": "Only Indivisible",
        "L": 0, "M": 3, "H": 100,
        "a_d": [],
        "b_d": [],
        "a_w": [51, 45, 4],
        "b_w": [40, 50, 10]
    }
]


print("\n" + "="*100)
print("ИТОГОВАЯ ТАБЛИЦА РЕЗУЛЬТАТОВ")
print("Statement 1: F(S) ⊆ Q(S) ⊆ P(S) ⊆ E(S) = U(S)")
print("="*100)
print()

# Заголовок таблицы
print(f"{'№':<3} {'Название':<28} {'GA':<7} {'GB':<7} {'E(S)':<6} {'P(S)':<6} {'Q(S)':<6} {'F(S)':<6} {'Множество':<15}")
print("-" * 100)

for ex in examples:
    result = solve_fair_division(
        ex["L"], ex["M"], ex["a_d"], ex["b_d"], ex["a_w"], ex["b_w"], ex["H"]
    )
    
    if result is None:
        print(f"{ex['num']:<3} {ex['name']:<28} {'—':<7} {'—':<7} {'✗':<6} {'✗':<6} {'✗':<6} {'✗':<6} {'∅':<15}")
    else:
        ga = result["gains"]["A"]
        gb = result["gains"]["B"]
        
        if "statement1_sets" in result:
            sets = result["statement1_sets"]
            e = "✓" if sets["E"] else "✗"
            p = "✓" if sets["P"] else "✗"
            q = "✓" if sets["Q"] else "✗"
            f = "✓" if sets["F"] else "✗"
            belongs = result.get("belongs_to_sets", "—")
        else:
            e, p, q, f = "?", "?", "?", "?"
            belongs = "?"
        
        print(f"{ex['num']:<3} {ex['name']:<28} {ga:<7.2f} {gb:<7.2f} {e:<6} {p:<6} {q:<6} {f:<6} {belongs:<15}")

print("-" * 100)
print()

# Легенда
print("ЛЕГЕНДА:")
print("  E(S) - Efficient:     Парето-оптимальное решение")
print("  P(S) - Proportional:  GA ≥ H/2 и GB ≥ H/2 (каждый получает не менее половины)")
print("  Q(S) - Equitable:     GA = GB (равноценное)")
print("  F(S) - Fair:          E ∩ P ∩ Q (справедливое = эффективное ∩ пропорциональное ∩ равноценное)")
print()

# Диаграмма Эйлера (текстовая)
print("ДИАГРАММА ЭЙЛЕРА (Statement 1):")
print()
print("  ┌─────────────────────────────────────────────┐")
print("  │ U(S) - Универсум (все задачи)              │")
print("  │  ┌──────────────────────────────────────┐   │")
print("  │  │ E(S) - Efficient (Парето-оптимальные)│   │")
print("  │  │  ┌────────────────────────────────┐  │   │")
print("  │  │  │ P(S) - Proportional            │  │   │")
print("  │  │  │  ┌──────────────────────────┐  │  │   │")
print("  │  │  │  │ Q(S) - Equitable         │  │  │   │")
print("  │  │  │  │  ┌────────────────────┐  │  │  │   │")
print("  │  │  │  │  │ F(S) - Fair        │  │  │  │   │")
print("  │  │  │  │  │ (E ∩ P ∩ Q)        │  │  │  │   │")
print("  │  │  │  │  └────────────────────┘  │  │  │   │")
print("  │  │  │  └──────────────────────────┘  │  │   │")
print("  │  │  └────────────────────────────────┘  │   │")
print("  │  └──────────────────────────────────────┘   │")
print("  └─────────────────────────────────────────────┘")
print()

# Статистика
print("СТАТИСТИКА:")
total = len(examples)
no_solution = sum(1 for ex in examples if solve_fair_division(ex["L"], ex["M"], ex["a_d"], ex["b_d"], ex["a_w"], ex["b_w"], ex["H"]) is None)
has_solution = total - no_solution

results_with_sets = []
for ex in examples:
    result = solve_fair_division(ex["L"], ex["M"], ex["a_d"], ex["b_d"], ex["a_w"], ex["b_w"], ex["H"])
    if result and "statement1_sets" in result:
        results_with_sets.append(result["statement1_sets"])

if results_with_sets:
    efficient_count = sum(1 for s in results_with_sets if s["E"])
    proportional_count = sum(1 for s in results_with_sets if s["P"])
    equitable_count = sum(1 for s in results_with_sets if s["Q"])
    fair_count = sum(1 for s in results_with_sets if s["F"])
    
    print(f"  Всего примеров: {total}")
    print(f"  Решений найдено: {has_solution}")
    print(f"  Решений не найдено: {no_solution}")
    print()
    print(f"  E(S) - Efficient: {efficient_count}/{has_solution}")
    print(f"  P(S) - Proportional: {proportional_count}/{has_solution}")
    print(f"  Q(S) - Equitable: {equitable_count}/{has_solution}")
    print(f"  F(S) - Fair: {fair_count}/{has_solution}")
    print()
    print(f"  Доля Fair среди найденных: {fair_count}/{has_solution} = {fair_count/has_solution*100:.1f}%")

print()
print("="*100)
