"""
Тесты на основе примеров из статьи Fair Division
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fair_division_engine.r_polygon import build_r_polygon
from fair_division_engine.indivisible import build_s_set
from fair_division_engine.pareto import pareto_filter
from fair_division_engine.proportional import find_proportional_division
from fair_division_engine.equitable import find_equitable_division

EPS = 0.01  # Допустимая погрешность


def solve_fair_division(L, M, a_d, b_d, a_w, b_w, H=100):
    """
    Вспомогательная функция для решения задачи fair division
    Сначала ищет равноценный делёж, затем пропорциональный
    """
    R, sorted_indices = build_r_polygon(a_d, b_d)
    S = build_s_set(a_w, b_w)
    SP = pareto_filter(S)
    
    # Сначала пытаемся найти равноценный
    result = find_equitable_division(L, M, a_d, b_d, a_w, b_w, R, sorted_indices, SP, H)
    
    # Если не найден, ищем просто пропорциональный
    if result is None:
        result = find_proportional_division(L, M, a_d, b_d, a_w, b_w, R, sorted_indices, SP, H)
    
    return result


class TestExample1DivorceArrangement:
    """
    Example 1 — Divorce arrangement (AW, все пункты делимые)
    Источник: Table 1
    """
    
    def test_divorce_arrangement(self):
        """
        Тест на пример развода с 5 делимыми пунктами
        Ожидаемое решение: каждый получает 56.67
        """
        # Все пункты делимые
        L = 5  # делимых
        M = 0  # неделимых
        H = 100
        
        # Оценки для делимых пунктов
        a_d = [50, 20, 15, 10, 5]  # Retirement, House, Cottage, Portfolio, Other
        b_d = [40, 30, 10, 10, 10]
        
        a_w = []
        b_w = []
        
        # Ищем решение
        result = solve_fair_division(L, M, a_d, b_d, a_w, b_w, H)
        
        assert result is not None, "Пропорциональный делёж должен существовать"
        assert result["proportional_exists"] is True
        
        # Проверяем выигрыши
        gain_A = result["gains"]["A"]
        gain_B = result["gains"]["B"]
        
        assert abs(gain_A - 56.67) < EPS, f"Выигрыш A должен быть ~56.67, получено {gain_A}"
        assert abs(gain_B - 56.67) < EPS, f"Выигрыш B должен быть ~56.67, получено {gain_B}"
        
        # Проверяем что делится не более одного пункта
        divisible_A = result["division"]["divisible_A"]
        split_count = sum(1 for share in divisible_A.values() if 0 < share < 1)
        assert split_count <= 1, "Должен делиться не более одного предмета"


class TestExample2Mergers:
    """
    Example 2 — Mergers (только 1-й пункт делимый)
    Источник: Table 2-4
    """
    
    def test_mergers(self):
        """
        Тест на пример слияния компаний
        Ожидаемое решение: каждый получает 62.5
        """
        # 1 делимый (Laying off), 4 неделимых
        L = 1
        M = 4
        H = 100
        
        # Laying off - делимый
        a_d = [30]
        b_d = [10]
        
        # CEO, President, Headquarters, Name - неделимые
        a_w = [25, 15, 20, 10]
        b_w = [10, 20, 35, 25]
        
        result = solve_fair_division(L, M, a_d, b_d, a_w, b_w, H)
        
        assert result is not None, "Пропорциональный делёж должен существовать"
        assert result["proportional_exists"] is True
        
        gain_A = result["gains"]["A"]
        gain_B = result["gains"]["B"]
        
        assert abs(gain_A - 62.5) < EPS, f"Выигрыш A должен быть ~62.5, получено {gain_A}"
        assert abs(gain_B - 62.5) < EPS, f"Выигрыш B должен быть ~62.5, получено {gain_B}"
        
        # Проверяем распределение неделимых
        sigma = result["division"]["indivisible"]
        # A получает CEO (index 0) и President (index 1)
        # B получает Headquarters (index 2) и Name (index 3)
        assert sigma[0] == 1, "A должен получить CEO"
        assert sigma[1] == 1, "A должен получить President"
        assert sigma[2] == 0, "B должен получить Headquarters"
        assert sigma[3] == 0, "B должен получить Name"
        
        # Проверяем делимый пункт (Laying off)
        divisible_A = result["division"]["divisible_A"]
        laying_off_share = divisible_A.get("item_1", 0)
        assert abs(laying_off_share - 0.75) < EPS, f"Доля Laying off для A должна быть ~0.75, получено {laying_off_share}"


class TestExample3NoFairDivision:
    """
    Example 3 — 2 делимых + 3 неделимых (fair division не существует)
    Источник: Table 5
    """
    
    def test_no_fair_division(self):
        """
        Тест на случай когда пропорциональный делёж существует, но не эффективен
        """
        L = 2  # делимых
        M = 3  # неделимых
        H = 100
        
        # Items 1-2 делимые
        a_d = [10, 10]
        b_d = [30, 20]
        
        # Items 3-5 неделимые
        a_w = [35, 30, 15]
        b_w = [18, 20, 12]
        
        result = solve_fair_division(L, M, a_d, b_d, a_w, b_w, H)
        
        # Пропорциональный делёж должен существовать
        assert result is not None, "Пропорциональный делёж должен существовать"
        assert result["proportional_exists"] is True
        
        # Оба участника должны получить >= 50
        gain_A = result["gains"]["A"]
        gain_B = result["gains"]["B"]
        
        assert gain_A >= 50, f"Выигрыш A должен быть >= 50, получено {gain_A}"
        assert gain_B >= 50, f"Выигрыш B должен быть >= 50, получено {gain_B}"


class TestExample4NoProportional:
    """
    Example 4 — пропорционального дележа нет
    Источник: Table 8
    """
    
    def test_no_proportional(self):
        """
        Тест на случай когда пропорциональный делёж не существует
        """
        L = 1  # делимый
        M = 4  # неделимых
        H = 100
        
        # Item 0 делимый
        a_d = [1]
        b_d = [1]
        
        # Items 1-4 неделимые
        a_w = [45, 30, 15, 9]
        b_w = [30, 25, 22, 22]
        
        result = solve_fair_division(L, M, a_d, b_d, a_w, b_w, H)
        
        # Пропорциональный делёж НЕ должен существовать
        assert result is None, "Пропорциональный делёж не должен существовать"


class TestExample5ProportionalNoEquitable:
    """
    Example 5 — пропорциональный есть, равноценного нет
    Источник: Table 10
    """
    
    def test_proportional_no_equitable(self):
        """
        Тест на случай когда есть пропорциональный, но нет равноценного
        """
        L = 1  # делимый
        M = 4  # неделимых
        H = 100
        
        # Item 0 делимый
        a_d = [3]
        b_d = [3]
        
        # Items 1-4 неделимые
        a_w = [45, 30, 20, 2]
        b_w = [17, 20, 22, 38]
        
        result = solve_fair_division(L, M, a_d, b_d, a_w, b_w, H)
        
        # Пропорциональный делёж должен существовать
        assert result is not None, "Пропорциональный делёж должен существовать"
        assert result["proportional_exists"] is True
        
        gain_A = result["gains"]["A"]
        gain_B = result["gains"]["B"]
        
        assert gain_A >= 50, f"Выигрыш A должен быть >= 50, получено {gain_A}"
        assert gain_B >= 50, f"Выигрыш B должен быть >= 50, получено {gain_B}"


class TestExample6EquitableNotEfficient:
    """
    Example 6 — равноценный есть (50/50), но он неэффективен
    Источник: Table 12
    """
    
    def test_equitable_not_efficient(self):
        """
        Тест на случай когда есть равноценный делёж, но он неэффективен
        """
        L = 1  # делимый
        M = 4  # неделимых
        H = 100
        
        # Item 0 делимый
        a_d = [5]
        b_d = [5]
        
        # Items 1-4 неделимые
        a_w = [40, 10, 20, 25]
        b_w = [49, 1, 25, 20]
        
        result = solve_fair_division(L, M, a_d, b_d, a_w, b_w, H)
        
        # Пропорциональный делёж должен существовать
        assert result is not None, "Пропорциональный делёж должен существовать"
        assert result["proportional_exists"] is True
        
        gain_A = result["gains"]["A"]
        gain_B = result["gains"]["B"]
        
        # Должен быть найден делёж лучше чем 50/50
        assert gain_A >= 50, f"Выигрыш A должен быть >= 50, получено {gain_A}"
        assert gain_B >= 50, f"Выигрыш B должен быть >= 50, получено {gain_B}"


class TestExample7FairDivisionExists:
    """
    Example 7 — fair division существует (51.5/51.5)
    Источник: Table 13
    
    Существует 4 равноценных решения, все дающие 51.5/51.5:
    1. σ=(0,1,0,0), x=0.8529 — решение из статьи
    2. σ=(0,1,0,1), x=0.7353
    3. σ=(0,1,1,0), x=0.7353
    4. σ=(0,1,1,1), x=0.6176
    """
    
    def test_fair_division_exists(self):
        """
        Тест на случай когда fair division существует
        """
        L = 1  # делимый
        M = 4  # неделимых
        H = 100
        
        # Item 0 делимый (17 баллов для обоих)
        a_d = [17]
        b_d = [17]
        
        # Items 1-4 неделимые
        a_w = [42, 37, 2, 2]
        b_w = [45, 34, 2, 2]
        
        result = solve_fair_division(L, M, a_d, b_d, a_w, b_w, H)
        
        assert result is not None, "Пропорциональный делёж должен существовать"
        assert result["proportional_exists"] is True
        
        gain_A = result["gains"]["A"]
        gain_B = result["gains"]["B"]
        
        # Проверяем что выигрыши близки к 51.5
        assert abs(gain_A - 51.5) < EPS, f"Выигрыш A должен быть ~51.5, получено {gain_A}"
        assert abs(gain_B - 51.5) < EPS, f"Выигрыш B должен быть ~51.5, получено {gain_B}"
        
        # Проверяем что есть равноценное решение
        assert abs(gain_A - gain_B) < EPS, f"Выигрыши должны быть равны: A={gain_A}, B={gain_B}"
        
        # Проверяем долю делимого пункта (должна быть в разумных пределах)
        divisible_A = result["division"]["divisible_A"]
        share_0 = divisible_A.get("item_1", 0)
        assert 0 <= share_0 <= 1, f"Доля item0 должна быть в [0,1], получено {share_0}"
        
        # Проверяем что найденное решение - одно из 4 возможных
        sigma = result["division"]["indivisible"]
        valid_solutions = [
            ([0, 1, 0, 0], 0.8529),  # Решение из статьи
            ([0, 1, 0, 1], 0.7353),
            ([0, 1, 1, 0], 0.7353),
            ([0, 1, 1, 1], 0.6176),
        ]
        
        found_valid = False
        for valid_sigma, valid_x in valid_solutions:
            if sigma == valid_sigma and abs(share_0 - valid_x) < EPS:
                found_valid = True
                break
        
        assert found_valid, f"Найденное решение σ={sigma}, x={share_0:.4f} не является одним из 4 известных решений"


class TestExample8OnlyIndivisible:
    """
    Example 8 — только неделимые: profitable и uniform fairness
    Источник: Table 15-16
    """
    
    def test_only_indivisible(self):
        """
        Тест на случай только неделимых пунктов
        """
        L = 0  # нет делимых
        M = 3  # неделимых
        H = 100
        
        a_d = []
        b_d = []
        
        # Items 1-3 неделимые
        a_w = [51, 45, 4]
        b_w = [40, 50, 10]
        
        result = solve_fair_division(L, M, a_d, b_d, a_w, b_w, H)
        
        # Пропорциональный делёж должен существовать
        assert result is not None, "Пропорциональный делёж должен существовать"
        assert result["proportional_exists"] is True
        
        gain_A = result["gains"]["A"]
        gain_B = result["gains"]["B"]
        
        # Должен быть один из двух пропорциональных дележей
        # σ=(1,0,0) => (51,60) или σ=(1,0,1) => (55,50)
        sigma = result["division"]["indivisible"]
        
        if sigma == [1, 0, 0]:
            # Profitably fair: max min
            assert abs(gain_A - 51) < EPS, f"Для σ=(1,0,0) выигрыш A = 51, получено {gain_A}"
            assert abs(gain_B - 60) < EPS, f"Для σ=(1,0,0) выигрыш B = 60, получено {gain_B}"
        elif sigma == [1, 0, 1]:
            # Uniformly fair: min |diff|
            assert abs(gain_A - 55) < EPS, f"Для σ=(1,0,1) выигрыш A = 55, получено {gain_A}"
            assert abs(gain_B - 50) < EPS, f"Для σ=(1,0,1) выигрыш B = 50, получено {gain_B}"
        else:
            pytest.fail(f"Неожиданное распределение σ={sigma}")
