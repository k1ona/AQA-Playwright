from pages.base_page import BasePage
from utils.config_manager import get_base_url


# ============================================================
# 🔍 STEP 1 — INPUTS PAGE OBJECT
# ------------------------------------------------------------
# Covers the four input fields and two action buttons on /inputs:
#   • #input-number   — numeric input
#   • #input-text     — free text input
#   • #input-password — password input (masked)
#   • #input-date     — date picker input
#   • #btn-display-inputs — renders a summary of entered values
#   • #btn-clear-inputs   — wipes all four fields
# ============================================================
class InputsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        # 🖱️ STEP 2 — DECLARE ELEMENT LOCATORS
        # All IDs confirmed from DOM inspection of /inputs.
        self.number_input = page.locator("#input-number")
        self.text_input = page.locator("#input-text")
        self.password_input = page.locator("#input-password")
        self.date_input = page.locator("#input-date")
        self.display_button = page.locator("#btn-display-inputs")
        self.clear_button = page.locator("#btn-clear-inputs")

    def navigate(self):
        # 🌐 STEP 3 — NAVIGATE TO PAGE
        self.visit(f"{get_base_url()}/inputs")

    # ============================================================
    # ⚡ STEP 4 — INPUT FILL ACTIONS
    # ------------------------------------------------------------
    # All writes go through BasePage.type_text() which:
    #   1. Waits for visibility before interacting
    #   2. Clears any pre-filled value before typing
    # This prevents false failures from stale form state.
    # ============================================================
    def fill_number(self, value: str):
        """Enter a numeric string into the Number input field."""
        self.logger.info(f"Filling number input with: {value}")
        self.type_text(self.number_input, value)

    def fill_text(self, value: str):
        """Enter a string into the Text input field."""
        self.logger.info(f"Filling text input with: {value}")
        self.type_text(self.text_input, value)

    def fill_password(self, value: str):
        """Enter a string into the Password input field."""
        self.logger.info("Filling password input (value masked in logs)")
        self.type_text(self.password_input, value)

    def fill_date(self, value: str):
        """
        Enter a date into the Date input field.
        Format: YYYY-MM-DD (matches the HTML date input spec).
        Example: "2026-06-30"
        """
        self.logger.info(f"Filling date input with: {value}")
        self.type_text(self.date_input, value)

    # ============================================================
    # 🖱️ STEP 5 — BUTTON ACTIONS
    # ------------------------------------------------------------
    # Both buttons use click_element() from BasePage —
    # no raw locator.click() calls inside this page object.
    # ============================================================
    def click_display(self):
        """Click 'Display Inputs' to render the entered values on page."""
        self.logger.info("Clicking Display Inputs button")
        self.click_element(self.display_button)

    def click_clear(self):
        """Click 'Clear Inputs' to reset all four fields to empty."""
        self.logger.info("Clicking Clear Inputs button")
        self.click_element(self.clear_button)

    # ============================================================
    # 🔍 STEP 6 — STATE READERS
    # ------------------------------------------------------------
    # input_value() reads the live DOM value property —
    # reliable after fill actions regardless of render state.
    # ============================================================
    def get_number_value(self) -> str:
        return self.number_input.input_value()

    def get_text_value(self) -> str:
        return self.text_input.input_value()

    def get_password_value(self) -> str:
        return self.password_input.input_value()

    def get_date_value(self) -> str:
        return self.date_input.input_value()
