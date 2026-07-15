import pytest

from pages.login_page import LoginPage
from utils.config_manager import get_secure_path, get_test_password, get_test_username


@pytest.mark.smoke
def test_successful_login(page):
    """Validates successful authentication into the platform secure zone."""
    login_page = LoginPage(page)
    login_page.navigate()
    # ✅ Credentials pulled from .env via config_manager — no hardcoding
    login_page.execute_login(get_test_username(), get_test_password())
    assert "You logged into a secure area!" in login_page.get_flash_text()


@pytest.mark.regression
def test_invalid_login(page):
    """Validates that erroneous entries are blocked by system guardrails."""
    login_page = LoginPage(page)
    login_page.navigate()
    # ❌ Intentionally wrong credentials to test rejection boundary
    login_page.execute_login("invalid_user", "wrong_password")
    assert "Your username is invalid!" in login_page.get_flash_text()


# ============================================================
# 🔐 SESSION STATE BYPASS TEST
# ------------------------------------------------------------
# Uses the `authenticated_page` fixture from conftest.py.
# On first run: fixture auto-captures session via login.
# On every run after: fixture injects saved state and
# lands here already authenticated — credentials never typed.
# ============================================================
@pytest.mark.auth
def test_session_state_bypass(authenticated_page):
    """Validates that injecting saved session state bypasses the login screen entirely."""

    # 🔍 STEP 1 — Navigate to the protected zone using the pre-authenticated context
    # wait_until="domcontentloaded" skips blocking third-party ad resources on this site
    authenticated_page.goto(get_secure_path(), wait_until="domcontentloaded", timeout=60_000)

    # ⚡ STEP 2 — Confirm the browser landed inside /secure (not redirected to login)
    current_url = authenticated_page.url
    assert "/secure" in current_url, (
        f"Expected to be inside /secure but landed at: {current_url}. "
        "Session state may have expired — delete reports/auth_states/user_session.json to re-capture."
    )

    # ✅ STEP 3 — Confirm the secure page content is present in the raw DOM
    # page.content() reads the full HTML without waiting for visual rendering,
    # which is safer than locator.wait_for() after domcontentloaded.
    page_html = authenticated_page.content()
    assert "Secure Area" in page_html, "Secure Area content not found in page HTML — session state may have expired."

    # 🔒 STEP 4 — Confirm the logout link exists (only rendered when authenticated)
    logout_link = authenticated_page.locator("a[href='/logout']")
    assert logout_link.count() > 0, "Logout link not found — page did not load in an authenticated state."
