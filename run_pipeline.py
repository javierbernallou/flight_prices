import os
import sys

# 👇 Añadir raíz del proyecto al path
sys.path.append(os.path.abspath("."))

from flight_prices_ml.src.ingest import run

if __name__ == "__main__":
    print("Iniciando pipeline de vuelos...")
    run()
    print("Pipeline finalizado correctamente.")
