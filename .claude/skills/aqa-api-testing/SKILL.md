---
name: aqa-api-testing
description: >
  Use when writing or reviewing API tests, REST endpoints, status codes,
  schema or contract checks, auth flows. Trigger on "API test", "test the
  endpoint", "check the response", "auth flow", "JWT", "OTP".
---

# API Testing Standards

## Stack

requests for synchronous HTTP calls. Do not introduce httpx unless a specific
test needs async behavior, adding it "for consistency" is the kind of
speculative choice CLAUDE.md rule 2 exists to prevent.

## What every API test checks, at minimum

1. Status code, asserted explicitly, not inferred from a helper that treats
   any 2xx as a pass.
2. The specific response fields the test cares about, not the entire payload,
   unless a real schema or contract makes whole-payload validation practical.
3. One negative case per endpoint where it applies: malformed request,
   unauthorized request, or not-found case.

## Auth flow testing

Fetch a token once per test session, not once per test, unless the test is
specifically about login or token issuance. Token expiry and refresh is tested
as its own explicit test, not assumed to work because login worked. Never
store a real token in test code or fixture data, generate it from .env
credentials at runtime.

## Naming

test_<resource>_<action>_<expected_outcome>, e.g. test_user_create_duplicate_email_returns_409

## Out of scope for this skill

Verifying what the API actually wrote to the database. That is the
aqa-db-testing skill job, and it loads alongside this one when a test needs
both.
