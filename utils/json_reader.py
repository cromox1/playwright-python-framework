import json
from pathlib import Path
from models.user import User

def get_user(user_type):
    file_path = Path(__file__).parent.parent / "data" / "users.json"

    with open(file_path, "r") as file:
        users = json.load(file)

    user = users[user_type]

    return User(
        user['username'],
        user['password']
    )

def get_user_all():
    file_path = Path(__file__).parent.parent / "data" / "users.json"

    with open(file_path, "r") as file:
        users = json.load(file)

    return users
