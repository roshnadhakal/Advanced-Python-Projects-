# Exchange Rate API

This project is a FastAPI application that provides exchange rates for various currencies. It retrieves data from the ExchangeRate API and allows users to query exchange rates based on a specified base currency.

## Requirements

1. **python 3.12.4 or higher**

  To run this application, you need to install FastAPI and Uvicorn. Follow these steps:
  
2. **Install FastAPI and Uvicorn**:
   ```bash
   pip install fastapi uvicorn requests
   ```

3. **Get your API key**:
   - Sign up at [ExchangeRate API](https://v6.exchangerate-api.com) to receive your API key. Replace the placeholder in the code with your actual API key.

## How to Run the Code

To start the FastAPI application, run the following command in your terminal:

```bash
uvicorn FASTAPI:app --reload
```

Replace `FASTAPI` with the name of your Python file if it's different.

## Code Explanation

The code initializes a FastAPI application and defines two endpoints:

- **Root Endpoint (`/`)**: Returns a welcome message.
  
- **Exchange Rates Endpoint (`/exchange-rates`)**: Accepts a query parameter for the base currency (default is USD) and fetches exchange rates from the ExchangeRate API.

The application handles potential errors by raising HTTP exceptions if the API request fails or returns an error status.


## Usage

After starting the server, you can access:

- The root endpoint at `http://127.0.0.1:8000/` to see the welcome message.
- The exchange rates endpoint at `http://127.0.0.1:8000/exchange-rates?base_currency=EUR` (replace `EUR` with any other currency code) to get the exchange rates relative to the specified base currency.

## Features

- Fetches real-time exchange rates.
- Supports multiple currencies.
- Simple RESTful interface with clear error handling.

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request for any improvements or features you would like to add.
