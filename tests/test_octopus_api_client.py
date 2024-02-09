from datetime import datetime
import pytest
from typing import List, Dict
from app.octopus_api_client import OctopusApiClient


@pytest.fixture
def test_client() -> OctopusApiClient:
    test_credentials = {
        "mpan": 123,
        "mprn": 456,
        "electricity_serial_no": "electricity123",
        "gas_serial_no": "gas123",
        "api_key": "test123",
        "customer_id": "test123",
    }
    return OctopusApiClient("2020-01-01", "2020-01-02", test_credentials)


def test_octopus_api_client_instantiates(test_client: OctopusApiClient):
    assert isinstance(test_client, OctopusApiClient)


def test_octopus_api_client_get_url(test_client: OctopusApiClient):
    assert (
        test_client.get_url("electricity")
        == "https://api.octopus.energy/v1/electricity-meter-points/123/meters/electricity123/consumption/"
    )
    assert (
        test_client.get_url("gas")
        == "https://api.octopus.energy/v1/gas-meter-points/456/meters/gas123/consumption/"
    )


@pytest.mark.parametrize("fuel_type", ["electricity", "gas"])
def test_refine_consumption_data(test_client: OctopusApiClient, fuel_type: str):
    results: List = [{"key1": 1}]
    refined_data = test_client._refine_consumption_data(fuel_type, results)
    assert refined_data[0]["fuel_type"] == fuel_type
    assert isinstance(
        datetime.strptime(refined_data[0]["request_time"], "%Y-%m-%d %H:%M:%S"),
        datetime,
    )
    if fuel_type == "electricity":
        assert refined_data[0]["mpan"] == 123
        assert refined_data[0]["serial_number"] == "electricity123"
    if fuel_type == "gas":
        assert refined_data[0]["mpan"] == 456
        assert refined_data[0]["serial_number"] == "gas123"
