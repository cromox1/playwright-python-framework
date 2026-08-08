from pages.login_page import LoginPage
from pages.users_page import UsersPage
from utils.json_reader import get_user


def test_valid_login(page):

    user_valid = get_user('valid_user')
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(user_valid.username, user_valid.password)
    assert "/users" in page.url
    assert "/login" not in page.url
    users_page = UsersPage(page)
    users_page.verify_page_loaded()
    users_page.verify_user_visible(user_valid.username)

def test_login(page):
    login_page = LoginPage(page)
    login_page.open()
    assert "Google" in page.title()
