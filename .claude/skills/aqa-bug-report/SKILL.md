---
name: aqa-bug-report
description: >
  Use when writing a bug report from a failed test, a manual exploratory
  finding, or a defect discovered during requirements analysis. Trigger on
  "bug report", "write up this defect", "log this issue", "file a bug".
---

# Bug Report Standards

## Severity and priority are independent, never conflate them

Severity is a technical assessment: how badly the defect affects the system
(crashes, data corruption, a core workflow blocked, a security exposure).
Set it based on what the bug actually does, not on how it feels to find it.

Priority is a business judgment: how soon it needs fixing, based on who sees
it, how often, and what else is happening (a launch, a campaign, an
executive demo). Priority often needs input beyond what a tester alone can
assess, flag this rather than guessing at business context that is not
yours to know.

These can diverge in either direction. A crash that only triggers past 1000
characters in a field nobody fills past 10 is high severity, low priority.
A misaligned button on a pricing page during a paid campaign launch is low
severity, high priority. Report both axes honestly even when they pull in
different directions, do not round one up to match the other for emphasis.

## Severity scale

- Critical: system unusable, data loss or corruption, a security exposure
- Major: a core workflow broken for a meaningful set of users, no reasonable
  workaround exists
- Minor: a workflow is impaired but a workaround exists, or impact is
  limited to a small subset of users
- Low: cosmetic, no functional impact

## Required fields, every report, no exceptions

- Title specific enough that someone could triage from the title alone, not
  "login broken" but "login fails with 500 when password contains a
  trailing space"
- Environment: browser/OS/app version, whatever is relevant to reproduce
- Steps to reproduce, numbered, complete enough that someone else can follow
  them without guessing at an implied step
- Expected result
- Actual result
- Severity and priority, each justified in one sentence, not just a label
- Visual evidence where available: a screenshot, a video, or the relevant
  log/console output

A report missing reproduction steps is not ready to file. Reproduce it
again and capture the real steps before logging it, rather than filing
something a developer will just bounce back asking what was actually done.

## Intermittent bugs

Do not drop a bug for being hard to reproduce. Log it, but be transparent
about the reproduction rate ("reproduced 3 of 10 attempts") and note the
exact conditions present when it did reproduce, the device, what was
happening immediately before, anything that might be the actual trigger
even if it is not yet confirmed.

## Tying back to automated tests in this project

When a test in this suite fails and the failure represents a real defect,
not a flaky test or an environment issue, the bug report should reference
the specific test (file and function name) and include the actual pytest
failure output as the evidence, rather than re-describing the failure in
prose. The test output already is the reproduction steps.

## Format

Use the field order above as a literal template:

Title:
Environment:
Steps to reproduce:
Expected result:
Actual result:
Severity (with justification):
Priority (with justification):
Evidence:
