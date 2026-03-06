import requests
import time
from flight_price_ml.src.logger import logger
from flight_price_ml.src.amadeus_client import get_access_token


BASE_URL = "https://test.api.amadeus.com/v2/shopping/flight-offers"


def safe_request(url, headers=None, params=None, retries=3):

    for attempt in range(retries):
        try:
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=30
            )

            if response.status_code == 200:
                return response.json()

            logger.warning(f"API error {response.status_code}: {response.text}")

        except Exception as e:
            logger.warning(f"Request failed: {e}")

        time.sleep(2)

    logger.error("Max retries reached")
    return None


def search_flights(origin, destination, departure_date, return_date):

    token = get_access_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": departure_date,
        "returnDate": return_date,
        "adults": 1,
        "currencyCode": "EUR",
        "max": 10
    }

    data = safe_request(BASE_URL, headers=headers, params=params)

    if not data or "data" not in data:
        return []

    flights = []

    for offer in data["data"]:

        try:

            price = float(offer["price"]["total"])

            airline = offer["validatingAirlineCodes"][0]

            flights.append({
                "origin": origin,
                "destination": destination,
                "departure_date": departure_date,
                "return_date": return_date,
                "airline": airline,
                "price": price
            })

        except Exception as e:
            logger.warning(f"Error parsing flight: {e}")

    return flights
