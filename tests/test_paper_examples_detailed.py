"""
Детальные тесты примеров из статьи с выводом результатов
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fair_division_engine.r_polygon import build_r_polygon
from fair_division_engine.indivisible import build_s_set
from fair_division_engine.pareto import pareto_filter
from fair_division_engine.proportional import find_proportional_division
from fair_division_engine.equitable import find_equitable_division

EPS = 0.01


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


def print_result(name, result):
    """Вывод результата в читаемом виде"""
    print(f"\n{'='*60}")
    print(f"{name}")
    print(f"{'='*60}")
    
    if result is None:
        print("❌ Решение не найдено")
        return
    
    # Statement 1: F(S) ⊆ Q(S) ⊆ P(S) ⊆ E(S) = U(S)
    print("\n📊 Statement 1 Classification:")
    if "statement1_sets" in result:
        sets = result["statement1_sets"]
        print(f"  E(S) - Efficient (Парето-оптимальный): {'✓' if sets['E'] else '✗'}")
        print(f"  P(S) - Proportional (GA≥H/2, GB≥H/2): {'✓' if sets['P'] else '✗'}")
        print(f"  Q(S) - Equitable (GA=GB):             {'✓' if sets['Q'] else '✗'}")
        print(f"  F(S) - Fair (E∩P∩Q):                  {'✓' if sets['F'] else '✗'}")
        print(f"  → Belongs to: {result.get('belongs_to_sets', 'U(S)')}")
    else:
        print(f"  ✓ Пропорциональный: {result['proportional_exists']}")
        print(f"  ✓ Равноценный: {result.get('equitable_exists', False)}")
    
    print(f"\nВыигрыши:")
    print(f"  A: {result['gains']['A']:.2f}")
    print(f"  B: {result['gains']['B']:.2f}")
    print(f"  Разница: {abs(result['gains']['A'] - result['gains']['B']):.2f}")
    
    div = result['division']
    
    if div.get('divisible_A'):
        print(f"\nДелимые пункты (доля для A):")
        for item, share in div['divisible_A'].items():
            print(f"  {item}: {share:.4f} (B получает {1-share:.4f})")
    
    if div.get('indivisible'):
        print(f"\nНеделимые пункты:")
        for i, owner in enumerate(div['indivisible']):
            print(f"  item {i+1}: {'A' if owner == 1 else 'B'}")


def test_example1():
    """Example 1 — Divorce arrangement"""
    print("\n\nTEST 1: DIVORCE ARRANGEMENT")
    L, M, H = 5, 0, 100
    a_d = [50, 20, 15, 10, 5]
    b_d = [40, 30, 10, 10, 10]
    a_w, b_w = [], []
    
    result = solve_fair_division(L, M, a_d, b_d, a_w, b_w, H)
    print_result("Example 1: Divorce", result)
    
    assert result is not None
    assert abs(result['gains']['A'] - 56.67) < EPS
    assert abs(result['gains']['B'] - 56.67) < EPS
    print("✅ Тест пройден!")


def test_example2():
    """Example 2 — Mergers"""
    print("\n\nTEST 2: MERGERS")
    L, M, H = 1, 4, 100
    a_d = [30]
    b_d = [10]
    a_w = [25, 15, 20, 10]
    b_w = [10, 20, 35, 25]
    
    result = solve_fair_division(L, M, a_d, b_d, a_w, b_w, H)
    print_result("Example 2: Mergers", result)
    
    assert result is not None
    assert abs(result['gains']['A'] - 62.5) < EPS
    assert abs(result['gains']['B'] - 62.5) < EPS
    print("✅ Тест пройден!")


def test_example3():
    """Example 3 — No fair division"""
    print("\n\nTEST 3: NO FAIR DIVISION (but proportional exists)")
    L, M, H = 2, 3, 100
    a_d = [10, 10]
    b_d = [30, 20]
    a_w = [35, 30, 15]
    b_w = [18, 20, 12]
    
    result = solve_fair_division(L, M, a_d, b_d, a_w, b_w, H)
    print_result("Example 3: No Fair Division", result)
    
    assert result is not None
    assert result['gains']['A'] >= 50
    assert result['gains']['B'] >= 50
    print("✅ Тест пройден!")


def test_example4():
    """Example 4 — No proportional"""
    print("\n\nTEST 4: NO PROPORTIONAL DIVISION")
    L, M, H = 1, 4, 100
    a_d = [1]
    b_d = [1]
    a_w = [45, 30, 15, 9]
    b_w = [30, 25, 22, 22]
    
    result = solve_fair_division(L, M, a_d, b_d, a_w, b_w, H)
    print_result("Example 4: No Proportional", result)
    
    assert result is None
    print("✅ Тест пройден!")


def test_example5():
    """Example 5 — Proportional but no equitable"""
    print("\n\nTEST 5: PROPORTIONAL BUT NO EQUITABLE")
    L, M, H = 1, 4, 100
    a_d = [3]
    b_d = [3]
    a_w = [45, 30, 20, 2]
    b_w = [17, 20, 22, 38]
    
    result = solve_fair_division(L, M, a_d, b_d, a_w, b_w, H)
    print_result("Example 5: Proportional No Equitable", result)
    
    assert result is not None
    assert result['gains']['A'] >= 50
    assert result['gains']['B'] >= 50
    print("✅ Тест пройден!")


def test_example6():
    """Example 6 — Equitable exists but not efficient"""
    print("\n\nTEST 6: EQUITABLE NOT EFFICIENT")
    L, M, H = 1, 4, 100
    a_d = [5]
    b_d = [5]
    a_w = [40, 10, 20, 25]
    b_w = [49, 1, 25, 20]
    
    result = solve_fair_division(L, M, a_d, b_d, a_w, b_w, H)
    print_result("Example 6: Equitable Not Efficient", result)
    
    assert result is not None
    assert result['gains']['A'] >= 50
    assert result['gains']['B'] >= 50
    print("✅ Тест пройден!")


def test_example7():
    """Example 7 — Fair division exists"""
    print("\n\nTEST 7: FAIR DIVISION EXISTS (51.5/51.5)")
    L, M, H = 1, 4, 100
    a_d = [17]
    b_d = [17]
    a_w = [42, 37, 2, 2]
    b_w = [45, 34, 2, 2]
    
    result = solve_fair_division(L, M, a_d, b_d, a_w, b_w, H)
    print_result("Example 7: Fair Division", result)
    
    assert result is not None
    assert abs(result['gains']['A'] - 51.5) < EPS
    assert abs(result['gains']['B'] - 51.5) < EPS
    print("✅ Тест пройден!")


def test_example8():
    """Example 8 — Only indivisible items"""
    print("\n\nTEST 8: ONLY INDIVISIBLE ITEMS")
    L, M, H = 0, 3, 100
    a_d, b_d = [], []
    a_w = [51, 45, 4]
    b_w = [40, 50, 10]
    
    result = solve_fair_division(L, M, a_d, b_d, a_w, b_w, H)
    print_result("Example 8: Only Indivisible", result)
    
    assert result is not None
    sigma = result['division']['indivisible']
    gains_a = result['gains']['A']
    gains_b = result['gains']['B']
    
    print(f"\nНайденное распределение σ={sigma}")
    print(f"Выигрыши: ({gains_a}, {gains_b})")
    
    if sigma == [1, 0, 0]:
        print("→ Profitably fair (max min)")
        assert abs(gains_a - 51) < EPS
        assert abs(gains_b - 60) < EPS
    elif sigma == [1, 0, 1]:
        print("→ Uniformly fair (min diff)")
        assert abs(gains_a - 55) < EPS
        assert abs(gains_b - 50) < EPS
    
    print("✅ Тест пройден!")


if __name__ == "__main__":
    test_example1()
    test_example2()
    test_example3()
    test_example4()
    test_example5()
    test_example6()
    test_example7()
    test_example8()
    
    print("\n" + "="*60)
    print("ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО! ✅")
    print("="*60)
