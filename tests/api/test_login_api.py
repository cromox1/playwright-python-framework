# from sqlalchemy.testing.provision import drop_db
from utils.config import BASE_URL

def test_valid_login(api_request):

    response = api_request.post(f"{BASE_URL}/api/login", data={"username": "cromox1", "password": "Password123"})
    assert response.status == 200
    assert response.status_text == 'OK'
    data = response.json()
    assert data["success"] is True
    assert data["message"] == 'Login successful'
    assert data["user"]["username"] == "cromox1"
    assert "cromox1" in data["user"]["email"]

def test_invalid_login(api_request):

    response = api_request.post(f"{BASE_URL}/api/login", data={"username": "cromox1", "password": "WrongPassword"})
    assert response.status == 401
    assert response.status_text == 'UNAUTHORIZED'
    data = response.json()
    assert data["success"] is False
    assert data["message"] == 'Invalid username or password'
    assert "user" not in data       # assert key "user" does not exist in data
