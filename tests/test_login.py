from pages.login_page import LoginPage
from utils.json_reader import get_user

def test_login(page):
    user_valid = get_user('valid_user')
    page.goto("https://the-internet.herokuapp.com/login")
    login = LoginPage(page)
    login.login(user_valid.username, user_valid.password)
    assert "secure" in page.url
