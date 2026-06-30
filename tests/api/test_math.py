import pytest


@pytest.mark.smoke
def test_add_two_positive_integers_returns_correct_sum(api_session, api_base_url):
    response = api_session.get(f"{api_base_url}/add", params={"a": 3, "b": 4})
    body = response.json()

    assert response.status_code == 200
    assert body["result"] == 7


@pytest.mark.smoke
def test_add_negative_numbers_returns_correct_sum(api_session, api_base_url):
    response = api_session.get(f"{api_base_url}/add", params={"a": -5, "b": 3})
    body = response.json()

    assert response.status_code == 200
    assert body["result"] == -2


@pytest.mark.smoke
def test_add_float_inputs_returns_approximate_sum(api_session, api_base_url):
    # Using approx here because 1.1 + 2.2 produces 3.3000000000000003 in IEEE 754 — a bare equality check would always fail.
    response = api_session.get(f"{api_base_url}/add", params={"a": 1.1, "b": 2.2})
    body = response.json()

    assert response.status_code == 200
    assert body["result"] == pytest.approx(3.3)


@pytest.mark.regression
def test_add_missing_params_returns_400_with_error_message(api_session, api_base_url):
    response = api_session.get(f"{api_base_url}/add")
    body = response.json()

    assert response.status_code == 400
    assert body["error"] == "Both a and b must be numbers"
