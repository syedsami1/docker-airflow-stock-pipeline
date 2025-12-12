from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "stock_data_pipeline",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    fetch_and_store = BashOperator(
        task_id="fetch_and_store_stock_data",
        bash_command="python /opt/airflow/scripts/fetch_and_store.py"
    )
