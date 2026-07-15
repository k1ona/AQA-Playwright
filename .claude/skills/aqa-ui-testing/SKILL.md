---
name: aqa-ui-testing
description: >
  Use when writing or reviewing Playwright UI/E2E tests for this project,
  page objects, locators, fixtures, waits. Trigger on "UI test", "page object",
  "locator", "E2E", "browser test".
---

# UI Testing Standards (Playwright + pytest)

## Page object rules

One file per page or feature, under pages/. A page object holds locators and
thin actions only (fill_login_form, click_submit), no assertions inside a page
object, assertions live in the test file. BasePage carries shared waits and
navigation helpers every page object inherits from.

## Locator priority, highest to lowest

1. get_by_role / get_by_label / get_by_test_id
2. get_by_text, only when the text is stable copy unlikely to change for
   cosmetic reasons
3. CSS selector, only when nothing above is available, and only after a
   Planner pass confirms no test-id can reasonably be added

Raw CSS selectors inside a test file rather than a page object should fail the
Builder/Auditor own audit pass.

## Waits

Use Playwright built-in auto-waiting and expect() polling. No sleep(), no
manual retry loop. If an unusual wait is genuinely needed, say why in a
comment per the project comment voice rule, rather than silently adding a
fixed delay.

## Fixtures

Session-level browser/context fixture, function-level page fixture, matching
the structure already in conftest.py. Auth state reused via storage_state,
not re-logging-in per test, unless the test is specifically about login.

## Naming

test_<page>_<action>_<expected_outcome>, e.g. test_register_missing_email_shows_error


## Navigation and wait strategy (learned the hard way)

This project's BasePage.visit() uses wait_until="domcontentloaded", not the
Playwright default of "load". The sandbox site serves ad and tracker
resources that "load" waits on, which causes cascading timeouts across a
multi-test run. Do not change this back to "load" without a real reason and
a re-test of the full suite, not just the one test in front of you.

The tradeoff that comes with domcontentloaded: the DOM is parsed, but the
paint cycle may not be finished. That means visibility-based waits behave
differently depending on what you're doing:

- For assertions checking element state (is a checkbox checked, what's in a
  dropdown, what's in an input), use locator.count() > 0, locator.is_checked(),
  or locator.input_value(). These read live DOM properties without requiring
  a visual paint, and won't flake on timing the way a visibility check will.
- For interactions (click, fill), wait_for(state="visible") is fine, and
  BasePage.click_element() / type_text() already use it with a 10000ms
  timeout, not the original 5000ms, which proved too tight on ad-heavy pages.
- Never write a bare locator.wait_for(state="visible") immediately before an
  assertion on this sandbox site specifically. That pattern was the single
  largest source of intermittent CI failures before the fix above, across
  four separate incidents (checkboxes, dropdowns, inputs, and a generic h2
  heading check).

Also never call sync_playwright() directly inside a session-scoped pytest
fixture. pytest-playwright already owns the event loop; starting a second
sync context inside it raises an incompatibility error at fixture setup.
Reuse the playwright and browser_type_launch_args fixtures pytest-playwright
already provides. Reserve sync_playwright() for standalone scripts that run
outside of pytest, like the one-off snapshot scripts in this project's history.
