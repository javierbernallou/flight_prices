from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "javier",
    "retries": 2,
    "retry_delay": timedelta(minutes=5)
}

with DAG(
    dag_id="flight_price_ingestion",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule="@0 */6 * * *",  # Cada 6 horasvam
    catchup=False
) as dag:

    run_ingestion = BashOperator(
        task_id="run_ingest_script",
        bash_command="python /opt/airflow/flight_project/src/ingest.py {{ ds }}"
    )