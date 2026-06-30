import pytest


@pytest.mark.smoke
def test_cars_returns_200_with_list_of_six_items(api_session, api_base_url):
    response = api_session.get(f"{api_base_url}/cars")
    body = response.json()

    assert response.status_code == 200
    assert body["status"] == "success"
    assert len(body["cars"]) == 6


@pytest.mark.regression
def test_cars_each_item_contains_required_fields(api_session, api_base_url):
    response = api_session.get(f"{api_base_url}/cars")
    body = response.json()

    assert response.status_code == 200
    for car in body["cars"]:
        assert "id" in car
        assert "name" in car
        assert "price" in car
        assert "image" in car
        assert isinstance(car["id"], int)
