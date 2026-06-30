from pages.base_page import BasePage
from utils.config_manager import get_register_path


class RegisterPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        # confirmPassword is camelCase in the DOM — not a typo
        self.confirm_password_input = page.locator("#confirmPassword")
        self.register_button = page.locator("button[type='submit']")
        # #flash is the inner alert div, same id convention the login page uses
        self.flash_message = page.locator("#flash")
        self.page_heading = page.locator("h1")

    def navigate(self):
        self.visit(get_register_path())

    def fill_username(self, username: str):
        self.type_text(self.username_input, username)

    def fill_password(self, password: str):
        self.type_text(self.password_input, password)

    def fill_confirm_password(self, confirm: str):
        self.type_text(self.confirm_password_input, confirm)

    def submit(self):
        self.click_element(self.register_button)

    def register(self, username: str, password: str, confirm_password: str):
        # Three separate params rather than a single password so mismatched-password
        # tests can pass two different values without a workaround
        self.fill_username(username)
        self.fill_password(password)
        self.fill_confirm_password(confirm_password)
        self.submit()

    def get_flash_text(self) -> str:
        # The flash div only exists after a POST-redirect cycle, so waiting for
        # visible is safe here — the page has already fully re-rendered by this point
        self.flash_message.wait_for(state="visible")
        return self.flash_message.inner_text().strip()
