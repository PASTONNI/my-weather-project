import pandas as pd
from sqlalchemy import text
from include.db_engine import engine


def recommend():
    """
    Aggregate the silver table into a daily summary (highs, lows,
    clothing recommendation, umbrella flag) and load it into
    weather_table_summary.
    """
    sql = text("""
            SELECT
            date,
            highest_temperature,
            lowest_temperature,
            carry_umbrella,
            CASE
            WHEN lowest_temperature < 10 THEN 'Heavy coat'
            WHEN lowest_temperature < 15 THEN 'Light jacket'
            WHEN lowest_temperature < 20 THEN 'Casual wear'
            ELSE 'Light clothing'
            END AS clothing_recommendation
            from (
                SELECT
                date,
                MAX(apparent_temperature) AS highest_temperature,
                MIN(apparent_temperature) AS lowest_temperature,
                CASE WHEN
                MAX(precipitation) > 0
                THEN True ELSE False END AS carry_umbrella
                FROM weather_table_silver
                WHERE time between '07:00' and '18:00'
                GROUP BY date
            ) as daily_summary
            """)
    # def read_sql_file():

    # sql = read_sql_file()
    df = pd.read_sql(sql, con=engine)

    # write the summary table to the POSTGRES
    df.to_sql(
        name="weather_table_summary",
        index=False,
        con=engine,
        if_exists='replace'
    )
