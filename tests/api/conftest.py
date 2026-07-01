import pytest
import requests

from utils.config_manager import get_base_url

# practice.expandtesting.com API is currently returning empty response bodies
# across all endpoints, confirmed via health check. Skipping the entire suite
# rather than xfailing since running against a known-down service wastes CI
# time — each request times out before getting an empty response.
# Remove this hook and confirm recovery via health check before re-enabling.
def pytest_collection_modifyitems(items):
    for item in items:
        if "tests/api" in str(item.fspath) or "tests\\api" in str(item.fspath):
            item.add_marker(
                pytest.mark.skip(
                    reason="practice.expandtesting.com API outage — all endpoints returning empty body, skip to avoid 30s timeouts per test"
                )
            )


@pytest.fixture(scope="session")
def api_base_url():
    return f"{get_base_url()}/api"


@pytest.fixture(scope="session")
def api_session():
    session = requests.Session()
    session.headers.update({"Accept": "application/json"})
    yield session
    session.close()
