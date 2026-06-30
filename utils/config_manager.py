import os
from pathlib import Path

# ============================================================
# 🔍 STEP 1 — LOCATE THE ROOT .env FILE
# ------------------------------------------------------------
# We walk up from this file's directory to find the project
# root. This keeps the loader working regardless of how deep
# inside the repo we are when the module is imported.
# ============================================================
_ROOT_DIR = Path(__file__).resolve().parent.parent
_ENV_FILE = _ROOT_DIR / ".env"

# ============================================================
# ⚡ STEP 2 — LOAD .env INTO THE PROCESS ENVIRONMENT
# ------------------------------------------------------------
# python-dotenv reads KEY=VALUE pairs from the .env file and
# injects them into os.environ so every part of the framework
# can reach them via os.getenv().  If the file is missing we
# print a friendly warning and carry on — the framework will
# fall back to whatever is already in the shell environment.
# ============================================================
try:
    from dotenv import load_dotenv
    if _ENV_FILE.exists():
        load_dotenv(dotenv_path=_ENV_FILE, override=False)
        print(f"[CONFIG] ✅ Loaded environment variables from: {_ENV_FILE}")
    else:
        print(f"[CONFIG] ⚠️  No .env file found at {_ENV_FILE} — relying on shell environment variables.")
except ImportError:
    print("[CONFIG] ⚠️  python-dotenv is not installed. Run: pip install python-dotenv")


# ============================================================
# 🖱️ STEP 3 — EXPOSE CLEAN GETTER FUNCTIONS
# ------------------------------------------------------------
# Tests and page objects should call these functions rather
# than touching os.getenv() directly.  Each getter has a safe
# fallback value so the suite never crashes with a KeyError.
# ============================================================
def get_base_url() -> str:
    """Return the application root URL defined in .env (BASE_URL)."""
    return os.getenv("BASE_URL", "https://expandtesting.com")


def get_login_path() -> str:
    """Return the full URL of the login page."""
    return f"{get_base_url()}/login"


def get_secure_path() -> str:
    """Return the full URL of the post-login secure area."""
    return f"{get_base_url()}/secure"


def get_test_username() -> str:
    """Return the sandbox test username defined in .env (TEST_USERNAME)."""
    return os.getenv("TEST_USERNAME", "practice")


def get_test_password() -> str:
    """Return the sandbox test password defined in .env (TEST_PASSWORD)."""
    return os.getenv("TEST_PASSWORD", "SuperSecretPassword!")
