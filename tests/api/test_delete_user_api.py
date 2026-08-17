from utils.config import BASE_URL
from utils.test_data import TEST_FIRSTNAME
from utils.logger import get_logger
# from api.users_api import UsersAPI

logger = get_logger(__name__)

def convert_user_id_to_name(users_api, user_id):
    users_all_json = users_api.get_allusers().json()
    return [user['username'] for user in users_all_json if user['id'] == user_id][0]

def list_user_todelete(users_api, firstname):
    users_all_json = users_api.get_allusers().json()
    return [user['id'] for user in users_all_json if firstname in user['username']]

def test_delete_user(users_api):

    users_todelete = list_user_todelete(users_api, TEST_FIRSTNAME)

    if len(users_todelete) == 0:
        users_api.create_testuser(TEST_FIRSTNAME)
        users_todelete = list_user_todelete(users_api, TEST_FIRSTNAME)

    i = 1
    for user_id in users_todelete:
        logger.info(f"{i}) User to DELETE : ID = {user_id} / username = {convert_user_id_to_name(users_api, user_id)}")
        response = users_api.delete_user(user_id)
        assert response.status == 200
        assert response.status_text == 'OK'
        assert response.url.split('/')[-1] == str(user_id)
        data = response.json()
        assert data["message"] == "User deleted"
        i += 1

def test_delete_allusers_except_five(users_api):
    users_all_json = users_api.get_allusers().json()
    all_users_except_five = [u['id'] for u in users_all_json if u['id'] >= 5]
    i = 1
    for user_id in all_users_except_five:
        logger.info(f"{i}) User to DELETE : ID = {user_id} / username = {convert_user_id_to_name(users_api, user_id)}")
        response = users_api.delete_user(user_id)
        assert response.status == 200
        assert response.status_text == 'OK'
        assert response.url.split('/')[-1] == str(user_id)
        data = response.json()
        assert data["message"] == "User deleted"
        i += 1
