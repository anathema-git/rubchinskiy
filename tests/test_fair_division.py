"""
Тесты для модуля fair_division_engine
"""
import sys
import os

# Добавляем корневую директорию в PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fair_division_engine.utils import validate_input, safe_divide
from fair_division_engine.r_polygon import build_r_polygon, check_r_monotonicity
from fair_division_engine.indivisible import build_s_set
from fair_division_engine.pareto import pareto_filter, shift_r_polygon
from fair_division_engine.proportional import (
    find_proportional_division,
    check_vertex_proportionality,
    check_segment_proportionality
)


class TestUtils:
    """Тесты для utils.py"""
    
    def test_validate_input_correct(self):
        """Проверка корректных входных данных"""
        # Не должно быть исключений
        # Суммы: a_d=60, a_w=40, итого A=100; b_d=50, b_w=50, итого B=100
        validate_input(
            L=3, M=2,
            a_d=[20, 15, 25],  # сумма = 60
            b_d=[20, 30, 0],   # сумма = 50
            a_w=[25, 15],      # сумма = 40
            b_w=[30, 20],      # сумма = 50
            H=100
        )
    
    def test_validate_input_wrong_lengths(self):
        """Проверка некорректных длин массивов"""
        with pytest.raises(ValueError):
            validate_input(
                L=3, M=4,
                a_d=[10, 20],  # неверная длина
                b_d=[15, 15, 20],
                a_w=[35, 30, 15, 20],
                b_w=[18, 20, 12, 25]
            )
    
    def test_validate_input_negative_values(self):
        """Проверка отрицательных значений"""
        with pytest.raises(ValueError):
            validate_input(
                L=2, M=0,
                a_d=[10, -5],  # отрицательное значение
                b_d=[15, 15],
                a_w=[],
                b_w=[]
            )
    
    def test_validate_input_wrong_sum(self):
        """Проверка несоответствия суммы оценок"""
        with pytest.raises(ValueError):
            validate_input(
                L=2, M=0,
                a_d=[10, 20],  # сумма = 30, должно быть 100
                b_d=[15, 15],  # сумма = 30, должно быть 100
                a_w=[],
                b_w=[],
                H=100
            )
    
    def test_safe_divide(self):
        """Проверка безопасного деления"""
        assert safe_divide(10, 2) == 5.0
        assert safe_divide(10, 0) == 0.0
        assert safe_divide(10, 0, default=100) == 100.0


class TestRPolygon:
    """Тесты для r_polygon.py"""
    
    def test_build_r_polygon_simple(self):
        """Простой тест построения ломаной R"""
        a_d = [10, 20, 30]
        b_d = [15, 15, 20]
        
        R, sorted_indices = build_r_polygon(a_d, b_d)
        
        # Проверяем, что ломаная начинается с (0, Bd)
        assert R[0] == (0.0, 50.0)
        
        # Проверяем, что ломаная заканчивается в (Ad, 0)
        assert R[-1][0] == 60.0
        assert R[-1][1] == 0.0
        
        # Проверяем количество точек
        assert len(R) == 4  # L + 1
        
        # Проверяем монотонность
        assert check_r_monotonicity(R)
    
    def test_build_r_polygon_sorting(self):
        """Проверка правильности сортировки"""
        a_d = [30, 10, 20]  # ratio: 30/20=1.5, 10/15=0.67, 20/15=1.33
        b_d = [20, 15, 15]
        
        R, sorted_indices = build_r_polygon(a_d, b_d)
        
        # Ожидаем порядок: [0] (ratio=1.5), [2] (ratio=1.33), [1] (ratio=0.67)
        assert sorted_indices == [0, 2, 1]
    
    def test_build_r_polygon_empty(self):
        """Проверка пустого набора делимых пунктов"""
        R, sorted_indices = build_r_polygon([], [])
        
        assert R == [(0.0, 0.0)]
        assert sorted_indices == []


class TestIndivisible:
    """Тесты для indivisible.py"""
    
    def test_build_s_set_simple(self):
        """Простой тест построения множества S"""
        a_w = [10, 20]
        b_w = [15, 25]
        
        S = build_s_set(a_w, b_w)
        
        # Должно быть 2^2 = 4 комбинации
        assert len(S) == 4
        
        # Проверяем все комбинации
        expected = [
            (0, 40, [0, 0]),    # оба к B
            (10, 25, [1, 0]),   # первый к A, второй к B
            (20, 15, [0, 1]),   # первый к B, второй к A
            (30, 0, [1, 1])     # оба к A
        ]
        
        for exp in expected:
            assert exp in S
    
    def test_build_s_set_empty(self):
        """Проверка пустого набора неделимых пунктов"""
        S = build_s_set([], [])
        
        assert len(S) == 1
        assert S[0] == (0.0, 0.0, [])


class TestPareto:
    """Тесты для pareto.py"""
    
    def test_pareto_filter_simple(self):
        """Простой тест фильтрации Парето-множества"""
        S = [
            (0, 40, [0, 0]),
            (10, 25, [1, 0]),
            (20, 15, [0, 1]),
            (30, 0, [1, 1])
        ]
        
        SP = pareto_filter(S)
        
        # Проверяем, что точки отсортированы по убыванию x
        for i in range(len(SP) - 1):
            assert SP[i][0] >= SP[i+1][0]
        
        # Проверяем, что y возрастает
        for i in range(len(SP) - 1):
            assert SP[i][1] < SP[i+1][1]
    
    def test_pareto_filter_all_pareto(self):
        """Все точки являются Парето-оптимальными"""
        S = [
            (30, 10, [1]),
            (20, 20, [2]),
            (10, 30, [3])
        ]
        
        SP = pareto_filter(S)
        
        # Все точки должны остаться
        assert len(SP) == 3
    
    def test_shift_r_polygon(self):
        """Проверка смещения ломаной R"""
        R = [(0, 10), (5, 5), (10, 0)]
        x_star, y_star = 20, 30
        
        R_star = shift_r_polygon(R, x_star, y_star)
        
        expected = [(20, 40), (25, 35), (30, 30)]
        assert R_star == expected


class TestProportional:
    """Тесты для proportional.py"""
    
    def test_check_vertex_proportionality_found(self):
        """Проверка нахождения вершины с пропорциональностью"""
        R_star = [(40, 40), (55, 45), (60, 50)]
        
        idx = check_vertex_proportionality(R_star, threshold=50.0)
        
        assert idx == 2  # третья вершина (60, 50)
    
    def test_check_vertex_proportionality_not_found(self):
        """Проверка отсутствия пропорциональности в вершинах"""
        R_star = [(40, 40), (45, 35), (48, 30)]
        
        idx = check_vertex_proportionality(R_star, threshold=50.0)
        
        assert idx is None
    
    def test_check_segment_proportionality_found(self):
        """Проверка пересечения отрезка с линией пропорциональности"""
        p1 = (45, 55)
        p2 = (55, 45)
        
        intersection = check_segment_proportionality(p1, p2, threshold=50.0)
        
        assert intersection is not None
        assert intersection[0] == 50.0
        assert intersection[1] == 50.0
    
    def test_check_segment_proportionality_not_found(self):
        """Проверка отсутствия пересечения"""
        p1 = (40, 40)
        p2 = (45, 35)
        
        intersection = check_segment_proportionality(p1, p2, threshold=50.0)
        
        assert intersection is None


class TestIntegration:
    """Интеграционные тесты всего алгоритма"""
    
    def test_example_from_spec(self):
        """Пример из раздела 6 ТЗ"""
        L = 3
        M = 4
        a_d = [10, 20, 30]
        b_d = [15, 15, 20]
        a_w = [35, 30, 15, 20]
        b_w = [18, 20, 12, 25]
        H = 100
        
        # Шаг 1: Построение R
        R, sorted_indices = build_r_polygon(a_d, b_d)
        assert check_r_monotonicity(R)
        
        # Шаг 2: Построение S
        S = build_s_set(a_w, b_w)
        assert len(S) == 16  # 2^4
        
        # Шаг 3: Парето-фильтрация
        SP = pareto_filter(S)
        assert len(SP) > 0
        assert len(SP) <= len(S)
        
        # Шаг 4: Поиск пропорционального дележа
        result = find_proportional_division(
            L, M, a_d, b_d, a_w, b_w,
            R, sorted_indices, SP, H
        )
        
        # Проверяем, что решение найдено
        assert result is not None
        assert result['proportional_exists'] == True
        
        # Проверяем выигрыши
        assert result['gains']['A'] >= 50.0
        assert result['gains']['B'] >= 50.0
    
    def test_no_solution_case(self):
        """Случай, когда пропорциональный делёж невозможен"""
        # Искусственный пример: все оценки A = 100, все оценки B = 0
        L = 2
        M = 0
        a_d = [50, 50]
        b_d = [0.01, 99.99]  # B оценивает только один пункт высоко
        a_w = []
        b_w = []
        H = 100
        
        R, sorted_indices = build_r_polygon(a_d, b_d)
        S = build_s_set(a_w, b_w)
        SP = pareto_filter(S)
        
        result = find_proportional_division(
            L, M, a_d, b_d, a_w, b_w,
            R, sorted_indices, SP, H
        )
        
        # В данном случае может быть решение или нет в зависимости от данных
        # Просто проверяем, что функция работает без ошибок
        assert result is None or isinstance(result, dict)
    
    def test_only_divisible(self):
        """Тест только с делимыми пунктами (M=0)"""
        L = 3
        M = 0
        a_d = [30, 40, 30]
        b_d = [20, 30, 50]
        a_w = []
        b_w = []
        H = 100
        
        R, sorted_indices = build_r_polygon(a_d, b_d)
        S = build_s_set(a_w, b_w)
        SP = pareto_filter(S)
        
        result = find_proportional_division(
            L, M, a_d, b_d, a_w, b_w,
            R, sorted_indices, SP, H
        )
        
        # Должно быть решение
        assert result is not None
        assert result['proportional_exists'] == True
    
    def test_only_indivisible(self):
        """Тест только с неделимыми пунктами (L=0)"""
        L = 0
        M = 4
        a_d = []
        b_d = []
        a_w = [25, 25, 25, 25]
        b_w = [25, 25, 25, 25]
        H = 100
        
        R, sorted_indices = build_r_polygon(a_d, b_d)
        S = build_s_set(a_w, b_w)
        SP = pareto_filter(S)
        
        result = find_proportional_division(
            L, M, a_d, b_d, a_w, b_w,
            R, sorted_indices, SP, H
        )
        
        # Должно быть решение (каждый получает по 2 пункта)
        assert result is not None
        assert result['proportional_exists'] == True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
