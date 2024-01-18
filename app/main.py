from app.octopus_api_client import OctopusApiClient
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    data_folder = os.getenv('DATA_FOLDER')
    user_credentials = {
        "mpan": os.getenv('MPAN'),
        "mprn": os.getenv('MPRN'),
        "electricity_serial_no": os.getenv('ELECTRICITY_SERIAL_NO'),
        "gas_serial_no": os.getenv('GAS_SERIAL_NO'),
        "api_key": os.getenv('API_KEY'),
        'customer_id': os.getenv('CUSTOMER_ID')
    }

    octopus_api_client = OctopusApiClient(
        start_date="2024-01-01",
        end_date="2024-01-11",
        user_credentials=user_credentials,
    )

    for fuel_type in ["electricity", "gas"]:
        data = octopus_api_client._get_consumption_data(fuel_type)
        octopus_api_client.save_consumption_data(data, f'{data_folder}test_{fuel_type}.csv')