from pages.login_page import LoginPage
from pages.users_page import UsersPage
from api.users_api import UsersAPI
from utils.json_reader import get_user
from utils.config import BASE_URL
from time import sleep
import requests
from datetime import datetime
timestamp = datetime.now().strftime("%H%M%S")


def get_list_allusers():
    return requests.get(url=f"{BASE_URL}/api/users", headers={'Accept': 'application/json'})

def login_page_then_validate(page, list_users):
    allusers = get_list_allusers()
    allusers_list = [i['username'] for i in allusers.json()]
    print(f"ALLUSERS = {allusers.json()}")
    print(f"ALLUSERS_LIST = {allusers_list}")
    for userx in list_users:
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(userx.username, userx.password)
        users_page = UsersPage(page)
        sleep(1)
        print(f"USERX = {userx}")
        if not users_page.verify_page_not_login:
            print(f"User [ {userx.username} ] ABLE to LOGIN")
            assert "/users" in page.url
            assert "/login" not in page.url
            users_page.verify_page_loaded()
            users_page.verify_user_visible(userx.username)
        else:
            print(f"User [ {userx.username} / {userx.password} ] CANNOT LOGIN")
            if str(userx.username) not in allusers_list:
                tstamp = datetime.now().strftime("%H%M%S")
                url1 = f"{BASE_URL}/api/users"
                headers1 = {'Accept': 'application/json'}
                data1 = {"username": f"{userx.username}", "password": f"{userx.password}",
                         "email": f"{userx.username}_{tstamp}@rosli-laptop.com.my"}
                print(f"URL = {url1}")
                print(f"DATA = {data1}")
                response = requests.post(url=url1, json=data1, headers=headers1)
                assert response.status_code == 201
            sleep(1)
            login_page = LoginPage(page)
            login_page.open()
            login_page.login(userx.username, userx.password)
            users_page = UsersPage(page)
            print(f"NOW - User [ {userx.username} ] ABLE to LOGIN")
            assert "/users" in page.url
            assert "/login" not in page.url
            users_page.verify_page_loaded()
            users_page.verify_user_visible(userx.username)


def test_valid_login_validusers(page):
    login_page_then_validate(page, [get_user('valid_user')])

def test_valid_login_integers_user(page):
    login_page_then_validate(page, [get_user('integers_user')])

def test_valid_login_integers_pswd(page):
    login_page_then_validate(page, [get_user('integers_pswd')])
