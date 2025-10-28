import pytest
import requests
import allure
from data.URL import url
from data.courier_data import generation_new_data_courier

class TestCreateCourier:

    @allure.title('Создание курьера')
    @allure.step('Проверка создания курьера (код - 201 и текст - "ok": True')
    def test_create_courier(self, courier_data_fix):
        courier = courier_data_fix
        response = requests.post(f"{url}/api/v1/courier", data=courier)
        assert response.status_code == 201
        assert response.json() == {"ok": True}, "Неверное содержимое ответа."

    @allure.title('Проверка невозможности создать курьера. дублирующие креды')
    @allure.description('Проверка, что нельзя создать курьера с уже существующеми кредами (код - 409 и текст - "message": "Этот логин уже используетсяПопробуйте другой."')
    def test_create_courier_duplicate_login(self, registered_courier_data):
        payload = registered_courier_data
        response = requests.post(f"{url}/api/v1/courier", data=payload)

        assert response.status_code == 409
        assert response.json() == {"code": 409, "message": "Этот логин уже используется. Попробуйте другой."}, "Неверное содержимое ответа."


    @allure.title('Проверка невозможности создать курьера. Не все обязательные поля')
    @allure.description(
        'Проверка заполнения не всех обязательных полей. Курьер не создан (код - 400 и текст - "message": "Недостаточно данных для создания учетной записи"')
    @pytest.mark.parametrize("missing_field", ["password", 
                                                "login"
                                            ])
    def test_courier_with_missing_field(self, missing_field):
        data = generation_new_data_courier()
        payload = {k: data[k] for k in data if k != missing_field}
        response = requests.post(f"{url}/api/v1/courier", data=payload)

        assert response.status_code == 400
        assert response.json() == {"code": 400,
                                   "message": "Недостаточно данных для создания учетной записи"}, "Неверное содержимое ответа."