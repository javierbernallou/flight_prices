from flight_price_ml.src.db import get_connection
from flight_price_ml.src.flight_search import search_flights
from flight_price_ml.src.logger import logger
from sqlalchemy import text


ORIGINS = [
    "BCN",  # Barcelona
    "MAD",  # Madrid
    "ZAZ"   # Zaragoza
]

DESTINATIONS = [
    "LIS",  # Lisbon
    "BGY",  # Milan Bergamo
    "FCO",  # Rome
    "PRG",  # Prague
    "BUD",  # Budapest
    "CRL",  # Brussels Charleroi
    "VIE",  # Vienna
    "KRK"   # Krakow
]

DEPARTURE_DATES = [
    "2026-04-12",
    "2026-04-13",
    "2026-04-14",
    "2026-04-15"
]

RETURN_DATE = "2026-04-18"


def save_to_db(rows):

    conn = get_connection()

    query =text( """
    INSERT INTO flight_prices_raw (
        origin,
        destination,
        departure_date,
        return_date,
        airline,
        price
    )
    VALUES (
        :origin,
        :destination,
        :departure_date,
        :return_date,
        :airline,
        :price
    )
    """)

    for row in rows:
        conn.execute(query, row)

    conn.commit()
    conn.close()


def run():

    logger.info("Starting flight ingestion")

    rows = []

    for origin in ORIGINS:

        for destination in DESTINATIONS:

            for departure_date in DEPARTURE_DATES:

                logger.info(
                    f"Searching flights {origin} -> {destination} | {departure_date}"
                )

                flights = search_flights(
                    origin=origin,
                    destination=destination,
                    departure_date=departure_date,
                    return_date=RETURN_DATE
                )

                rows.extend(flights)

    if rows:

        logger.info(f"Saving {len(rows)} flights")

        save_to_db(rows)

    else:

        logger.warning("No flights found")


if __name__ == "__main__":
    run()
