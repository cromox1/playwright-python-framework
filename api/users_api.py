from datetime import datetime
from utils.config import BASE_URL
from utils.test_data import TEST_FIRSTNAME


class UsersAPI:

    def __init__(self, request):
        self.request = request

    def get_user(self, user_id):
        return self.request.get(f"{BASE_URL}/api/users/{user_id}")

    def create_user(self, body):
        return self.request.post(f"{BASE_URL}/api/users", data=body)

    def create_testuser(api_request, firstname):
        timestamp = datetime.now().strftime("%H%M%S")
        testuser = firstname + '_' + timestamp

        return api_request.post(
            f"{BASE_URL}/api/users",
            data={"username": f"{testuser}", "password": "Password123",
                  "email": f"{testuser}@rosli-laptop.com.my"}
        ), testuser
