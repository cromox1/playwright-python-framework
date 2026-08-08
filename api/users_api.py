# api/users_api.py

class UsersAPI:

    def __init__(self, request):
        self.request = request

    def get_user(self, user_id):
        return self.request.get(
            f"https://reqres.in/api/users/{user_id}"
        )

    def create_user(self, body):
        return self.request.post(
            "https://reqres.in/api/users",
            data=body
        )
