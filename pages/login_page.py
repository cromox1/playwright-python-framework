class LoginPage:

    def __init__(self,page):
        self.page = page

    def login(self,user,password):
        self.page.fill("#username",user)
        self.page.fill("#password",password)
        self.page.click("button[type='submit']")
