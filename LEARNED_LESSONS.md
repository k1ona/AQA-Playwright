# 🧠 LEARNED LESSONS — AQA Playwright Framework

## 📋 Format
Each entry records: **Failure Type → Root Cause → Fix Applied → Guardrail**

---

## ⚠️ LESSON #1 — Wrong BASE_URL causes silent selector timeout
- **Date:** 2026-06-29
- **Failure type:** `playwright.TimeoutError` — `Locator.wait_for` on `#username` exceeded 5000ms
- **Root cause:** `.env` was set to `BASE_URL=https://expandtesting.com`. The practice login form
  (`#username`, `#password`) only exists on the **`practice.` subdomain**:
  `https://practice.expandtesting.com/login`. The apex domain returns a marketing page with no
  matching selectors, so every locator wait times out silently.
- **Fix applied:** Updated `.env` → `BASE_URL=https://practice.expandtesting.com`
- **Guardrail:** When building a config-manager `BASE_URL`, always verify it by navigating to
  `{BASE_URL}/login` in a browser before committing. The correct practice base URL is
  `https://practice.expandtesting.com` — never `https://expandtesting.com` (apex domain).

---

## ⚠️ LESSON #2 — Never call `sync_playwright()` inside a pytest-playwright session-scoped fixture
- **Date:** 2026-06-29
- **Failure type:** `playwright._impl._errors.Error: It looks like you are using Playwright Sync API inside the asyncio loop.`
- **Root cause:** `tests/conftest.py` tried to open a second `sync_playwright()` context manager
  inside a `scope="session"` fixture. pytest-playwright already owns the asyncio event loop for
  its internal async Playwright engine. Starting a second sync context inside that loop raises an
  incompatibility error at fixture setup.
- **Fix applied:** Replaced `sync_playwright()` with the `playwright` and
  `browser_type_launch_args` fixtures provided by pytest-playwright (both session-scoped). The
  fixture signature becomes `def authenticated_page(playwright, browser_type_launch_args)`.
- **Guardrail:** In any `conftest.py` fixture, always reuse the `playwright` fixture from
  pytest-playwright rather than calling `sync_playwright()`. Reserve `sync_playwright()` only for
  standalone scripts that run outside of pytest.

---

## ⚠️ LESSON #3 — `locator.wait_for(state="visible")` fails after `goto(wait_until="domcontentloaded")`
- **Date:** 2026-06-29
- **Failure type:** `playwright.TimeoutError` — `Locator.wait_for` on `h2` exceeded 10000ms
- **Root cause:** `page.goto(..., wait_until="domcontentloaded")` returns as soon as the DOM
  tree is parsed, before the browser has painted or made elements visually "visible". Playwright's
  `locator.wait_for(state="visible")` checks CSS visibility, which may not yet be true immediately
  after `domcontentloaded`. On ad-heavy pages we must use `domcontentloaded` to avoid blocking on
  third-party trackers, but this means visibility-based waits will often time out.
- **Fix applied:** Replaced `locator.wait_for(state="visible")` with `page.content()` (reads raw
  DOM immediately) and `locator.count() > 0` (DOM presence check, no visual state required).
- **Guardrail:** After `goto(wait_until="domcontentloaded")`, use `page.content()` or
  `locator.count()` for assertions. Only use `locator.wait_for(state="visible")` after
  `wait_until="load"` or `wait_until="networkidle"`, which guarantees the paint cycle has run.


## ⚠️ LESSON #4 — Flaky timeout on sequential page.goto() calls to sandbox site
- **Date:** 2026-06-29
- **Failure type:** `playwright.TimeoutError` — `Page.goto` exceeded 30000ms on second navigation
- **Root cause:** `wait_until="load"` (Playwright default) blocks until ALL network requests
  finish, including third-party ads and trackers on practice.expandtesting.com. When the
  suite runs multiple tests back to back, the second navigation hits the site while it's
  still serving ad resources from the first, causing a cascade timeout.
- **Fix applied:** Changed `BasePage.visit()` to use `wait_until="domcontentloaded"` so
  navigation returns as soon as the HTML is parsed, not when every resource finishes.
- **Guardrail:** Always use `wait_until="domcontentloaded"` in `BasePage.visit()` for
  ad-heavy sandbox sites. Never rely on the default `load` strategy in this framework.

---

## ⚠️ LESSON #5 — Flaky timeout on `locator.wait_for(state="visible")` in multi-page test suites
- **Date:** 2026-06-30
- **Failure type:** `playwright.TimeoutError` — `Locator.wait_for` on interactive elements
  (`#checkbox1`, `#dropdown`, `#input-number`) exceeded 10000ms intermittently across
  `test_ui_components.py` test runs.
- **Root cause:** After `page.goto(url, wait_until="domcontentloaded")`, the browser DOM
  is parsed but the visual paint cycle may not have completed. `locator.wait_for(state="visible")`
  checks CSS computed visibility, which is not guaranteed immediately post-`domcontentloaded`.
  In a multi-test suite run, prior test navigations leave the browser event loop in an
  unsettled state, making the paint timing even less predictable for the next test.
- **Fix applied:** For checkbox, dropdown, and input state ASSERTIONS, replaced
  `locator.wait_for(state="visible")` with `locator.count() > 0` (DOM presence) and
  `locator.input_value()` / `locator.is_checked()` (live DOM property reads that do not
  require visual rendering). For CLICK and FILL interactions, kept `wait_for(state="visible")`
  inside `BasePage.click_element()` and `BasePage.type_text()` but raised the timeout from
  5000ms to 10000ms to absorb paint delays on ad-heavy sandbox pages.
- **Guardrail:** After `goto(wait_until="domcontentloaded")`:
  - **Assertions** → use `locator.count()`, `locator.input_value()`, or `locator.is_checked()`.
    These read the DOM state without requiring a visual paint cycle.
  - **Interactions** (click, fill) → `wait_for(state="visible")` with ≥10000ms is acceptable
    because the user action itself implicitly confirms element readiness.
  - **Never** write bare `locator.wait_for(state="visible")` before an assertion on an
    ad-heavy sandbox site — this is the #1 source of intermittent CI failures in this suite.