from playwright.sync_api import Page, expect


class UsersPage:

    def __init__(self, page: Page):
        self.page = page
        self.page_title = page.get_by_role("heading", name="User Management")

    def verify_page_loaded(self):
        expect(self.page_title).to_be_visible()

    def verify_user_visible(self, username):
        expect(self.page.get_by_role("cell", name=username, exact=True)).to_be_visible()

    def verify_page_not_login(self):
        expect(self.page.get_by_role("button", name="Login", exact=True)).to_be_visible()
        expect(self.page.get_by_text("Invalid username or password", exact=True)).to_be_visible()