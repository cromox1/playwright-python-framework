import re
from time import sleep
from api.users_api import UsersAPI
from utils.config import BASE_URL
from utils.test_data import TEST_FIRSTNAME


def test_create_user(api_request):

    for i in range(2):
        response, testuser = UsersAPI.create_testuser(api_request, TEST_FIRSTNAME)
        sleep(1)        # to make the username diff name by 1 sec
        assert response.status == 201
        assert response.status_text == 'CREATED'
        data = response.json()
        assert data["message"] == "User created"
        assert data["user"]["username"] == f"{testuser}"
        assert re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", data["user"]["email"])
