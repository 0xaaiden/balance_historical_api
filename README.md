# Token Balances API

This is a Flask-based API that retrieves the latest token balances for a given Ethereum address on a specific date. The data is queried from Flipside and returned in JSON format.

## Getting Started

To use this API, clone the repository and install the dependencies:

```
git clone https://github.com/0xaaiden/balance_historical_api
cd balance_historical_api
pip3 install -r requirements.txt
```

You will also need to obtain an API key from Flipside.com to query their database.

Once you have the API key, create a .env file in the root directory of the project and add the following line:

```
FLIPSIDE_API=yourapikeyhere
```

By default, the API will be available at http://localhost:5000/.

## Endpoints

### `/token_balances`

Retrieves the latest token balances for a given Ethereum address on a specific date.

#### Parameters

- `address (required)`: The Ethereum address for which to retrieve the token balances.
- `date (required)`: The date on which to retrieve the token balances, in the format `YYYY-MM-DD`.

#### Example Request

```
GET http://localhost:5000/token_balances?address=0x1234567890123456789012345678901234567890&date=2022-03-17
```

#### Example Response

```
{
    "address": "0x1234567890123456789012345678901234567890",
    "date": "2022-03-17",
    "num_tokens": 3,
    "latest_balances": {
        "ETH": "1.23456789",
        "USDT": "1234.56789",
        "LINK": "12.3456789"
    }
}
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.
