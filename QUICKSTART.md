# Быстрый старт

## Установка и запуск

### 1. Установка зависимостей

```bash
# Создание виртуального окружения
python3 -m venv venv

# Активация виртуального окружения
source venv/bin/activate  # Linux/Mac

# Установка зависимостей
pip install -r requirements.txt
```

### 2. Запуск сервера

#### Вариант 1: Используя скрипт

```bash
./run.sh
```

#### Вариант 2: Напрямую через Python

```bash
python app/main.py
```

#### Вариант 3: Используя uvicorn

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Открытие веб-интерфейса

После запуска откройте браузер и перейдите по адресу:
- **Веб-интерфейс:** http://localhost:8000
- **API документация:** http://localhost:8000/api/docs
- **ReDoc:** http://localhost:8000/api/redoc

## Тестирование

### Запуск тестов

```bash
# Установка тестовых зависимостей (если не установлены)
pip install pytest pytest-asyncio httpx

# Запуск всех тестов
pytest tests/ -v

# Запуск тестов алгоритмов
pytest tests/test_fair_division.py -v

# Запуск API тестов
pytest tests/test_api.py -v
```

## Примеры использования

### Пример 1: Веб-интерфейс

1. Откройте http://localhost:8000
2. Нажмите "Загрузить пример"
3. Нажмите "Решить"
4. Увидите результат с распределением пунктов и выигрышами

### Пример 2: Curl запрос к API

```bash
curl -X POST "http://localhost:8000/api/solve" \
  -H "Content-Type: application/json" \
  -d '{
    "L": 3,
    "M": 4,
    "a_d": [10, 20, 30],
    "b_d": [15, 15, 20],
    "a_w": [35, 30, 15, 20],
    "b_w": [18, 20, 12, 25],
    "H": 100
  }'
```

### Пример 3: Python клиент

```python
import requests
import json

# URL API
url = "http://localhost:8000/api/solve"

# Данные задачи
data = {
    "L": 3,
    "M": 4,
    "a_d": [10, 20, 30],
    "b_d": [15, 15, 20],
    "a_w": [35, 30, 15, 20],
    "b_w": [18, 20, 12, 25],
    "H": 100
}

# Отправка запроса
response = requests.post(url, json=data)

# Вывод результата
result = response.json()
print(json.dumps(result, indent=2, ensure_ascii=False))

# Проверка результата
if result["proportional_exists"]:
    print(f"\n✓ Пропорциональный делёж найден!")
    print(f"Выигрыш A: {result['gains']['A']}")
    print(f"Выигрыш B: {result['gains']['B']}")
    print(f"Метод: {result['method']}")
else:
    print("\n✗ Пропорциональный делёж не существует")
```

## Проверка корректности работы

### 1. Проверка здоровья сервиса

```bash
curl http://localhost:8000/health
```

Ожидаемый ответ:
```json
{"status": "healthy", "version": "1.0.0"}
```

### 2. Получение информации о системе

```bash
curl http://localhost:8000/api/info
```

### 3. Запуск тестового примера

Используйте пример из ТЗ (раздел 6):

```json
{
  "L": 3,
  "M": 4,
  "a_d": [10, 20, 30],
  "b_d": [15, 15, 20],
  "a_w": [35, 30, 15, 20],
  "b_w": [18, 20, 12, 25],
  "H": 100
}
```

Ожидаемый результат:
- `proportional_exists: true`
- `gains.A >= 50`
- `gains.B >= 50`

## Устранение неполадок

### Проблема: ModuleNotFoundError

**Решение:**
```bash
# Убедитесь, что виртуальное окружение активировано
source venv/bin/activate

# Переустановите зависимости
pip install -r requirements.txt
```

### Проблема: Порт 8000 уже занят

**Решение:** Используйте другой порт
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### Проблема: Тесты не запускаются

**Решение:**
```bash
# Убедитесь, что pytest установлен
pip install pytest pytest-asyncio httpx

# Запустите из корневой директории проекта
cd /home/anathema/rubchinskiy
pytest tests/ -v
```

## Структура проекта

```
rubchinskiy/
├── app/                          # FastAPI приложение
│   ├── main.py                  # Главный модуль
│   ├── api/
│   │   └── endpoints.py         # API endpoints
│   ├── models/
│   │   ├── request_models.py    # Модели запросов
│   │   └── response_models.py   # Модели ответов
│   ├── core/
│   │   └── config.py            # Конфигурация
│   └── templates/
│       └── index.html           # Главная страница
│
├── fair_division_engine/         # Математический движок
│   ├── __init__.py
│   ├── r_polygon.py             # Построение ломаной R
│   ├── indivisible.py           # Генерация множества S
│   ├── pareto.py                # Парето-фильтрация
│   ├── proportional.py          # Проверка пропорциональности
│   └── utils.py                 # Вспомогательные функции
│
├── static/                       # Статические файлы
│   ├── styles.css               # CSS стили
│   └── script.js                # JavaScript
│
├── tests/                        # Тесты
│   ├── test_fair_division.py    # Тесты алгоритмов
│   └── test_api.py              # Тесты API
│
├── requirements.txt              # Зависимости Python
├── README.md                     # Документация
├── QUICKSTART.md                 # Этот файл
├── run.sh                        # Скрипт запуска
└── .gitignore                    # Git ignore
```

## Дополнительная информация

- **Документация алгоритма:** README.md
- **Научная работа:** 101017_Fair_division - preprint.pdf
- **Методичка:** Проверка пропорциональности.docx

## Поддержка

При возникновении вопросов или проблем:
1. Проверьте логи в консоли
2. Изучите API документацию: http://localhost:8000/api/docs
3. Запустите тесты для проверки корректности установки
4. Проверьте версию Python (требуется Python 3.11+)
