import argparse
import os
from typing import Dict, Optional

from dotenv import load_dotenv

from octopus_api_client import OctopusApiClient

load_dotenv()


def main(
    user_credentials: dict, start_date: str, end_date: str, data_folder: Optional[str]
) -> None:
    octopus_api_client = OctopusApiClient(
        start_date=start_date,
        end_date=end_date,
        user_credentials=user_credentials,
    )

    data = octopus_api_client._get_consumption_data(args.fuel_type)
    octopus_api_client.save_consumption_data(
        data, f"{data_folder}test_{args.fuel_type}.csv"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get consumption data.")
    parser.add_argument(
        "fuel_type", type=str, help='The fuel type, either "electricity" or "gas"'
    )
    parser.add_argument(
        "start_date", type=str, help="The start date in YYYY-MM-DD format"
    )
    parser.add_argument("end_date", type=str, help="The end date in YYYY-MM-DD format")
    args = parser.parse_args()
    start_date = args.start_date
    end_date = args.end_date

    data_folder: Optional[str] = os.getenv("DATA_FOLDER")

    user_credentials: Dict = {
        "mpan": os.getenv("MPAN"),
        "mprn": os.getenv("MPRN"),
        "electricity_serial_no": os.getenv("ELECTRICITY_SERIAL_NO"),
        "gas_serial_no": os.getenv("GAS_SERIAL_NO"),
        "api_key": os.getenv("API_KEY"),
        "customer_id": os.getenv("CUSTOMER_ID"),
    }

    main(user_credentials, start_date, end_date, data_folder)
