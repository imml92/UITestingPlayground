from playwright.sync_api import Page

class LoginPage:

    def __init__(self, page: Page):
        self.page = page
        self.page.goto("http://uitestingplayground.com/sampleapp")

        self.username = self.page.get_by_placeholder("User Name")
        self.password = self.page.get_by_placeholder("********")

        self.login_btn = self.page.get_by_role("button", name="Log In")
        self.loginstatus = self.page.locator("label#loginstatus")

    def login(self, username, password):
        self.username.fill(username)
        self.password.fill(password)

        self.login_btn.click()