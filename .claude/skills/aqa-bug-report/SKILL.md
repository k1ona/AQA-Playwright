---
name: aqa-bug-report
description: >
  Use when writing a bug report from a failed test, a manual exploratory
  finding, or a defect discovered during requirements analysis. Trigger on
  "bug report", "write up this defect", "log this issue", "file a bug",
  "баг-репорт", "оформить баг".
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

These are always two separate fields, never one column doing double duty.
A column labeled Priority that actually holds severity language (Critical,
Minor) is a common and easy mistake, watch for it specifically when
adapting an existing template, including templates already in use
elsewhere, not just ones built from scratch here.

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
- Low / cosmetic: no functional impact

## Priority scale

- High: fix before the next release, blocks something time-sensitive
- Medium: fix in the current cycle, no immediate external pressure
- Low: fix when capacity allows, not currently blocking anything

## Required fields, every report, no exceptions

- Title specific enough that someone could triage from the title alone, not
  "login broken" but "login fails with 500 when password contains a
  trailing space"
- Environment: browser/OS/app version, whatever is relevant to reproduce
- Preconditions: state the system needs to be in before reproducing
  (an account must exist, a specific record must already be present)
- Steps to reproduce, numbered, complete enough that someone else can follow
  them without guessing at an implied step
- Expected result
- Actual result
- Severity, justified in one sentence
- Priority, justified in one sentence, separately from severity
- Visual evidence where available: a screenshot, a video, or the relevant
  log/console/response output

A report missing reproduction steps is not ready to file. Reproduce it
again and capture the real steps before logging it, rather than filing
something a developer will just bounce back asking what was actually done.

## Intermittent bugs

Do not drop a bug for being hard to reproduce. Log it, but be transparent
about the reproduction rate ("reproduced 3 of 10 attempts") and note the
exact conditions present when it did reproduce.

## Tying back to automated tests in this project

When a test in this suite fails and the failure represents a real defect,
not a flaky test or an environment issue, the bug report should reference
the specific test (file and function name) and include the actual pytest
failure output as the evidence, rather than re-describing the failure in
prose. The test output already is the reproduction steps.

## Format (English)

Title:
Environment:
Preconditions:
Steps to reproduce:
Expected result:
Actual result:
Severity (with justification):
Priority (with justification):
Evidence:

## Format (Russian)

Use this when the target application, the team, or the existing bug
tracker is Russian-language. Field names below match common Russian QA
tracker conventions, not a literal translation of the English template.

Название БР:
Окружение:
Предусловия:
Шаги воспроизведения:
Ожидаемый результат:
Фактический результат:
Серьёзность (с обоснованием):
Приоритет (с обоснованием):
Доказательства:

Серьёзность scale: Критический / Существенный / Незначительный / Косметический
Приоритет scale: Высокий / Средний / Низкий

Keep Серьёзность and Приоритет as two distinct fields even when adapting
an existing tracker template that historically combined them into one
Приоритет column holding severity-flavored values (Критический,
Незначительный, and similar). That historical pattern is the exact
conflation this skill exists to avoid, do not reproduce it just because a
prior template did.
