# CLAUDE.md — Project Constitution for AQA-Playwright

This file is read at the start of every Claude Code session in this repository.
It is not optional context, it is the standing rule set. Skill files under
.claude/skills/ carry domain knowledge (how to write a given kind of test);
this file carries behavior (how to work at all).

## 1. Think before coding

Before writing any test or fixture, state in plain language: which acceptance
criterion this covers, and which selector or endpoint it relies on, and where
that selector or endpoint was actually verified (a Planner pass, a live page
inspection, or documented API behavior). If a selector or endpoint has not been
verified, say so and stop. Do not guess a CSS path or invent a field name. Ask
rather than silently resolve an ambiguous requirement.

## 2. Simplicity first

Write the smallest test or fixture that proves the requirement. No speculative
configuration, no parameterizing a value that has only ever had one value, no
abstraction "for later." If a fixture or page object passes roughly 100 lines,
treat that as a signal to stop and simplify before continuing.

## 3. Surgical changes

Touch only the files this task requires. Do not refactor, rename, or restyle
adjacent code while completing an unrelated task. If you notice dead code or an
inconsistency outside the current scope, name it in your summary, do not fix it
unasked.

## 4. Goal-driven execution

Before starting multi-step work, state success criteria in checkable terms, for
example "3 new tests, all green locally and in CI, zero raw selectors in the
audit pass." Loop against that criteria. Do not report something done because it
looks plausible, run it and report what actually happened.

## 5. AQA-specific rules

- Never declare a test "passing" without executing it and reading the actual
  output.
- No hardcoded credentials, tokens, or connection strings anywhere in test code.
  Source them from environment variables via .env, which is gitignored.
  .env.example documents variable names only, never real values.
- No raw CSS selectors inside test files. Locators belong in page objects,
  role-based or test-id based wherever possible (see aqa-ui-testing skill).
- Database tests run inside a rolled-back transaction or against a disposable
  test database. Never against a database you cannot afford to corrupt.
- A test file with no assertion in it is not a test, it's dead code, flag it.

## 6. Comment voice

Code comments in this project follow the voice rule documented in
COMMENT_VOICE.md at the repo root. No exceptions, including for quick scripts
or scratch files.

## 7. Project state

Current page objects, test file coverage, reference vault contents, and useful
commands are tracked in PROJECT_STATE.md, not in this file. Check there before
assuming a page object or test doesn't already exist.