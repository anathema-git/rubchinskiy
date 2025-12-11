"""
Тесты для API endpoints
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestAPI:
    """Тесты для FastAPI endpoints"""
    
    def test_health_check(self):
        """Проверка эндпоинта health"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_api_info(self):
        """Проверка эндпоинта info"""
        response = client.get("/api/info")
        assert response.status_code == 200
        data = response.json()
        assert "title" in data
        assert "algorithm" in data
    
    def test_solve_example_from_spec(self):
        """Тест решения примера из ТЗ"""
        # Корректные данные с правильными суммами
        # a_d: 30+40+30=100, b_d: 20+30+50=100 (L=3, M=0)
        request_data = {
            "L": 3,
            "M": 0,
            "a_d": [30, 40, 30],
            "b_d": [20, 30, 50],
            "a_w": [],
            "b_w": [],
            "H": 100
        }
        
        response = client.post("/api/solve", json=request_data)
        assert response.status_code == 200
        
        result = response.json()
        assert "proportional_exists" in result
        
        if result["proportional_exists"]:
            assert result["gains"]["A"] >= 50.0
            assert result["gains"]["B"] >= 50.0
            assert "method" in result
    
    def test_solve_with_debug(self):
        """Тест решения с отладочной информацией"""
        request_data = {
            "L": 2,
            "M": 2,
            "a_d": [30, 20],
            "b_d": [25, 25],
            "a_w": [25, 25],
            "b_w": [30, 20],
            "H": 100
        }
        
        response = client.post("/api/solve?debug=true", json=request_data)
        assert response.status_code == 200
        
        result = response.json()
        assert "debug" in result
        assert "R_polygon" in result["debug"]
        assert "SP_size" in result["debug"]
    
    def test_solve_invalid_lengths(self):
        """Тест с некорректными длинами массивов"""
        request_data = {
            "L": 3,
            "M": 2,
            "a_d": [10, 20],  # неверная длина
            "b_d": [15, 15, 20],
            "a_w": [50, 50],
            "b_w": [50, 50],
            "H": 100
        }
        
        response = client.post("/api/solve", json=request_data)
        assert response.status_code == 422  # Validation error
    
    def test_solve_wrong_sum(self):
        """Тест с неправильной суммой оценок"""
        request_data = {
            "L": 2,
            "M": 0,
            "a_d": [10, 20],  # сумма = 30, должно быть 100
            "b_d": [15, 15],  # сумма = 30, должно быть 100
            "a_w": [],
            "b_w": [],
            "H": 100
        }
        
        response = client.post("/api/solve", json=request_data)
        assert response.status_code == 400  # Bad request
    
    def test_solve_only_divisible(self):
        """Тест с только делимыми пунктами"""
        request_data = {
            "L": 3,
            "M": 0,
            "a_d": [30, 40, 30],
            "b_d": [20, 30, 50],
            "a_w": [],
            "b_w": [],
            "H": 100
        }
        
        response = client.post("/api/solve", json=request_data)
        assert response.status_code == 200
        
        result = response.json()
        assert result["proportional_exists"] == True
    
    def test_solve_only_indivisible(self):
        """Тест с только неделимыми пунктами"""
        request_data = {
            "L": 0,
            "M": 4,
            "a_d": [],
            "b_d": [],
            "a_w": [25, 25, 25, 25],
            "b_w": [25, 25, 25, 25],
            "H": 100
        }
        
        response = client.post("/api/solve", json=request_data)
        assert response.status_code == 200
        
        result = response.json()
        assert result["proportional_exists"] == True
    
    def test_root_page(self):
        """Тест главной страницы"""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
