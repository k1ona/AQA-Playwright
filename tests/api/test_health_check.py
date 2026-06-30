import pytest


@pytest.mark.smoke
def test_health_check_returns_200_and_status_up(api_session, api_base_url):
    response = api_session.get(f"{api_base_url}/health-check")
    body = response.json()

    assert response.status_code == 200
    assert body["success"] is True
    assert body["status"] == "UP"
