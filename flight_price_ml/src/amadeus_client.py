import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AMADEUS_API_KEY")
API_SECRET = os.getenv("AMADEUS_API_SECRET")

def get_access_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"

    data = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": API_SECRET
    }

    response = requests.post(url, data=data)
    response.raise_for_status()

    return response.json()["access_token"]