import re

import pytest


@pytest.mark.smoke
def test_time_returns_200_with_iso8601_timestamp(api_session, api_base_url):
    response = api_session.get(f"{api_base_url}/time")
    body = response.json()

    assert response.status_code == 200
    assert re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z$", body["time"]) is not None


@pytest.mark.smoke
def test_random_color_returns_200_with_hex_string(api_session, api_base_url):
    response = api_session.get(f"{api_base_url}/random-color")
    body = response.json()

    assert response.status_code == 200
    assert re.match(r"^#[0-9a-fA-F]{6}$", body["color"]) is not None


@pytest.mark.smoke
def test_random_number_defaults_returns_number_in_1_to_100(api_session, api_base_url):
    response = api_session.get(f"{api_base_url}/random-number")
    body = response.json()

    assert response.status_code == 200
    assert 1 <= body["number"] <= 100


@pytest.mark.smoke
def test_random_number_custom_range_returns_number_within_range(api_session, api_base_url):
    response = api_session.get(f"{api_base_url}/random-number", params={"min": 10, "max": 20})
    body = response.json()

    assert response.status_code == 200
    assert 10 <= body["number"] <= 20


@pytest.mark.smoke
def test_echo_valid_name_returns_greeting_message(api_session, api_base_url):
    # Asserting on "message", not "echoed" — the spec is wrong, the live API returns "message".
    response = api_session.post(f"{api_base_url}/echo", json={"name": "Alice"})
    body = response.json()

    assert response.status_code == 200
    assert body["message"] == "Hi Alice"
