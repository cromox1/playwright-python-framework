from utils.config import BASE_URL
from utils.test_data import TEST_FIRSTNAME
from test_create_user_api import create_user

def list_user_todelete(api_request, firstname):
    users = api_request.get(f"{BASE_URL}/api/users").json()
    return [user['id'] for user in users if firstname in user['username']]

def test_delete_user(api_request):

    users_todelete = list_user_todelete(api_request, TEST_FIRSTNAME)

    if len(users_todelete) == 0:
        create_user(api_request, TEST_FIRSTNAME)
        users_todelete = list_user_todelete(api_request, TEST_FIRSTNAME)

    for user_id in users_todelete:
        response = api_request.delete(f"{BASE_URL}/api/users/{user_id}")
        assert response.status == 200
        assert response.status_text == 'OK'
        assert response.url.split('/')[-1] == str(user_id)
        data = response.json()
        assert data["message"] == "User deleted"
