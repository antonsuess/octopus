import argparse
from app.octopus_api_client import OctopusApiClient
from dotenv import load_dotenv
import os

load_dotenv()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process start and end dates.")
    parser.add_argument('fuel_type', type=str, help='The fuel type, either "electricity" or "gas"')
    parser.add_argument('start_date', type=str, help='The start date in YYYY-MM-DD format')
    parser.add_argument('end_date', type=str, help='The end date in YYYY-MM-DD format')
    args = parser.parse_args()

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
        start_date=args.start_date,
        end_date=args.end_date,
        user_credentials=user_credentials,
    )

    data = octopus_api_client._get_consumption_data(args.fuel_type)
    octopus_api_client.save_consumption_data(data, f'{data_folder}test_{args.fuel_type}.csv')