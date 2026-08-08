from utils.config import BASE_URL
import re
# from api.users_api import UsersAPI

def test_get_allusers(api_request):

    response = api_request.get(f"{BASE_URL}/api/users")
    assert response.status == 200
    assert response.status_text == 'OK'
    data = response.json()
    assert len(data) > 0
    assert "username" in data[0]
    assert "email" in data[0]
    assert "id" in data[0]

def test_get_single_user(api_request):

    users = api_request.get(f"{BASE_URL}/api/users").json()

    user_id = None
    for user in users:
        assert user["id"] != user_id
        user_id = user["id"]
        assert user["username"] == user["email"].split('@')[0]
        assert re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", user["email"])
