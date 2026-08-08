from pages.login_page import LoginPage
from pages.users_page import UsersPage
from utils.json_reader import get_user


def test_invalid_login_failure(page):

    user_invalid = get_user('invalid_user')
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(user_invalid.username, user_invalid.password)
    # Deliberately incorrect expectation
    assert "/users" not in page.url
    assert "/login" in page.url
    users_page = UsersPage(page)
    users_page.verify_page_not_login()
