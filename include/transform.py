import pandas as pd
from sqlalchemy import text
from include.db_engine import engine
from include.config import weather_codes


def load_weather_codes():
    """
    Load the static weather-code lookup table into Postgres.
    """
    df = pd.DataFrame(data=weather_codes)

    # load the table into Postgres
    df.to_sql(
        name="weather_code_table",
        con=engine,
        index=False,
        if_exists='replace'
        )


def transform_data():
    """
    Join raw weather data with weather codes, engineer clothing/
    umbrella columns, and load the result into weather_table_silver.
    """
    sql = text("""
        SELECT w.*,
        wc.description as weather_condtion
        FROM weather_table w
        LEFT JOIN weather_code_table wc ON w.weather_code = wc.code;
        """)
    df = pd.read_sql(sql, con=engine)

    # Transform the data
    df[['date', 'time']] = df.time.str.split("T", expand=True)

    # rearrange the order of the columns
    df = df[
        [
            "date",
            "time",
            "temperature_2m",
            "apparent_temperature",
            "wind_speed_10m",
            "precipitation",
            "weather_code"
            ]
        ]

    def get_clothing_recommendation(temp):
        if temp <= 10:
            return 'Heavy Coat'
        elif temp <= 15:
            return 'Light Coat'
        elif temp <= 20:
            return 'Casual wear'
        else:
            return 'Light clothing'

    df['clothing_recommendation'] = df['apparent_temperature'].apply(
        get_clothing_recommendation
        )

    def carry_umbrella(precipitaion):
        if precipitaion > 0:
            return True
        else:
            return False

    df['carry_umbrella'] = df['precipitation'].apply(carry_umbrella)

    print(df.head())

    # Load to PG admin
    df.to_sql(
        name="weather_table_silver",
        con=engine,
        index=False,
        if_exists='replace'
        )
