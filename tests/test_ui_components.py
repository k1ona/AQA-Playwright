import pytest
from pages.checkboxes_page import CheckboxesPage
from pages.dropdown_page import DropdownPage
from pages.inputs_page import InputsPage


# ╔══════════════════════════════════════════════════════════════╗
# ║              CHECKBOXES TESTS                               ║
# ╚══════════════════════════════════════════════════════════════╝

@pytest.mark.smoke
def test_checkbox1_default_state_is_unchecked(page):
    """
    Validates that checkbox 1 is unchecked on initial page load.
    This is the BASELINE state — the page always resets on navigate().
    """
    # 🔍 STEP 1 — Navigate to the checkboxes practice page
    checkboxes_page = CheckboxesPage(page)
    checkboxes_page.navigate()

    # ✅ STEP 2 — Assert default state: checkbox 1 must be unchecked
    assert not checkboxes_page.is_checkbox1_checked(), (
        "Expected checkbox 1 to be UNCHECKED on load, but it was checked."
    )


@pytest.mark.smoke
def test_checkbox2_default_state_is_checked(page):
    """
    Validates that checkbox 2 is checked on initial page load.
    The DOM sets the 'checked' attribute on this element by default.
    """
    # 🔍 STEP 1 — Navigate to the checkboxes practice page
    checkboxes_page = CheckboxesPage(page)
    checkboxes_page.navigate()

    # ✅ STEP 2 — Assert default state: checkbox 2 must be checked
    assert checkboxes_page.is_checkbox2_checked(), (
        "Expected checkbox 2 to be CHECKED on load, but it was unchecked."
    )


@pytest.mark.regression
def test_toggle_checkbox1_on_then_off(page):
    """
    Validates that clicking checkbox 1 twice returns it to its original state.
    Tests the full click → unclick cycle (unchecked → checked → unchecked).
    """
    # 🔍 STEP 1 — Navigate and confirm starting state
    checkboxes_page = CheckboxesPage(page)
    checkboxes_page.navigate()
    assert not checkboxes_page.is_checkbox1_checked(), "Pre-condition failed: checkbox 1 should start unchecked."

    # ⚡ STEP 2 — First toggle: unchecked → checked
    checkboxes_page.toggle_checkbox1()
    assert checkboxes_page.is_checkbox1_checked(), (
        "After first click, checkbox 1 should be CHECKED."
    )

    # 🖱️ STEP 3 — Second toggle: checked → unchecked
    checkboxes_page.toggle_checkbox1()
    assert not checkboxes_page.is_checkbox1_checked(), (
        "After second click, checkbox 1 should be UNCHECKED again."
    )


@pytest.mark.regression
def test_toggle_checkbox2_off(page):
    """
    Validates that clicking checkbox 2 (which starts checked) unchecks it.
    """
    # 🔍 STEP 1 — Navigate and confirm starting state
    checkboxes_page = CheckboxesPage(page)
    checkboxes_page.navigate()
    assert checkboxes_page.is_checkbox2_checked(), "Pre-condition failed: checkbox 2 should start checked."

    # ⚡ STEP 2 — Toggle: checked → unchecked
    checkboxes_page.toggle_checkbox2()
    assert not checkboxes_page.is_checkbox2_checked(), (
        "After clicking, checkbox 2 should be UNCHECKED."
    )


# ╔══════════════════════════════════════════════════════════════╗
# ║              DROPDOWN TESTS                                 ║
# ╚══════════════════════════════════════════════════════════════╝

@pytest.mark.smoke
def test_simple_dropdown_select_option1(page):
    """
    Validates selecting 'Option 1' from the simple dropdown.
    Checks the live DOM value, not the visible label text.
    """
    # 🔍 STEP 1 — Navigate to the dropdown practice page
    dropdown_page = DropdownPage(page)
    dropdown_page.navigate()

    # ⚡ STEP 2 — Select Option 1 by value attribute
    dropdown_page.select_simple_option("1")

    # ✅ STEP 3 — Assert the live DOM value reflects the selection
    assert dropdown_page.get_simple_dropdown_value() == "1", (
        "Expected simple dropdown value to be '1' (Option 1)."
    )


@pytest.mark.regression
def test_simple_dropdown_select_option2(page):
    """
    Validates selecting 'Option 2' from the simple dropdown.
    """
    # 🔍 STEP 1 — Navigate
    dropdown_page = DropdownPage(page)
    dropdown_page.navigate()

    # ⚡ STEP 2 — Select Option 2 by value attribute
    dropdown_page.select_simple_option("2")

    # ✅ STEP 3 — Assert value
    assert dropdown_page.get_simple_dropdown_value() == "2", (
        "Expected simple dropdown value to be '2' (Option 2)."
    )


@pytest.mark.regression
def test_per_page_dropdown_select_50(page):
    """
    Validates selecting '50' from the elements-per-page dropdown.
    """
    # 🔍 STEP 1 — Navigate
    dropdown_page = DropdownPage(page)
    dropdown_page.navigate()

    # ⚡ STEP 2 — Select 50 items per page
    dropdown_page.select_per_page("50")

    # ✅ STEP 3 — Assert value
    assert dropdown_page.get_per_page_value() == "50", (
        "Expected per-page dropdown to show value '50'."
    )


@pytest.mark.regression
def test_country_dropdown_select_kazakhstan(page):
    """
    Validates selecting Kazakhstan (value='KZ') from the country dropdown.
    Tests a non-trivial country that requires scrolling the long list.
    """
    # 🔍 STEP 1 — Navigate
    dropdown_page = DropdownPage(page)
    dropdown_page.navigate()

    # ⚡ STEP 2 — Select Kazakhstan by ISO code
    dropdown_page.select_country("KZ")

    # ✅ STEP 3 — Assert value
    assert dropdown_page.get_country_value() == "KZ", (
        "Expected country dropdown to show value 'KZ' (Kazakhstan)."
    )


# ╔══════════════════════════════════════════════════════════════╗
# ║              INPUTS TESTS                                   ║
# ╚══════════════════════════════════════════════════════════════╝

@pytest.mark.smoke
def test_inputs_fill_number_field(page):
    """
    Validates that a number can be typed into the Number input
    and the DOM reflects the entered value.
    """
    # 🔍 STEP 1 — Navigate to the inputs practice page
    inputs_page = InputsPage(page)
    inputs_page.navigate()

    # ⚡ STEP 2 — Fill the number input field
    inputs_page.fill_number("42")

    # ✅ STEP 3 — Assert the DOM value matches what we typed
    assert inputs_page.get_number_value() == "42", (
        "Expected number input to contain '42' after fill."
    )


@pytest.mark.smoke
def test_inputs_fill_text_field(page):
    """
    Validates that arbitrary text can be typed into the Text input.
    """
    # 🔍 STEP 1 — Navigate
    inputs_page = InputsPage(page)
    inputs_page.navigate()

    # ⚡ STEP 2 — Fill the text input
    inputs_page.fill_text("Hello Playwright")

    # ✅ STEP 3 — Assert
    assert inputs_page.get_text_value() == "Hello Playwright", (
        "Expected text input to contain 'Hello Playwright'."
    )


@pytest.mark.regression
def test_inputs_fill_password_field(page):
    """
    Validates that the password field accepts input.
    Note: the field type is 'password' so the value is masked visually
    but is still readable via input_value() in Playwright.
    """
    # 🔍 STEP 1 — Navigate
    inputs_page = InputsPage(page)
    inputs_page.navigate()

    # ⚡ STEP 2 — Fill the password input
    inputs_page.fill_password("S3cr3tPass!")

    # ✅ STEP 3 — Assert the DOM value (not the masked display)
    assert inputs_page.get_password_value() == "S3cr3tPass!", (
        "Expected password input to hold 'S3cr3tPass!' in the DOM."
    )


@pytest.mark.regression
def test_inputs_fill_date_field(page):
    """
    Validates that a date string in YYYY-MM-DD format is accepted
    by the date input and reflected in the DOM.
    """
    # 🔍 STEP 1 — Navigate
    inputs_page = InputsPage(page)
    inputs_page.navigate()

    # ⚡ STEP 2 — Fill the date field (ISO format required by HTML date inputs)
    inputs_page.fill_date("2026-06-30")

    # ✅ STEP 3 — Assert
    assert inputs_page.get_date_value() == "2026-06-30", (
        "Expected date input to hold '2026-06-30'."
    )


@pytest.mark.regression
def test_inputs_clear_button_resets_all_fields(page):
    """
    Validates that clicking 'Clear Inputs' empties all four fields.
    Fills every field first, then asserts all are empty after clearing.
    """
    # 🔍 STEP 1 — Navigate and fill all four fields
    inputs_page = InputsPage(page)
    inputs_page.navigate()
    inputs_page.fill_number("99")
    inputs_page.fill_text("Test value")
    inputs_page.fill_password("TempPass1")
    inputs_page.fill_date("2026-01-01")

    # ⚡ STEP 2 — Click the Clear button
    inputs_page.click_clear()

    # ✅ STEP 3 — Assert all fields are now empty
    assert inputs_page.get_number_value()   == "", "Number field should be empty after clear."
    assert inputs_page.get_text_value()     == "", "Text field should be empty after clear."
    assert inputs_page.get_password_value() == "", "Password field should be empty after clear."
    assert inputs_page.get_date_value()     == "", "Date field should be empty after clear."
