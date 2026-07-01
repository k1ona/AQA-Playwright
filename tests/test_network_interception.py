import pytest
import os
from playwright.sync_api import Page, expect


# The mock payload mirrors the exact shape the real notes API returns for
# an empty notes list, confirmed by hitting the live endpoint directly
# before writing this test. The point of mocking here is not to avoid
# the API call, but to control what comes back so the UI empty state is
# guaranteed to render regardless of what notes actually exist in the
# test account.
EMPTY_NOTES_RESPONSE = {
    "success": True,
    "status": 200,
    "message": "No notes found",
    "data": [],
}

NOTES_EMAIL = os.getenv("NOTES_EMAIL", "")
NOTES_PASSWORD = os.getenv("NOTES_PASSWORD", "")


@pytest.fixture
def logged_in_notes_page(page: Page):
    # Logging in directly here rather than reusing the main sandbox
    # storage_state fixture, since the notes app uses a separate
    # authentication system at /notes/app/login, not /login.
    # Locators verified by inspection: id=email, id=password.
    # Using domcontentloaded consistently with BasePage.visit() strategy
    # since the notes app also has third-party resources that slow full load.
    page.goto(
        "https://practice.expandtesting.com/notes/app/login",
        wait_until="domcontentloaded",
    )
    page.locator("#email").fill(NOTES_EMAIL)
    page.locator("#password").fill(NOTES_PASSWORD)
    page.get_by_role("button", name="Login").click()
    page.wait_for_url("**/notes/app", wait_until="domcontentloaded", timeout=60000)
    return page


@pytest.mark.smoke
def test_notes_empty_state_shown_when_api_returns_no_notes(logged_in_notes_page: Page):
    # Setting up the route intercept before reloading, so it catches
    # the API call the page makes on load rather than after.
    logged_in_notes_page.route(
        "**/notes/api/notes",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            json=EMPTY_NOTES_RESPONSE,
        ),
    )

    # Reloading after the route is registered so the intercepted response
    # controls what the UI renders, not whatever was already on screen.
    logged_in_notes_page.reload()

    expect(logged_in_notes_page.get_by_text(
        "You don't have any notes in all categories"
    )).to_be_visible()