import re
from api.users_api import UsersAPI
from utils.config import BASE_URL
from utils.logger import get_logger


logger = get_logger(__name__)

def convert_id_to_name(api_request, user_id):
    allusers = api_request.get(f"{BASE_URL}/api/users")
    return [user['username'] for user in allusers.json() if user['id'] == user_id][0]

def test_get_allusers(api_request):
    allusers = api_request.get(f"{BASE_URL}/api/users")
    logger.info(f"Get ALL users -- >  GET {BASE_URL}/api/users \n\t\tALL_users = {[user['username'] for user in allusers.json()]}")
    assert allusers.status == 200
    assert allusers.status_text == 'OK'
    assert 'api' in allusers.url and 'users' in allusers.url
    assert str(allusers.url).split('users')[-1] == ''

def test_get_user_1by1(api_request):
    data_all = api_request.get(f"{BASE_URL}/api/users").json()
    list_ids = [d['id'] for d in data_all]
    i = 1
    for id in list_ids:
        response = api_request.get(f"{BASE_URL}/api/users/{id}")
        logger.info(f"{i}) User INFO : ID = {id} / username = {convert_id_to_name(api_request, id)}")
        assert response.status == 200
        user = response.json()
        assert user["id"] == id
        assert re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", user["email"])
        assert len(user['username']) > 1
        i += 1
