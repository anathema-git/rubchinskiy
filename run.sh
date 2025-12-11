#!/bin/bash
# Скрипт для запуска сервера

echo "Starting Fair Division System..."
echo "================================"
echo ""

# Проверка Python версии
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Проверка установки зависимостей
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

echo ""
echo "Starting uvicorn server..."
echo "Web interface: http://localhost:8000"
echo "API docs: http://localhost:8000/api/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Запуск сервера
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
