import os
import pathlib

import pytest

from utils.auth_helper import SESSION_FILE_PATH, capture_session_automatically
from utils.config_manager import (
    get_login_path,
    get_test_password,
    get_test_username,
)

# ============================================================
# 🔍 STEP 1 — DEFINE THE SESSION FILE GATE
# ------------------------------------------------------------
# SESSION_FILE_PATH is imported from auth_helper so the path
# is always in sync with the single source of truth in that
# module.  No string duplication anywhere in the project.
# ============================================================
_SESSION_PATH = SESSION_FILE_PATH


# ============================================================
# ⚡ STEP 2 — SESSION-SCOPED AUTHENTICATED PAGE FIXTURE
# ------------------------------------------------------------
# scope="session" means ONE browser is launched for the whole
# pytest run and this fixture is initialised exactly once.
# All @pytest.mark.auth tests share this pre-authenticated
# page — zero repeated logins between individual test functions.
#
# IMPORTANT: We use the `playwright` and `browser_type_launch_args`
# fixtures provided by pytest-playwright (both session-scoped).
# Using sync_playwright() here would conflict with
# pytest-playwright's internal asyncio event loop — always
# delegate browser creation to these fixtures instead.
# ============================================================
@pytest.fixture(scope="session", autouse=True)
def allure_environment(tmp_path_factory):
    # Writing environment metadata for Allure reports. Only non-sensitive
    # values go here — BASE_URL is safe since it's the public sandbox,
    # but credentials never appear in this file.
    allure_dir = pathlib.Path("reports/allure-results")
    allure_dir.mkdir(parents=True, exist_ok=True)
    env_file = allure_dir / "environment.properties"
    env_file.write_text(
        f"Browser=Chromium\n"
        f"Python={os.sys.version.split()[0]}\n"
        f"Platform=Windows 11\n"
        f"BASE_URL={os.getenv('BASE_URL', 'https://practice.expandtesting.com')}\n"
        f"Suite=AQA-Playwright\n",
        encoding="utf-8",
    )


@pytest.fixture(scope="session")
def authenticated_page(playwright, browser_type_launch_args):
    """
    Yields a Playwright Page object already inside the secure area.

    Scenario A — Session file is MISSING:
        Runs the automated login flow via capture_session_automatically(),
        dumps cookies/localStorage to disk, then opens a fresh context
        loaded with that saved state.

    Scenario B — Session file EXISTS:
        Skips the login flow entirely and injects the saved state
        directly into a new browser context — no credentials typed.
    """

    # --------------------------------------------------------
    # 🌐 STEP 2a — LAUNCH A DEDICATED HEADED BROWSER
    # We create our own browser (separate from the function-
    # scoped browser pytest-playwright uses for `page`) so we
    # control its full lifecycle.  browser_type_launch_args
    # carries the --headed / --headless flag from the CLI so
    # our browser always matches the session mode.
    # --------------------------------------------------------
    browser = playwright.chromium.launch(**browser_type_launch_args)

    # --------------------------------------------------------
    # 🔍 STEP 2b — CHECK WHETHER SESSION FILE EXISTS
    # --------------------------------------------------------
    if not os.path.exists(_SESSION_PATH):
        print(f"\n[CONFTEST] ⚠️  No session file found at '{_SESSION_PATH}'.")
        print("[CONFTEST] 🚀 Triggering automated login to capture session state...")

        # ----------------------------------------------------
        # 🖱️ STEP 2c — AUTOMATED LOGIN + STATE CAPTURE
        # auth_helper delegates to LoginPage (BasePage wrapper)
        # so zero raw selectors appear in this conftest file.
        # ----------------------------------------------------
        capture_session_automatically(
            browser=browser,
            login_url=get_login_path(),
            username=get_test_username(),
            password=get_test_password(),
            output_path=_SESSION_PATH,
        )
    else:
        print(f"\n[CONFTEST] ✅ Session file found at '{_SESSION_PATH}' — skipping login entirely.")

    # --------------------------------------------------------
    # ✅ STEP 2d — INJECT SAVED STATE INTO A NEW CONTEXT
    # storage_state pre-loads cookies and localStorage so the
    # browser starts already authenticated — the login form
    # is never rendered or interacted with.
    # --------------------------------------------------------
    context = browser.new_context(storage_state=_SESSION_PATH)
    page = context.new_page()
    print("[CONFTEST] 🔓 Authenticated context ready — session state injected, no login required.")

    # --------------------------------------------------------
    # 🎁 STEP 2e — YIELD PAGE TO THE TEST, THEN TEAR DOWN
    # Navigation is intentionally left to the test itself so
    # any page-load issues surface as clean assertion failures
    # rather than opaque fixture-setup timeouts.
    # --------------------------------------------------------
    yield page

    context.close()
    browser.close()
