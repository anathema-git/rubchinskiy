"""
Pydantic модели для ответов API
"""
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any


class SPPoint(BaseModel):
    """Точка из Парето-множества SP"""
    x: float = Field(..., description="Выигрыш A от неделимых пунктов")
    y: float = Field(..., description="Выигрыш B от неделимых пунктов")


class IntersectionPoint(BaseModel):
    """Точка пересечения отрезка с линией пропорциональности"""
    x: float
    y: float


class Division(BaseModel):
    """Распределение пунктов между участниками"""
    divisible_A: Dict[str, float] = Field(..., description="Доли делимых пунктов для участника A")
    divisible_B: Dict[str, float] = Field(..., description="Доли делимых пунктов для участника B")
    indivisible: List[int] = Field(..., description="Распределение неделимых пунктов (1=A, 0=B)")


class Gains(BaseModel):
    """Выигрыши участников"""
    A: float = Field(..., description="Выигрыш участника A")
    B: float = Field(..., description="Выигрыш участника B")


class FairDivisionResponse(BaseModel):
    """
    Модель ответа для решения задачи справедливого дележа
    """
    proportional_exists: bool = Field(..., description="Существует ли пропорциональный делёж")
    division: Optional[Division] = Field(None, description="Распределение пунктов (если найдено)")
    gains: Optional[Gains] = Field(None, description="Выигрыши участников (если найдено)")
    method: Optional[str] = Field(None, description="Метод нахождения дележа")
    vertex_index: Optional[int] = Field(None, description="Индекс вершины (для метода vertex)")
    segment_index: Optional[int] = Field(None, description="Индекс отрезка (для метода segment)")
    split_fraction: Optional[float] = Field(None, description="Доля деления пункта (для метода segment)")
    sp_point: Optional[SPPoint] = Field(None, description="Точка из SP-множества")
    intersection_point: Optional[IntersectionPoint] = Field(None, description="Точка пересечения (для метода segment)")
    error: Optional[str] = Field(None, description="Сообщение об ошибке (если есть)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "proportional_exists": True,
                "division": {
                    "divisible_A": {"item_1": 1.0, "item_2": 1.0, "item_3": 0.0},
                    "divisible_B": {"item_1": 0.0, "item_2": 0.0, "item_3": 1.0},
                    "indivisible": [1, 0, 1, 0]
                },
                "gains": {
                    "A": 56.67,
                    "B": 56.67
                },
                "method": "vertex"
            }
        }


class DebugInfo(BaseModel):
    """Отладочная информация для разработки"""
    R_polygon: List[List[float]] = Field(..., description="Ломаная R")
    sorted_indices: List[int] = Field(..., description="Индексы отсортированных делимых пунктов")
    S_size: int = Field(..., description="Размер множества S")
    SP_size: int = Field(..., description="Размер Парето-множества SP")
    SP_points: List[Dict[str, Any]] = Field(..., description="Точки SP-множества")


class FairDivisionDebugResponse(FairDivisionResponse):
    """Расширенный ответ с отладочной информацией"""
    debug: Optional[DebugInfo] = Field(None, description="Отладочная информация")
