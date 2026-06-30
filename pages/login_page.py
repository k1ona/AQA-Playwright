from pages.base_page import BasePage

# ============================================================
# 🔍 STEP 1 — IMPORT THE DYNAMIC CONFIGURATION LOADER
# ------------------------------------------------------------
# config_manager reads BASE_URL from the root .env file so we
# never hardcode environment-specific URLs inside page objects.
# ============================================================
from utils.config_manager import get_login_path


# ============================================================
# ⚡ STEP 2 — DEFINE THE LOGIN PAGE WITH DYNAMIC URL
# ------------------------------------------------------------
# LoginPage inherits all safe wrapped actions from BasePage.
# The login URL is resolved at runtime by get_login_path(),
# which assembles it from BASE_URL defined in the .env file.
# ============================================================
class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # 🖱️ STEP 3 — DECLARE ELEMENT LOCATORS
        # Selectors based on real DOM inspector configurations
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("button[type='submit']")
        self.flash_message = page.locator("#flash")

    def navigate(self):
        # 🌐 URL is resolved dynamically — no hardcoded strings here
        self.visit(get_login_path())

    def execute_login(self, username, password):
        """Self-documenting login sequence utilizing parent action wrappers."""
        self.type_text(self.username_input, username)
        self.type_text(self.password_input, password)
        self.click_element(self.login_button)

    def get_flash_text(self):
        # Target the inner container text directly
        self.flash_message.wait_for(state="visible")
        return self.flash_message.inner_text()
