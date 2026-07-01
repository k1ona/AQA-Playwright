import pytest


@pytest.mark.smoke
def test_get_city_valid_coordinates_returns_city_name(api_session, api_base_url):
    response = api_session.get(f"{api_base_url}/get-city", params={"lat": 48.8566, "lon": 2.3522})
    body = response.json()
    assert response.status_code == 200
    assert body["status"] == "success"
    assert body["city"] == "Paris"


@pytest.mark.regression
def test_get_city_missing_params_returns_400(api_session, api_base_url):
    response = api_session.get(f"{api_base_url}/get-city")
    body = response.json()
    assert response.status_code == 400
    assert body["message"] == "Missing coordinates"


@pytest.mark.regression
def test_get_city_ocean_coordinates_returns_404(api_session, api_base_url):
    response = api_session.get(f"{api_base_url}/get-city", params={"lat": 0, "lon": 0})
    body = response.json()
    assert response.status_code == 404
    assert body["status"] == "error"


@pytest.mark.smoke
def test_location_details_valid_coordinates_returns_country_record(api_session, api_base_url):
    response = api_session.get(
        f"{api_base_url}/location-details",
        params={"latitude": 48.8566, "longitude": 2.3522},
    )
    body = response.json()
    assert response.status_code == 200
    assert body["location_details"]["short_name"] == "FR"
    assert body["location_details"]["long_name"] == "France"


@pytest.mark.regression
def test_location_details_ocean_coordinates_returns_404(api_session, api_base_url):
    # This endpoint returns 404 for unresolvable coordinates rather than a
    # structured not-found body, so I am checking for the key presence only.
    response = api_session.get(
        f"{api_base_url}/location-details",
        params={"latitude": 0, "longitude": 0},
    )
    body = response.json()
    assert response.status_code == 404
    assert "error" in body
