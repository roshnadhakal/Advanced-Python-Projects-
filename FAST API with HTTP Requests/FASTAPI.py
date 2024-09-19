# Import FastAPI and HTTPException from fastapi module
from fastapi import FastAPI, HTTPException
import requests

#  First Initializing the FastAPI app
app = FastAPI()

# API key provided by api website for accessing the ExchangeRate API
api_key = "d52d92f7d818c26a1c4b6fc3"

# Base endpoint url for the ExchangeRate API
api_endpoint = "https://v6.exchangerate-api.com"

# Defining a route to get exchange rates for a given base currency
@app.get("/")  
async def read_root():
    # Returns a simple message at the root endpoint
    return {"message": "Welcome to the Exchange Rate API!"}

@app.get("/exchange-rates")
async def get_exchange_rates(base_currency: str = "USD"):
    # Construct the API URL with the base currency
    url = f"{api_endpoint}/v6/{api_key}/latest/{base_currency}"

    try:
        # Make a request to the ExchangeRate API
        response = requests.get(url)

        # Check if the response is successful (HTTP 200)
        if response.status_code == 200:
            # Parse the response JSON data
            data = response.json()
            # Return the conversion rates if available
            return {"exchange_rates": data.get("conversion_rates", {})}
        else:
            # Raise an HTTP exception if the status code is not 200
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except requests.exceptions.RequestException as e:
        # Handle any request exceptions (network issues, etc.)
        raise HTTPException(status_code=500, detail=str(e))

# To run the app, use the command: uvicorn FASTAPI:app --reload
