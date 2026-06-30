# AQA-Playwright

![tests](https://github.com/k1ona/AQA-Playwright/actions/workflows/tests.yml/badge.svg)

## What this demonstrates

- Page Object Model with role-based and ID-based locators, no raw selectors
  inside test files
- An AI-assisted workflow with deterministic guardrails: pre-commit secret
  scanning (gitleaks), a Planner agent that verifies locators and server
  responses against the live site before any code is written, and a
  Builder-Auditor agent that audits and re-runs its own output before
  reporting a task done
- CI running the full suite on every push, with secrets injected via GitHub
  repository secrets rather than committed anywhere
- Database integrity testing against a real PostgreSQL instance (a small
  practice app, kept local rather than committed, since the public sandbox
  site used for UI/API tests has no accessible database), with test
  isolation via explicit cleanup so repeated runs do not leave stale rows
- API testing against a third-party service (practice.expandtesting.com),
  including status code and response shape assertions, negative cases, and
  a documented xfail for a known upstream bug rather than a softened
  assertion or a silently broken CI badge
- A documented project constitution (CLAUDE.md) and three scoped skill files
  (UI, API, database testing) that govern how tests get written in this repo

## Architecture
AQA-Playwright/

├── pages/                  # Page Object Models

├── tests/                  # Test files, organized by feature

├── utils/                  # config_manager, auth_helper

├── reference_vault/        # Saved HTML snapshots for offline inspection

├── .claude/

│   ├── skills/              # aqa-ui-testing, aqa-api-testing, aqa-db-testing

│   └── agents/               # planner, builder-auditor

├── .github/workflows/      # CI pipeline

├── CLAUDE.md                # Project constitution

├── COMMENT_VOICE.md         # Code comment style rule

├── PROJECT_STATE.md         # Current page objects, test coverage, known gotchas

├── .pre-commit-config.yaml  # gitleaks + ruff, runs before every commit

└── pytest.ini
## Running locally

```powershell
git clone https://github.com/k1ona/AQA-Playwright.git
cd AQA-Playwright
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
playwright install
pre-commit install
```

Copy `.env.example` to `.env` and fill in real values for `BASE_URL`,
`TEST_USERNAME`, and `TEST_PASSWORD`. Then:

```powershell
pytest
```

## What's intentionally out of scope right now

- Mobile and native app testing
- Accessibility scanning
- Broader database test coverage (constraint behavior, cascading deletes,
  soft-delete timestamps) — one test currently proves the pattern works,
  it is not yet a comprehensive suite
- Multi-agent orchestration beyond Planner and Builder-Auditor

These are deferred deliberately, not missing by oversight.
