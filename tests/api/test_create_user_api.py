from datetime import datetime
import re
from utils.config import BASE_URL
from utils.test_data import TEST_FIRSTNAME

def create_user(api_request, firstname):
    timestamp = datetime.now().strftime("%H%M%S")
    testuser = firstname + '_' + timestamp

    return api_request.post(
        f"{BASE_URL}/api/users",
        data={"username": f"{testuser}", "password": "Password123",
              "email": f"{testuser}@rosli-laptop.com.my"}
    ), testuser

def test_create_user(api_request):

    response, testuser = create_user(api_request, TEST_FIRSTNAME)

    assert response.status == 201
    assert response.status_text == 'CREATED'
    data = response.json()
    assert data["message"] == "User created"
    assert data["user"]["username"] == f"{testuser}"
    assert re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", data["user"]["email"])