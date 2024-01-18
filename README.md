# Octopus Energy API Client

This repository contains a Python client for interacting with the Octopus Energy API.

## Features

- Fetch consumption data for a specified date range.
- Save consumption data to a file.
- Supports both electricity and gas data.

## Setup

### 1. Clone the repo
To get started, you need to clone the repository to your local machine. 
In the directory where you want to install the app, run the following command:

```bash
git clone https://github.com/antonsuess/octopus.git
```
Once the repository has been cloned, navigate into the directory:

```bash
cd octopus
```

### 2. Install Pyenv

Pyenv is a simple, powerful and cross-platform tool for managing multiple Python versions. To install it, you can follow the instructions on the [official Pyenv GitHub](https://github.com/pyenv/pyenv#installation).

### 3. Install Python 3.11.3 with Pyenv

Once Pyenv is installed, you can install Python 3.11.3 using the following command:

```bash
pyenv install 3.11.3
```

### 4. Create a Virtual Environment
Next, create a virtual environment named octopus using Python 3.11.3:

```bash
pyenv virtualenv 3.11.3 octopus
```
### 5. Activate the Virtual Environment
Before installing the project dependencies, make sure to activate the octopus environment:

```bash
pyenv activate octopus
```

### 6. Install dependencies
Install the required dependencies:
```bash
pip install -r requirements.txt
```

### 7. Get your Octopus Enery credentials
To complete

### 8. Create `octopus/.env` with environment variables
```bash
cd octopus
touch .env
```
Put the following environment variables in this file

```bash
MPAN=
MPRN=
ELECTRICITY_SERIAL_NO=
GAS_SERIAL_NO=
API_KEY=
CUSTOMER_ID="FirstName LastName" # eg.
```


## Usage
Then, you can use the `OctopusApiClient` class in your Python code:

```python
from octopus_api_client import OctopusApiClient

user_credentials = {
    "mpan": 123,
    "mprn": 123,
    "electricity_serial_no": "123ABC",
    "gas_serial_no": "123ABC",
    "api_key": ,
}

octopus_api_client = OctopusApiClient(
    start_date="2020-01-01",
    end_date="2020-01-02",
    user_credentials=user_credentials,
)

electricity_data = octopus_api_client._get_consumption_data("electricity")
```
## Testing

Tests are written using pytest. To run the tests, use the following command:
```bash
pytest
```

## Contributing
Contributions are welcome! Please submit a pull request or create an issue to get started.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
