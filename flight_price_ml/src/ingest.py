from datetime import date,datetime, timedelta
from sqlalchemy import text 
from flight_price_ml.src.db import get_connection
from flight_price_ml.src.flight_search import search_flights, safe_requests
import sys
from flight_price_ml.src.amadeus_client import get_access_token

from flight_price_ml.src.logger import logger

from datetime import date

def extract_price_data(data, origin, destination, departure_date):
    rows = []
    
    if "data" not in data:
        return rows

    for offer in data["data"]:
        try:
            price = float(offer["price"]["total"])
            airline_codes = offer.get("validatingAirlineCodes", [])
            
            if price <= 0: continue  
            if not airline_codes: continue 
            
            row = {
                "search_date": date.today(),
                "origin": origin,
                "destination": destination,
                "departure_date": departure_date,
                "return_date": None,
                "airline": airline_codes[0],
                "price": price,
                "currency": offer["price"]["currency"],
                "stops": len(offer["itineraries"][0]["segments"]) - 1,
                "duration_minutes": 0  
            }
            rows.append(row)
            
        except (KeyError, TypeError, IndexError) as e:
            print(f"Error procesando una oferta: {e}")
            continue

    return rows

def save_to_db(rows):
    conn = get_connection()

    query = text("""
        INSERT INTO flight_prices_raw (
            search_date, origin, destination,
            departure_date, return_date,
            airline, price, currency,
            stops, duration_minutes
        )
        VALUES (
            :search_date, :origin, :destination,
            :departure_date, :return_date,
            :airline, :price, :currency,
            :stops, :duration_minutes
        )
        ON CONFLICT DO NOTHING
    """)

    try:

        conn.execute(query, rows)
        conn.commit()
    except Exception as e:
        print(f"Error al guardar en DB: {e}")
        conn.rollback()
    finally:
        conn.close()

def run():
    if len(sys.argv) > 1:
        departure = sys.argv[1]
    else:
        departure = "2026-04-7"
    ROUTES = [
    # Madrid a los principales de Londres
    ("MAD", "LHR"),  # Heathrow
    ("MAD", "LGW"),  # Gatwick
    ("MAD", "STN"),  # Stansted
    
    # Barcelona a Londres
    ("BCN", "LHR"),
    ("BCN", "LGW"),
    ("BCN", "STN"),
    
    # Otras rutas importantes de España
    ("AGP", "LGW"),  # Málaga (muy común para Londres)
    ("ALC", "STN"),  # Alicante
    ("VLC", "LGW"),  # Valencia
    ("BIO", "LHR"),  # Bilbao
]

    departure = "2026-05-10"

    for origin, destination in ROUTES:
        data = search_flights(origin, destination, "2026-05-10")
        rows = extract_price_data(data, origin, destination, "2026-05-10")
        data = safe_requests(lambda: search_flights(origin, destination, "2026-05-10"))
        if rows:
            save_to_db(rows)
            print(f"Se han insertado {len(rows)} vuelos correctamente.")
        else:
            print("No se encontraron vuelos para la ruta: {}-{}".format(origin, destination))


    logger.info("Iniciando ingestión vuelos")
    logger.info(f"Registros obtenidos: {len(rows)}")
    logger.error("Error API", exc_info=True)
    



if __name__ == "__main__":
    run()
