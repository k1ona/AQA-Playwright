import pytest
import requests

from utils.config_manager import get_base_url


@pytest.fixture(scope="session")
def api_base_url():
    return f"{get_base_url()}/api"


@pytest.fixture(scope="session")
def api_session():
    session = requests.Session()
    session.headers.update({"Accept": "application/json"})
    yield session
    session.close()
