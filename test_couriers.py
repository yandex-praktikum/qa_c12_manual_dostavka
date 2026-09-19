"""Стартовые тесты клиента из предыдущего спринта."""

import os

import pytest
import requests
from dotenv import load_dotenv

from api_client import CourierAPIClient

load_dotenv()


@pytest.fixture
def client():
    """Создаёт клиент API для каждого теста."""
    base_url = os.getenv("API_BASE_URL", "http://127.0.0.1:5001/api")
    token = os.getenv("AUTH_TOKEN", "test_token_123")
    return CourierAPIClient(base_url, token)


@pytest.fixture
def new_courier_data():
    """Возвращает данные для создания курьера."""
    return {
        "first_name": "Мария",
        "last_name": "Сидорова",
        "phone": "+79997654321",
    }


@pytest.mark.usefixtures("fake_server")
class TestCourierClient:
    """Проверяет получение, создание и удаление курьера."""

    def test_get_courier_by_id(self, client):
        """Получает курьера, который уже есть на сервере."""
        courier = client.get_courier_by_id(1)
        assert courier["id"] == 1, "Убедитесь, что получен курьер с id=1."
        assert courier["first_name"] == "Иван", (
            "Убедитесь, что API вернул правильное имя курьера."
        )

    def test_create_courier(self, client, new_courier_data):
        """Создаёт курьера с переданными данными."""
        result = client.create_courier(new_courier_data)
        assert "id" in result, "Убедитесь, что у созданного курьера есть id."
        assert result["first_name"] == new_courier_data["first_name"], (
            "Убедитесь, что имя созданного курьера совпадает с переданным."
        )

    def test_get_nonexistent_courier_raises(self, client):
        """Ожидает HTTPError при запросе несуществующего курьера."""
        with pytest.raises(requests.exceptions.HTTPError):
            client.get_courier_by_id(99999)

    def test_delete_courier(self, client):
        """Удаляет курьера, который уже есть на сервере."""
        result = client.delete_courier(2)
        assert result == {"status": "deleted"}, (
            "Убедитесь, что API подтвердил удаление курьера."
        )
