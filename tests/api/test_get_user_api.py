import re
from utils.config import BASE_URL

def test_get_allusers(api_request):

    allusers = api_request.get(f"{BASE_URL}/api/users")
    assert allusers.status == 200
    assert allusers.status_text == 'OK'

def test_get_user_1by1(api_request):
    data_all = api_request.get(f"{BASE_URL}/api/users").json()
    list_ids = [d['id'] for d in data_all]
    for id in list_ids:
        response = api_request.get(f"{BASE_URL}/api/users/{id}")
        assert response.status == 200
        user = response.json()
        assert user["id"] == id
        assert re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", user["email"])
        assert len(user['username']) > 1
