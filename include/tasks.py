from include.extract import extract_data
from include.db_load import load_data_to_db
from include.transform import load_weather_codes, transform_data
from include.recommend import recommend
from include.notify import daily_report


def extract_task():
    """
    Run the extraction task.
    """
    extract_data()


def load_data_to_db_task():
    """
    Run the load_data to db task
    """
    load_data_to_db()


def load_weather_codes_task():
    """
    Run the load weather codes task
    """
    load_weather_codes()


def transform_task():
    """
    Run the transform data task
    """
    transform_data()


def recommend_task():
    """
    Run the recommend data task
    """
    recommend()


def notify_task():
    """
    Run the notify task
    """
    daily_report()
