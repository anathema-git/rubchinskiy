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
from app.models.response_models import FairDivisionResponse, FairDivisionDebugResponse, DebugInfo
from fair_division_engine.utils import validate_input
from fair_division_engine.r_polygon import build_r_polygon, check_r_monotonicity
from fair_division_engine.indivisible import build_s_set
from fair_division_engine.pareto import pareto_filter
from fair_division_engine.proportional import find_proportional_division
from fair_division_engine.visualization import plot_ad_region, plot_ad_region_with_sp

router = APIRouter()


@router.post("/solve")
async def solve_fair_division(request: FairDivisionRequest, debug: bool = False):
    """
    Решение задачи справедливого дележа
    
    Принимает данные о делимых и неделимых пунктах с оценками участников A и B,
    и возвращает пропорциональный делёж если он существует.
    
    Args:
        request: данные задачи (L, M, оценки a_d, b_d, a_w, b_w)
        debug: включить отладочную информацию
        
    Returns:
        Результат работы алгоритма с найденным дележом или сообщением об отсутствии решения
    """
    try:
        # Валидация входных данных
        validate_input(
            request.L, request.M,
            request.a_d, request.b_d,
            request.a_w, request.b_w,
            request.H
        )
        
        # Шаг 1: Построение ломаной R для делимых пунктов
        R, sorted_indices = build_r_polygon(request.a_d, request.b_d)
        
        # Проверка монотонности R
        if not check_r_monotonicity(R):
            raise HTTPException(
                status_code=400,
                detail="Ломаная R не является строго монотонной. Проверьте входные данные."
            )
        
        # Шаг 2: Построение множества S всех распределений неделимых пунктов
        S = build_s_set(request.a_w, request.b_w)
        
        # Шаг 3: Выделение Парето-множества SP
        SP = pareto_filter(S)
        
        # Шаг 4: Поиск пропорционального дележа
        result = find_proportional_division(
            request.L, request.M,
            request.a_d, request.b_d,
            request.a_w, request.b_w,
            R, sorted_indices, SP,
            request.H
        )
        
        if result is None:
            # Пропорциональный делёж не найден
            response = {
                "proportional_exists": False,
                "error": "Пропорциональный делёж не существует для данных входных данных"
            }
        else:
            response = result
        
        # Добавление отладочной информации
        if debug:
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
        
        # Построение графика
        img_base64 = plot_ad_region_with_sp(
            request.a_d, request.b_d,
            request.a_w, request.b_w,
            SP, request.H / 2.0
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
