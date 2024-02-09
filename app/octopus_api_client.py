import logging
from datetime import datetime, timedelta
from typing import Dict, List

import pandas as pd
from requests import Response, get
from requests.auth import HTTPBasicAuth

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
    ],
)

log = logging.getLogger(__name__)

date_format: str = "%Y-%m-%d"


class OctopusApiClient:
    """
    A client for interacting with the Octopus Energy API.
    This client supports fetching consumption data for a specified date range.

    Attributes:
        start_date (str): The start date for fetching consumption data in the format 'YYYY-MM-DD'.
        end_date (str): The end date for fetching consumption data in the format 'YYYY-MM-DD'.
        user_credentials (dict): A dictionary containing user credentials needed for the API.
            It should include 'mpan', 'mprn', 'electricity_serial_no', 'gas_serial_no', and 'api_key'.
    """

    base_url = "https://api.octopus.energy"

    def __init__(self, start_date: str, end_date: str, user_credentials: Dict) -> None:
        self.start_date = datetime.strptime(start_date, date_format)
        self.end_date = datetime.strptime(end_date, date_format)
        self.mpan = user_credentials["mpan"]
        self.mprn = user_credentials["mprn"]
        self.electricity_serial_no = user_credentials["electricity_serial_no"]
        self.gas_serial_no = user_credentials["gas_serial_no"]
        self.api_key = user_credentials["api_key"]
        self.basic = HTTPBasicAuth(self.api_key, "")
        self.customer_id = user_credentials["customer_id"]

    def get_url(self, fuel_type: str) -> str:
        """
        Constructs and returns the URL for the API call based on the fuel type.
        Args:
            fuel_type (str): The type of fuel to get data for. This should be either "electricity" or "gas".
        Returns:
            str: The URL for the API call.
        Raises:
            ValueError: If the fuel_type is not "electricity" or "gas".
        """
        if fuel_type not in ["electricity", "gas"]:
            raise ValueError(
                f"Invalid fuel type {fuel_type}. Fuel type must be either 'electricity' or 'gas'."
            )
        if fuel_type == "electricity":
            url = f"{self.base_url}/v1/electricity-meter-points/{self.mpan}/meters/{self.electricity_serial_no}/consumption/"
        elif fuel_type == "gas":
            url = f"{self.base_url}/v1/gas-meter-points/{self.mprn}/meters/{self.gas_serial_no}/consumption/"
        return url

    def _call_api(self, url: str, params: Dict) -> List:
        """
        Private method to call the Octopus Energy API.
        This method sends a GET request to the specified URL and returns the response data.

        Args:
            url (str): The URL to send the GET request to.
        Returns:
            dict: The response data from the API call.
        Raises:
            requests.exceptions.RequestException: If the API call fails.
        """

        response: Response = get(url, params, auth=self.basic)
        if response.status_code == 200:
            return response.json()["results"]
        else:
            log.error(f"Error: Received status code {response.status_code}")
            return []

    def _get_consumption_data(self, fuel_type: str) -> List:
        """
        Private method to get consumption data from the Octopus Energy API for a specified fuel type and date range.
        This method iterates over each date in the range from `self.start_date` to `self.end_date`,
        and for each date, it calls the API to get the consumption data for the specified fuel type.

        Args:
            fuel_type (str): The type of fuel to get data for. This should be either "electricity" or "gas".
        Returns:
            List: A list of consumption data for each date in the range.
        Raises:
            requests.exceptions.RequestException: If an API call fails.
        """
        consumption_data: List = []

        for date in pd.date_range(self.start_date, self.end_date):
            start_date: str = datetime.strftime(date, date_format)
            log.info(
                f"Getting data for {start_date} and {fuel_type} for customer {self.customer_id}."
            )
            params: Dict = {
                "period_from": start_date,
                "period_to": datetime.strftime((date + timedelta(days=1)), date_format),
            }
            response: List = self._call_api(self.get_url(fuel_type), params)
            refined_data: List = self._refine_consumption_data(fuel_type, response)
            consumption_data.append(refined_data)

        return [item for sub_list in consumption_data for item in sub_list]

    def _refine_consumption_data(self, fuel_type: str, results: List) -> List[Dict]:
        """
        Private method to refine the consumption data returned from the Octopus Energy API.
        This method processes the raw data from the API to extract and format the relevant information.

        Args:
            data (dict): The raw data from the API.
        Returns:
            dict: The refined consumption data.
        Raises:
            KeyError: If an expected key is not found in the data.
        """
        refined_data: List = []
        for result in results:
            result["request_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            result["fuel_type"] = fuel_type
            result["mpan"] = self.mpan if fuel_type == "electricity" else self.mprn
            result["customer_id"] = self.customer_id
            result["serial_number"] = (
                self.electricity_serial_no
                if fuel_type == "electricity"
                else self.gas_serial_no
            )
            refined_data.append(result)
        return refined_data

    def save_consumption_data(self, refined_data: List[Dict], file_name: str) -> None:
        """
        Saves the consumption data to a file.
        This method takes the consumption data and a filename, and writes the data to the file in a specified format.

        Args:
            data (dict): The consumption data to save.
            filename (str): The name of the file to save the data to.

        Returns:
            None

        Raises:
            IOError: If there is an error writing to the file.
        """

        with open(file_name, "w") as f:
            f.write("date,mpan,serial_number,customer_id,fuel_type,consumption,request_time\n")
            for row in refined_data:
                f.write(
                    f"{row['interval_start']},{row['mpan']},{row['serial_number']},{row['customer_id']},{row['fuel_type']},{row['consumption']},{row['request_time']}\n"
                )
