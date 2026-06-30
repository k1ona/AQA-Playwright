from pages.base_page import BasePage
from utils.config_manager import get_base_url


# ============================================================
# 🔍 STEP 1 — CHECKBOXES PAGE OBJECT
# ------------------------------------------------------------
# Inherits all safe interaction wrappers from BasePage.
# URL is assembled at runtime from BASE_URL in .env —
# never hardcoded inside this file.
# ============================================================
class CheckboxesPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        # 🖱️ STEP 2 — DECLARE ELEMENT LOCATORS
        # Selectors confirmed from DOM inspection of /checkboxes.
        # checkbox1 is UNCHECKED by default on page load.
        # checkbox2 is CHECKED by default on page load.
        self.checkbox1 = page.locator("#checkbox1")
        self.checkbox2 = page.locator("#checkbox2")

    def navigate(self):
        # 🌐 STEP 3 — NAVIGATE TO PAGE
        # Uses BasePage.visit() which enforces domcontentloaded
        # strategy — safe for ad-heavy sandbox pages.
        self.visit(f"{get_base_url()}/checkboxes")

    # ============================================================
    # ⚡ STEP 4 — CHECKBOX STATE READER
    # ------------------------------------------------------------
    # Returns True/False based on the DOM checked property.
    # Uses locator.is_checked() — the correct Playwright method
    # for checkbox state, NOT .get_attribute("checked") which
    # only reads the HTML attribute, not the live DOM property.
    # ============================================================
    def is_checkbox1_checked(self) -> bool:
        return self.checkbox1.is_checked()

    def is_checkbox2_checked(self) -> bool:
        return self.checkbox2.is_checked()

    # ============================================================
    # 🖱️ STEP 5 — CHECKBOX TOGGLE ACTIONS
    # ------------------------------------------------------------
    # Uses the inherited click_element() wrapper from BasePage
    # so we never call raw locator.click() inside page objects.
    # ============================================================
    def toggle_checkbox1(self):
        """Click checkbox 1 to flip its checked state."""
        self.logger.info("Toggling checkbox 1")
        self.click_element(self.checkbox1)

    def toggle_checkbox2(self):
        """Click checkbox 2 to flip its checked state."""
        self.logger.info("Toggling checkbox 2")
        self.click_element(self.checkbox2)
