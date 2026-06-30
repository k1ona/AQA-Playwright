import pytest


@pytest.mark.smoke
def test_currency_convert_usd_to_eur_returns_correct_rate_and_amount(api_session, api_base_url):
    response = api_session.get(
        f"{api_base_url}/currency-convert",
        params={"from": "USD", "to": "EUR", "amount": 100},
    )
    body = response.json()

    assert response.status_code == 200
    assert body["rate"] == pytest.approx(0.85)
    assert body["converted"] == 85


@pytest.mark.smoke
def test_currency_convert_zero_amount_returns_zero_converted(api_session, api_base_url):
    response = api_session.get(
        f"{api_base_url}/currency-convert",
        params={"from": "USD", "to": "EUR", "amount": 0},
    )
    body = response.json()

    assert response.status_code == 200
    assert body["converted"] == 0


@pytest.mark.regression
def test_currency_convert_unsupported_pair_returns_400(api_session, api_base_url):
    response = api_session.get(
        f"{api_base_url}/currency-convert",
        params={"from": "INVALID", "to": "EUR", "amount": 100},
    )
    body = response.json()

    assert response.status_code == 400
    assert body["error"] == "Unsupported currency conversion"


@pytest.mark.regression
def test_currency_convert_missing_amount_param_returns_400(api_session, api_base_url):
    response = api_session.get(
        f"{api_base_url}/currency-convert",
        params={"from": "USD", "to": "EUR"},
    )
    body = response.json()

    assert response.status_code == 400
    assert body["error"] == "Missing or invalid parameters"
