# Project State

## Page objects registry

| File | Target URL | Key locators |
|---|---|---|
| `pages/login_page.py` | `/login` | `#username`, `#password`, `button[type='submit']`, `#flash` |
| `pages/checkboxes_page.py` | `/checkboxes` | `#checkbox1` (unchecked default), `#checkbox2` (checked default) |
| `pages/dropdown_page.py` | `/dropdown` | `#dropdown` (simple), `#elementsPerPageSelect` (per-page), `#country` (ISO codes) |
| `pages/inputs_page.py` | `/inputs` | `#input-number`, `#input-text`, `#input-password`, `#input-date`, `#btn-display-inputs`, `#btn-clear-inputs` |
| `pages/register_page.py` | `/register` | `#username`, `#password`, `#confirmPassword`, `button[type='submit']`, `#flash` |

## Test files registry

| File | Markers used | Coverage |
|---|---|---|
| `tests/test_authentication.py` | `smoke`, `regression`, `auth` | Login, invalid login, session state bypass |
| `tests/test_ui_components.py` | `smoke`, `regression` | Checkbox toggling, all three dropdowns, all four input fields plus clear action |
| `tests/test_register.py` | `smoke`, `regression` | Registration form validation, duplicate username, password rules, success redirect |
| `tests/test_db_bugs.py` | none | Bug creation via local practice app, verified directly against Postgres; skipped in CI (requires local infrastructure) |
| `tests/api/test_health_check.py` | `smoke` | API health check endpoint |
| `tests/api/test_math.py` | `smoke`, `regression` | /add endpoint, integers, negatives, floats with approx, missing params |
| `tests/api/test_phone.py` | `smoke`, `regression` | Phone code lookup by country |
| `tests/api/test_geo.py` | `smoke`, `regression` | City and location lookup by coordinates; two cases marked xfail for a known upstream /get-city degradation |
| `tests/api/test_utility.py` | `smoke` | Time, random color, random number, echo endpoints |
| `tests/api/test_cars.py` | `smoke`, `regression` | Cars listing endpoint, item shape validation |
| `tests/api/test_currency.py` | `smoke`, `regression` | Currency conversion, valid pairs, unsupported pairs, missing params |
| `tests/test_network_interception.py` | `smoke` | Network interception via page.route() — mocks notes API empty response and asserts UI empty state renders correctly |

## Test suite summary (as of last CI run)

- Total collected: 53 (local, includes DB test)
- CI result: 49 passed, 1 skipped, 2 xfailed
- Skipped: `test_db_bugs.py` — requires local practice app and Postgres, not available in CI
- Xfailed: 2 tests in `test_geo.py` — known upstream `/get-city` endpoint degradation

## Reference vault

- `reference_vault/expandtesting/` — saved HTML snapshots of practice.expandtesting.com pages, for offline selector inspection without hitting the live site.
- `reference_vault/expandtesting/notes_app.html` — logged-in snapshot of the notes app (separate auth system from main sandbox), captured via `scripts/capture_notes_snapshot.py`.


## Useful commands

- Full suite, headed: `pytest --headed`
- Specific marker: `pytest -m smoke --headed`
- UI component tests only: `pytest tests/test_ui_components.py --headed`

## Known gotchas

- BASE_URL must be `https://practice.expandtesting.com`, not
  `https://expandtesting.com`. The apex domain returns a marketing page with
  none of the practice site's selectors, so any locator wait against it times
  out with no useful error pointing at the real cause. This has caused a real
  failure twice: once locally, once in CI before secrets were wired in
  correctly. config_manager.py's get_base_url() fallback now defaults to the
  correct subdomain, but a misconfigured .env or missing CI secret will still
  reproduce this exact failure.
- PowerShell 5.1 `Out-File -Encoding utf8` silently adds a UTF-8 BOM to
  files, which breaks pytest.ini parsing and can cause Python import errors.
  Create sensitive files (pytest.ini, .py files) via VS Code directly rather
  than PowerShell here-strings, or use `[System.IO.File]::WriteAllText()`
  which writes clean UTF-8 without BOM.

## Deferred additions

- Cross-browser testing: add `--browser firefox` and `--browser webkit` to
  pytest.ini addopts when ready to triple the test run across browsers.
  Both are supported by pytest-playwright with no other changes needed.
  CI workflow already installs all browser dependencies via
  `playwright install --with-deps`.
  ## Integrated tooling

- **Playwright MCP** (`@playwright/mcp@latest`) — connected in Claude Code
  sessions, 23 tools. Gives the Planner agent live browser access via the
  accessibility tree. Registered via `claude mcp add` scoped to this project
  directory. The Planner uses `browser_snapshot` for locator verification
  instead of reference vault snapshots.