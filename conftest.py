import pytest
import requests
from data.URL import url
from data.courier_data import register_new_courier_and_return_login_password
from data.courier_data import generation_new_data_courier

@pytest.fixture
def registered_courier_data():
    login_pass = register_new_courier_and_return_login_password()
    return {
        "login": login_pass[0],
        "password": login_pass[1],
        "firstName": login_pass[2]
    }

@pytest.fixture
def delete_courier_data():
    login_pass = register_new_courier_and_return_login_password()
    yield {
        "login": login_pass[0],
        "password": login_pass[1]
    }
    response = requests.post(f"{url}/api/v1/courier/login", data=login_pass)
    if response.status_code == 200:
        courier_id = response.json().get("id")
        if courier_id:
            requests.delete(f"{url}/api/v1/courier/{courier_id}")

@pytest.fixture
def courier_data_fix():
    login_pass = generation_new_data_courier()
    yield login_pass
    response = requests.post(f"{url}/api/v1/courier/login", data=login_pass)
    if response.status_code == 200:
        courier_id = response.json().get("id")
        if courier_id:
            requests.delete(f"{url}/api/v1/courier/{courier_id}")#@pytest.fixture
#def delete_courier():
   # delete_response = requests.delete(f"{url}/api/v1/courier/{courier_id}")
   # assert delete_response.status_code == 200, "Failed to delete courier."