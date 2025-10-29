import requests
import allure
import pytest
from data.URL import url

class TestCreateOrder:

    @pytest.mark.parametrize('color', [
        ['BLACK'],
        ['GREY'],
        ['BLACK', 'GRAY'],
        []
    ])
    @allure.title('Создание заказа')
    @allure.description('Проверка, что заказ создан (код - 201 и track в ответе)')
    def test_create_order(self, color):

        payload = {
            "firstName": "Kristy",
            "lastName": "Rassudova",
            "address": "Khabarovsk, ul. Volochaevskaya",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Kommentariy",
            "color": color
        }

        r = requests.post(f"{url}/api/v1/orders", json=payload)
        assert r.status_code == 201
        assert 'track' in r.json()

        #Удаляем созданный заказ таким образом чистим данные после автотеста
        track_number = r.json().get('track') 
        order_r = requests.put(f"{url}/api/v1/orders/cancel?track={track_number}")
        assert order_r.status_code == 200