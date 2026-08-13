from pages.login_page import LoginPage
from pages.users_page import UsersPage
from utils.json_reader import get_user


def test_invalid_login_failure(page):

    for userx in [get_user('invalid_user'), get_user('verylong_user'), get_user('verylong_pswd'), get_user("tooshort_user"), get_user("tooshort_pswd")]:
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(userx.username, userx.password)
        # Deliberately incorrect expectation
        assert "/users" not in page.url
        assert "/login" in page.url
        users_page = UsersPage(page)
        users_page.verify_page_not_login()
