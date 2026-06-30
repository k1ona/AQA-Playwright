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