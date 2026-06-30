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
