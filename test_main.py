import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app, User

client = TestClient(app)

# Тест для создания пользователя
def test_create_user():
    user_data = {"id": 1, "name": "Alice", "age": 30}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    assert response.json() == user_data

def test_create_user_already_exists():
    user_data = {"id": 1, "name": "Alice", "age": 30}
    client.post("/users/", json=user_data)  # Создаем пользователя

    response = client.post("/users/", json=user_data)  # Повторное создание
    assert response.status_code == 400
    assert response.json() == {"detail": "User already exists"}

# Тест для получения пользователя
def test_get_user():
    user_data = {"id": 1, "name": "Alice", "age": 30}
    client.post("/users/", json=user_data)  # Создаем пользователя

    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == user_data

def test_get_user_not_found():
    response = client.get("/users/999")  # Неизвестный пользователь
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

# Тест для обработки исключений
def test_create_user_invalid_id():
    user_data = {"id": "not_an_integer", "name": "Alice", "age": 30}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 422  # Ошибка валидации данных
