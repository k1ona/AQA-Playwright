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
| `tests/test_ui_components.py` (added 2026-06-30) | `smoke`, `regression` | Checkbox toggling, all three dropdowns, all four input fields plus clear action |
| `tests/test_register.py` (added 2026-06-30) | `smoke`, `regression` | Registration happy path, all server-side validation errors, duplicate username |

## Reference vault

- `reference_vault/expandtesting/` — saved HTML snapshots of practice.expandtesting.com pages, for offline selector inspection without hitting the live site.

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