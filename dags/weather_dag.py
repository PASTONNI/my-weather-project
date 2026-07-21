from airflow.sdk import Asset, dag, task
from pendulum import datetime


@dag(
    start_date=datetime(2025, 4, 22),
    schedule="@daily",
    doc_md=__doc__,
    default_args={"owner": "Airflow", "retries": 3},
    tags=["weather_pipeline"],
)
