import time

import pytest

from pages.register_page import RegisterPage
from utils.config_manager import get_register_password, get_test_username


@pytest.mark.smoke
def test_register_page_loads_with_correct_title(page):
    register_page = RegisterPage(page)
    register_page.navigate()
    assert page.title() == "Test Register Page for Automation Testing Practice"
    assert "Test Register page for Automation Testing Practice" in register_page.page_heading.inner_text()


@pytest.mark.smoke
def test_register_valid_credentials_redirects_to_login(page):
    # Username must be unique per run because the sandbox retains registrations
    # indefinitely — a static name would fail on every run after the first
    username = f"tuser{int(time.time())}"
    register_page = RegisterPage(page)
    register_page.navigate()
    register_page.register(username, get_register_password(), get_register_password())
    assert "/login" in page.url
    assert "Successfully registered, you can log in now." in register_page.get_flash_text()


@pytest.mark.regression
def test_register_all_fields_empty_shows_required_error(page):
    register_page = RegisterPage(page)
    register_page.navigate()
    register_page.submit()
    assert "All fields are required." in register_page.get_flash_text()


@pytest.mark.regression
def test_register_missing_username_shows_required_error(page):
    register_page = RegisterPage(page)
    register_page.navigate()
    register_page.fill_password(get_register_password())
    register_page.fill_confirm_password(get_register_password())
    register_page.submit()
    assert "All fields are required." in register_page.get_flash_text()


@pytest.mark.regression
def test_register_missing_confirm_password_shows_required_error(page):
    register_page = RegisterPage(page)
    register_page.navigate()
    register_page.fill_username("validuser")
    register_page.fill_password(get_register_password())
    register_page.submit()
    assert "All fields are required." in register_page.get_flash_text()


@pytest.mark.regression
def test_register_mismatched_passwords_shows_mismatch_error(page):
    register_page = RegisterPage(page)
    register_page.navigate()
    register_page.register("validuser", "PasswordA1!", "PasswordB2!")
    assert "/register" in page.url
    assert "Passwords do not match." in register_page.get_flash_text()


@pytest.mark.regression
def test_register_username_too_short_shows_length_error(page):
    register_page = RegisterPage(page)
    register_page.navigate()
    register_page.register("ab", get_register_password(), get_register_password())
    assert "Username must be at least 3 characters long." in register_page.get_flash_text()


@pytest.mark.regression
@pytest.mark.parametrize(
    "bad_username",
    [
        "test_user",  # underscore not allowed
        "-testuser",  # leading hyphen not allowed
        "a" * 40,  # exceeds 39-character maximum
    ],
)
def test_register_invalid_username_format_shows_format_error(page, bad_username):
    # Uppercase letters produce a different generic server error ("An error occurred
    # during registration") rather than this format message — that inconsistency is
    # documented here so a future test can cover it if the site fixes the behaviour
    register_page = RegisterPage(page)
    register_page.navigate()
    register_page.register(bad_username, get_register_password(), get_register_password())
    assert (
        "Invalid username. Usernames can only contain lowercase letters, numbers, "
        "and single hyphens, must be between 3 and 39 characters, and cannot start "
        "or end with a hyphen."
    ) in register_page.get_flash_text()


@pytest.mark.regression
def test_register_password_too_short_shows_length_error(page):
    # "validuser" satisfies format constraints; "abc" is 3 chars, one below the minimum of 4
    register_page = RegisterPage(page)
    register_page.navigate()
    register_page.register("validuser", "abc", "abc")
    assert "Password must be at least 4 characters long." in register_page.get_flash_text()


@pytest.mark.regression
def test_register_duplicate_username_shows_taken_error(page):
    # "practice" is the pre-seeded sandbox account used across the test suite;
    # it is guaranteed to exist and avoids creating a dedicated fixture for this case
    register_page = RegisterPage(page)
    register_page.navigate()
    register_page.register(get_test_username(), get_register_password(), get_register_password())
    assert "/register" in page.url
    assert "Username is already taken." in register_page.get_flash_text()
