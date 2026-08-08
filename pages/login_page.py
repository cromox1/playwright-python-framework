from utils.config import BASE_URL


class LoginPage:

    def __init__(self,page):
        self.page = page
        self.username = page.locator("#username")
        self.password = page.locator("#password")
        # self.login_button = page.locator("#login-button")
        self.login_button = page.get_by_role("button", name="Login", exact=True)
        self.login_error = page.locator("#login-error")

    def open(self):
        self.page.goto(f"{BASE_URL}/login")

    def login(self,loginuser,pswduser):
        self.username.fill(loginuser)
        self.password.fill(pswduser)
        self.login_button.click()

    def get_error_message(self):
        return self.login_error.text_content()
