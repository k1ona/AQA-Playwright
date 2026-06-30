import pytest


@pytest.mark.smoke
def test_phone_code_valid_country_returns_dialing_code(api_session, api_base_url):
    response = api_session.get(f"{api_base_url}/phone-code/FR")
    body = response.json()

    assert response.status_code == 200
    assert body["countryCode"] == "FR"
    assert body["phoneCode"] == "+33"


@pytest.mark.regression
def test_phone_code_unknown_country_returns_404(api_session, api_base_url):
    response = api_session.get(f"{api_base_url}/phone-code/INVALID_CODE")
    body = response.json()

    assert response.status_code == 404
    assert body["message"] == "Country code not found"
