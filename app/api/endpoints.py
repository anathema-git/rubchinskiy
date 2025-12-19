"""
API endpoints для системы справедливого дележа
"""
from fastapi import APIRouter, HTTPException
from typing import Optional
import sys
import os

# Добавляем корневую директорию в PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models.request_models import FairDivisionRequest
from app.models.response_models import FairDivisionResponse, FairDivisionDebugResponse, DebugInfo, Division, Gains
from fair_division_engine.utils import validate_input
from fair_division_engine.r_polygon import build_r_polygon, check_r_monotonicity
from fair_division_engine.indivisible import build_s_set
from fair_division_engine.pareto import pareto_filter
from fair_division_engine.proportional import find_proportional_division
from fair_division_engine.equitable import find_equitable_division
from fair_division_engine.comprehensive import find_all_division_types
from fair_division_engine.visualization import plot_ad_region, plot_ad_region_with_sp

router = APIRouter()


@router.post("/solve")
async def solve_fair_division(request: FairDivisionRequest, debug: bool = False):
    """
    Решение задачи справедливого дележа
    
    Согласно Statement 1: F(S) ⊆ Q(S) ⊆ P(S) ⊆ E(S) = U(S)
    Находит все типы решений: Efficient, Proportional, Equitable, Fair
    
    Args:
        request: данные задачи (L, M, оценки a_d, b_d, a_w, b_w)
        debug: включить отладочную информацию
        
    Returns:
        Результат со всеми типами решений
    """
    try:
        # Валидация входных данных
        validate_input(
            request.L, request.M,
            request.a_d, request.b_d,
            request.a_w, request.b_w,
            request.H
        )
        
        # Комплексное решение - находим все типы
        result = find_all_division_types(
            request.a_d, request.b_d,
            request.a_w, request.b_w,
            request.H
        )
        
        # Формируем ответ
        def format_division(div_data):
            if div_data is None:
                return None
            x, sigma = div_data
            return Division(
                divisible_A={f"D{i+1}": round(x[i], 4) for i in range(len(x))},
                divisible_B={f"D{i+1}": round(1-x[i], 4) for i in range(len(x))},
                indivisible=sigma
            )
        
        def format_gains(gains_data):
            if gains_data is None:
                return None
            ga, gb = gains_data
            return Gains(A=round(ga, 2), B=round(gb, 2))
        
        response = {
            "has_efficient": result['has_efficient'],
            "has_proportional": result['has_proportional'],
            "has_equitable": result['has_equitable'],
            "has_fair": result['has_fair'],
            
            "efficient_division": format_division(result['efficient_division']),
            "proportional_division": format_division(result['proportional_division']),
            "equitable_division": format_division(result['equitable_division']),
            "fair_division": format_division(result['fair_division']),
            
            "efficient_gains": format_gains(result['efficient_gains']),
            "proportional_gains": format_gains(result['proportional_gains']),
            "equitable_gains": format_gains(result['equitable_gains']),
            "fair_gains": format_gains(result['fair_gains']),
            
            "sp_points_count": result['sp_points_count'],
            
            # Statement 1 classification
            "efficient_exists": result.get('efficient_exists', result['has_efficient']),
            "proportional_exists": result.get('proportional_exists', result['has_proportional']),
            "equitable_exists": result.get('equitable_exists', result['has_equitable']),
            "fair_exists": result.get('fair_exists', result['has_fair']),
            "statement1_sets": result.get('statement1_sets', []),
            "belongs_to_sets": result.get('belongs_to_sets', 'U(S)'),
            
            # Для обратной совместимости
            "division": format_division(result['fair_division'] or result['equitable_division'] or result['proportional_division']),
            "gains": format_gains(result['fair_gains'] or result['equitable_gains'] or result['proportional_gains']),
            "method": "comprehensive"
        }
        
        # Добавление отладочной информации
        if debug:
            R, sorted_indices = build_r_polygon(request.a_d, request.b_d)
            S = build_s_set(request.a_w, request.b_w)
            SP = pareto_filter(S)
            
            debug_info = DebugInfo(
                R_polygon=[[round(x, 2), round(y, 2)] for x, y in R],
                sorted_indices=sorted_indices,
                S_size=len(S),
                SP_size=len(SP),
                SP_points=[
                    {"x": round(x, 2), "y": round(y, 2), "sigma": sigma}
                    for x, y, sigma in SP
                ]
            )
            response["debug"] = debug_info
            return FairDivisionDebugResponse(**response).model_dump()
        
        return FairDivisionResponse(**response).model_dump()
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")


@router.post("/plot/ad")
async def plot_ad_graph(request: FairDivisionRequest):
    """
    Построение графика области достижимости Ad (ломаная R)
    
    Возвращает base64-encoded PNG изображение графика
    """
    try:
        # Валидация
        validate_input(
            request.L, request.M,
            request.a_d, request.b_d,
            request.a_w, request.b_w,
            request.H
        )
        
        # Построение графика
        img_base64 = plot_ad_region(request.a_d, request.b_d)
        
        return {
            "success": True,
            "image": img_base64,
            "format": "png",
            "encoding": "base64"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка построения графика: {str(e)}")


@router.post("/plot/ad-with-sp")
async def plot_ad_with_sp_graph(request: FairDivisionRequest):
    """
    Построение графика области достижимости с SP-точками
    
    Показывает ломаную R, точки Парето-множества SP и линии пропорциональности
    """
    try:
        # Валидация
        validate_input(
            request.L, request.M,
            request.a_d, request.b_d,
            request.a_w, request.b_w,
            request.H
        )
        
        # Построение данных
        R, sorted_indices = build_r_polygon(request.a_d, request.b_d)
        S = build_s_set(request.a_w, request.b_w)
        SP = pareto_filter(S)
        
        # Находим решение для отображения на графике
        from fair_division_engine.comprehensive import find_all_division_types, calculate_gains
        solution_point = None
        
        try:
            result = find_all_division_types(
                request.a_d, request.b_d,
                request.a_w, request.b_w,
                request.H
            )
            # Берём лучший найденный тип дележа
            if result.get("fair_division"):
                x, sigma = result["fair_division"]
                GA, GB = calculate_gains(request.a_d, request.b_d, request.a_w, request.b_w, x, sigma)
                solution_point = (GA, GB)
            elif result.get("equitable_division"):
                x, sigma = result["equitable_division"]
                GA, GB = calculate_gains(request.a_d, request.b_d, request.a_w, request.b_w, x, sigma)
                solution_point = (GA, GB)
            elif result.get("proportional_division"):
                x, sigma = result["proportional_division"]
                GA, GB = calculate_gains(request.a_d, request.b_d, request.a_w, request.b_w, x, sigma)
                solution_point = (GA, GB)
        except Exception as e:
            # Логируем ошибку для отладки
            import logging
            logging.error(f"Error finding solution point: {e}")
            pass  # Если решение не найдено, просто не показываем точку
        
        # Построение графика
        img_base64 = plot_ad_region_with_sp(
            request.a_d, request.b_d,
            request.a_w, request.b_w,
            SP, request.H / 2.0,
            solution_point=solution_point
        )
        
        return {
            "success": True,
            "image": img_base64,
            "format": "png",
            "encoding": "base64",
            "sp_count": len(SP)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка построения графика: {str(e)}")




@router.get("/info")
async def get_info():
    """
    Информация о системе и алгоритме
    """
    return {
        "title": "Fair Division System",
        "description": "Система справедливого дележа с делимыми и неделимыми пунктами",
        "algorithm": "Rubchinsky A. Fair Division with Divisible and Indivisible Items (2009)",
        "version": "1.0.0",
        "features": [
            "Построение ломаной R для делимых пунктов",
            "Генерация множества S всех распределений неделимых пунктов",
            "Выделение Парето-множества SP",
            "Проверка пропорциональности через вершины и отрезки",
            "Поддержка до 2^20 комбинаций неделимых пунктов",
            "Визуализация области достижимости Ad"
        ],
        "endpoints": {
            "POST /api/solve": "Решение задачи справедливого дележа",
            "POST /api/plot/ad": "График области достижимости Ad",
            "POST /api/plot/ad-with-sp": "График Ad с SP-точками",
            "GET /api/info": "Информация о системе",
            "GET /": "Веб-интерфейс",
            "GET /health": "Проверка здоровья сервиса"
        }
    }
