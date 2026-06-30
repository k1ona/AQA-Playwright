from pages.base_page import BasePage
from utils.config_manager import get_base_url


# ============================================================
# 🔍 STEP 1 — DROPDOWN PAGE OBJECT
# ------------------------------------------------------------
# Covers three independent dropdowns on /dropdown:
#   1. #dropdown       — Simple option picker (Option 1 / Option 2)
#   2. #elementsPerPageSelect — Items-per-page picker (10/20/50/100)
#   3. #country        — Country selection (180+ options)
# ============================================================
class DropdownPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        # 🖱️ STEP 2 — DECLARE ELEMENT LOCATORS
        # All three <select> elements confirmed from DOM inspection.
        self.simple_dropdown = page.locator("#dropdown")
        self.per_page_dropdown = page.locator("#elementsPerPageSelect")
        self.country_dropdown = page.locator("#country")

    def navigate(self):
        # 🌐 STEP 3 — NAVIGATE TO PAGE
        self.visit(f"{get_base_url()}/dropdown")

    # ============================================================
    # ⚡ STEP 4 — SELECTION HELPERS
    # ------------------------------------------------------------
    # page.locator.select_option() is the correct Playwright API
    # for <select> elements.  We wrap each dropdown so tests
    # never call raw selector strings or .select_option() directly.
    # ============================================================
    def select_simple_option(self, value: str):
        """
        Select from the simple dropdown by option VALUE attribute.
        Valid values: "1" → Option 1,  "2" → Option 2
        """
        self.logger.info(f"Selecting simple dropdown option: {value}")
        self.simple_dropdown.wait_for(state="visible")
        self.simple_dropdown.select_option(value=value)

    def select_per_page(self, value: str):
        """
        Select items-per-page count by VALUE attribute.
        Valid values: "10", "20", "50", "100"
        """
        self.logger.info(f"Selecting per-page count: {value}")
        self.per_page_dropdown.wait_for(state="visible")
        self.per_page_dropdown.select_option(value=value)

    def select_country(self, value: str):
        """
        Select a country by its ISO 2-letter VALUE attribute.
        e.g. "US" → United States,  "KZ" → Kazakhstan
        """
        self.logger.info(f"Selecting country code: {value}")
        self.country_dropdown.wait_for(state="visible")
        self.country_dropdown.select_option(value=value)

    # ============================================================
    # 🔍 STEP 5 — STATE READERS
    # ------------------------------------------------------------
    # Returns the currently selected option VALUE for each dropdown.
    # input_value() reads the live <select> element's current value.
    # ============================================================
    def get_simple_dropdown_value(self) -> str:
        return self.simple_dropdown.input_value()

    def get_per_page_value(self) -> str:
        return self.per_page_dropdown.input_value()

    def get_country_value(self) -> str:
        return self.country_dropdown.input_value()
