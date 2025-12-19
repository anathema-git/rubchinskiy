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
    Согласно Statement 1: F(S) ⊆ Q(S) ⊆ P(S) ⊆ E(S) = U(S)
    """
    # Основная информация о существовании решений
    has_efficient: bool = Field(..., description="Существует ли эффективный делёж (E)")
    has_proportional: bool = Field(..., description="Существует ли пропорциональный делёж (P)")
    has_equitable: bool = Field(..., description="Существует ли равноценный делёж (Q)")
    has_fair: bool = Field(..., description="Существует ли справедливый делёж (F = E ∩ P ∩ Q)")
    
    # Statement 1 classification
    efficient_exists: Optional[bool] = Field(None, description="Существование эффективного решения (E(S))")
    proportional_exists: Optional[bool] = Field(None, description="Существование пропорционального решения (P(S))")
    equitable_exists: Optional[bool] = Field(None, description="Существование равноценного решения (Q(S))")
    fair_exists: Optional[bool] = Field(None, description="Существование справедливого решения (F(S))")
    statement1_sets: Optional[List[str]] = Field(None, description="Множества Statement 1, к которым принадлежит решение: E(S), P(S), Q(S), F(S)")
    belongs_to_sets: Optional[str] = Field(None, description="Классификация решения по Statement 1")
    
    # Решения для каждого типа
    efficient_division: Optional[Division] = Field(None, description="Эффективное распределение")
    proportional_division: Optional[Division] = Field(None, description="Пропорциональное распределение")
    equitable_division: Optional[Division] = Field(None, description="Равноценное распределение")
    fair_division: Optional[Division] = Field(None, description="Справедливое распределение")
    
    # Выигрыши для каждого типа
    efficient_gains: Optional[Gains] = Field(None, description="Выигрыши для эффективного")
    proportional_gains: Optional[Gains] = Field(None, description="Выигрыши для пропорционального")
    equitable_gains: Optional[Gains] = Field(None, description="Выигрыши для равноценного")
    fair_gains: Optional[Gains] = Field(None, description="Выигрыши для справедливого")
    
    # Дополнительная информация
    method: Optional[str] = Field(None, description="Метод нахождения дележа")
    sp_points_count: Optional[int] = Field(None, description="Количество точек в Парето-множестве")
    
    # Для обратной совместимости (deprecated)
    division: Optional[Division] = Field(None, description="[Deprecated] Используйте fair_division или equitable_division")
    gains: Optional[Gains] = Field(None, description="[Deprecated] Используйте fair_gains или equitable_gains")
    
    error: Optional[str] = Field(None, description="Сообщение об ошибке (если есть)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "has_efficient": True,
                "has_proportional": True,
                "has_equitable": True,
                "has_fair": True,
                "fair_division": {
                    "divisible_A": {"item_1": 1.0, "item_2": 1.0, "item_3": 0.0},
                    "divisible_B": {"item_1": 0.0, "item_2": 0.0, "item_3": 1.0},
                    "indivisible": [1, 0, 1, 0]
                },
                "fair_gains": {
                    "A": 56.67,
                    "B": 56.67
                },
                "method": "equitable"
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
