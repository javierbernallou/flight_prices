import requests
from datetime import date
from amadeus_client import get_access_token
import time

def search_flights(origin, destination, departure_date):
    token = get_access_token()

    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": departure_date,
        "adults": 1,
        "max": 5
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    return response.json()

def safe_requests(func, retries=3):
    for attempt in range(retries):
        try:
            return func()
        except requests.RequestException as e:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)