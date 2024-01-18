from app.octopus_api_client import OctopusApiClient
import sys
import pytest

sys.path.insert(0, '.././app/octopus_api_client.py')


def test_octopus_api_client_instantiates():
    test_credentials = {
        "mpan": 123,
        "mprn": 123,
        "electricity_serial_no": "123safasf",
        "gas_serial_no": "test123",
        "api_key": "test123",
        "customer_id": "test123"
    }
    test_client = OctopusApiClient('2020-01-01',
                                   '2020-01-02',
                                   test_credentials)
    assert isinstance(test_client, OctopusApiClient)
