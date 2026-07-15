import os

from playwright.sync_api import Browser, sync_playwright

# ============================================================
# 🔍 STEP 1 — DEFINE THE CANONICAL SESSION FILE PATH
# ------------------------------------------------------------
# This single constant is the only place that knows where the
# session JSON lives on disk.  Import it anywhere you need the
# path instead of duplicating the string across the project.
# ============================================================
SESSION_FILE_PATH = os.path.join("reports", "auth_states", "user_session.json")


# ============================================================
# ⚡ STEP 2 — AUTOMATED SESSION CAPTURE (HEADLESS-SAFE)
# ------------------------------------------------------------
# Accepts an already-running Playwright Browser object so the
# caller controls the launch mode (headed vs headless, etc.).
# Uses the LoginPage abstraction to stay within our CLAUDE.md
# "no raw selectors" contract — zero page.fill() calls here.
# ============================================================
def capture_session_automatically(
    browser: Browser,
    login_url: str,
    username: str,
    password: str,
    output_path: str = SESSION_FILE_PATH,
) -> None:
    """
    Silently logs in via the LoginPage abstraction, then dumps
    cookies + localStorage to disk as a reusable session file.

    Parameters
    ----------
    browser     : Active Playwright Browser instance from the caller.
    login_url   : Full URL of the login form (e.g. .../login).
    username    : Plaintext username credential string.
    password    : Plaintext password credential string.
    output_path : Destination path for the session JSON file.
    """
    # --------------------------------------------------------
    # 🖱️ STEP 2a — PREPARE OUTPUT DIRECTORY
    # --------------------------------------------------------
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # --------------------------------------------------------
    # 🌐 STEP 2b — OPEN A FRESH BROWSER CONTEXT AND LOG IN
    # We import LoginPage here (lazy) to avoid a circular-
    # import at module load time while keeping the proper
    # page-object abstraction fully intact.
    # --------------------------------------------------------
    from pages.login_page import LoginPage

    context = browser.new_context()
    page = context.new_page()

    print(f"\n[AUTH] 🚀 Launching automated login sequence → {login_url}")
    login_page_obj = LoginPage(page)
    login_page_obj.navigate()
    login_page_obj.execute_login(username, password)

    # --------------------------------------------------------
    # ✅ STEP 2c — WAIT FOR POST-LOGIN REDIRECT, THEN SAVE
    # wait_for_url confirms we actually reached the secure
    # zone before dumping state — guards against silent fails.
    # --------------------------------------------------------
    page.wait_for_url("**/secure", timeout=10_000)
    context.storage_state(path=output_path)
    print(f"[AUTH] ✅ Session state saved to: {output_path}")

    context.close()


# ============================================================
# 🧑‍💻 STEP 3 — MANUAL SESSION CAPTURE (HUMAN-IN-THE-LOOP)
# ------------------------------------------------------------
# Use this when the target site has a CAPTCHA, SSO, or MFA
# that automated scripts cannot navigate.  The function opens
# a visible browser, lets you log in yourself, and saves the
# resulting cookies when you type SAVE in the terminal.
# ============================================================
def save_session_state(
    target_url: str,
    output_json_name: str = "user_session.json",
) -> None:
    """
    Launches a headed browser for manual authentication.
    Type SAVE in the terminal once you are fully logged in.
    """
    output_dir = os.path.join("reports", "auth_states")
    os.makedirs(output_dir, exist_ok=True)
    state_path = os.path.join(output_dir, output_json_name)

    print("\n[INFO] 🌐 Launching Chromium for manual login. Complete authentication in the browser window.")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(target_url)

        print(f"[ACTION] URL Loaded: {target_url}")
        print("[ACTION] Please log in now. This script will wait for you to finish.")

        try:
            while True:
                user_input = input("Type 'SAVE' and press Enter once you are successfully logged in: ")
                if user_input.strip().upper() == "SAVE":
                    context.storage_state(path=state_path)
                    print(f"[SUCCESS] ✅ Auth tokens and cookies saved to: {state_path}")
                    break
        except KeyboardInterrupt:
            print("\n[WARNING] ⚠️  Script cancelled. Session state was NOT saved.")
        finally:
            browser.close()


# ============================================================
# 🔧 STEP 4 — STANDALONE ENTRY POINT FOR MANUAL USE
# ------------------------------------------------------------
# Run this file directly from the terminal to capture a manual
# session without needing to modify any test code:
#   python utils/auth_helper.py
# ============================================================
if __name__ == "__main__":
    from utils.config_manager import get_login_path

    save_session_state(get_login_path())
