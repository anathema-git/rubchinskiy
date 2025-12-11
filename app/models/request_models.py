"""
Pydantic модели для запросов к API
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional


class FairDivisionRequest(BaseModel):
    """
    Модель запроса для решения задачи справедливого дележа
    """
    L: int = Field(..., ge=0, description="Количество делимых пунктов")
    M: int = Field(..., ge=0, description="Количество неделимых пунктов")
    a_d: List[float] = Field(..., description="Оценки участника A для делимых пунктов")
    b_d: List[float] = Field(..., description="Оценки участника B для делимых пунктов")
    a_w: List[float] = Field(..., description="Оценки участника A для неделимых пунктов")
    b_w: List[float] = Field(..., description="Оценки участника B для неделимых пунктов")
    H: Optional[float] = Field(100.0, description="Сумма всех оценок (обычно 100)")
    
    @validator('a_d')
    def validate_a_d_length(cls, v, values):
        if 'L' in values and len(v) != values['L']:
            raise ValueError(f"Длина a_d должна быть равна L={values['L']}")
        return v
    
    @validator('b_d')
    def validate_b_d_length(cls, v, values):
        if 'L' in values and len(v) != values['L']:
            raise ValueError(f"Длина b_d должна быть равна L={values['L']}")
        return v
    
    @validator('a_w')
    def validate_a_w_length(cls, v, values):
        if 'M' in values and len(v) != values['M']:
            raise ValueError(f"Длина a_w должна быть равна M={values['M']}")
        return v
    
    @validator('b_w')
    def validate_b_w_length(cls, v, values):
        if 'M' in values and len(v) != values['M']:
            raise ValueError(f"Длина b_w должна быть равна M={values['M']}")
        return v
    
    @validator('a_d', 'b_d', 'a_w', 'b_w')
    def validate_non_negative(cls, v):
        if any(x < 0 for x in v):
            raise ValueError("Все оценки должны быть неотрицательными")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "L": 3,
                "M": 4,
                "a_d": [10, 20, 30],
                "b_d": [15, 15, 20],
                "a_w": [35, 30, 15, 20],
                "b_w": [18, 20, 12, 25],
                "H": 100
            }
        }
