# run_pipeline.py
import sys
from datetime import datetime
from .src.ingest import run

if __name__ == "__main__":

    print(f"Empezando desde GitHub Actions: {datetime.now()}")
    run()