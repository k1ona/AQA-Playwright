---
name: aqa-db-testing
description: >
  Use when writing or reviewing tests that assert PostgreSQL database state,
  verifying a UI or API action produced the correct row, constraint, or
  relationship. Trigger on "DB test", "check the database", "verify the row",
  "data integrity".
---

# Database Testing Standards (PostgreSQL)

## Before this skill applies at all

This skill only makes sense against a database you actually control. A
third-party sandbox site you do not have credentials for has no place for this
skill to attach to. If the current target has no accessible database, flag the
mismatch rather than inventing a connection string.

## Isolation

Every DB test runs inside a transaction rolled back at teardown, or against a
database reset between runs. Never leave rows behind for the next run to trip
over.

## What to check

- After an action, query the specific row it should have produced or changed.
  Assert on the specific columns the action claims to set, not a SELECT star
  eyeballed for plausibility.
- Constraint behavior: that a delete cascades or is blocked as designed, that
  a unique constraint actually rejects a duplicate.
- Timestamps and soft-delete flags, since these are exactly what a UI or API
  test can not see, and exactly what a real bug commonly breaks.

## Connection handling

Connection string comes from TEST_DATABASE_URL in .env, never hardcoded. Use a
context manager (with conn, with conn.cursor()) so a failed assertion does not
leak a connection.

## Naming

test_db_<table>_<action>_<expected_state>, e.g. test_db_bugs_close_sets_closed_at
