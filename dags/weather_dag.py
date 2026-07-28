"""
DAG: weather_pipeline

Daily ETL pipeline that pulls hourly weather data from Open-Meteo,
lands it in S3, loads it into Postgres, transforms it, computes a
daily clothing/umbrella recommendation, and renders a report.
"""

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from include.tasks import (
    extract_task,
    load_data_to_db_task,
    load_weather_codes_task,
    transform_task,
    recommend_task,
    notify_task,
)


default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="weather_pipeline",
    default_args=default_args,
    description="Daily weather ETL: extract -> load -> transform -> recommend -> notify",  # noqa: E501
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["weather"],
) as dag:

    extract = PythonOperator(
        task_id="extract_data",
        python_callable=extract_task,
    )

    load_raw = PythonOperator(
        task_id="load_data_to_db",
        python_callable=load_data_to_db_task,
    )

    load_codes = PythonOperator(
        task_id="load_weather_codes",
        python_callable=load_weather_codes_task,
    )

    transform = PythonOperator(
        task_id="transform_data",
        python_callable=transform_task,
    )

    generate_recommendation = PythonOperator(
        task_id="recommend",
        python_callable=recommend_task,
    )

    send_notification = PythonOperator(
        task_id="notify",
        python_callable=notify_task,
    )

    # extract must complete before the raw data can be loaded to Postgres
    extract >> load_raw

    # load_raw (weather_table) and load_codes (weather_code_table) both
    # need to exist before transform can join them
    [load_raw, load_codes] >> transform >> generate_recommendation >> send_notification   # noqa: E501
