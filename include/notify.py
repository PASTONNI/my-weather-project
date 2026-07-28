import pandas as pd
from jinja2 import Environment, FileSystemLoader
from include.db_engine import engine
from include.config import notification_recipient
from airflow.utils.email import send_email

env = Environment(loader=FileSystemLoader('include/templates/'))
template = env.get_template('weather_report.html')


def daily_report():
    sql = "SELECT * FROM weather_table_summary"
    df = pd.read_sql(sql, con=engine)

    # seperate the values
    row = df.iloc[0]

    # pass the html values
    html = template.render(
        date=row['date'],
        lowest_temperature=row['lowest_temperature'],
        highest_temperature=row['highest_temperature'],
        clothing_recommendation=row['clothing_recommendation'],
        carry_umbrella=row['carry_umbrella']
    )

    send_email(
        to=notification_recipient,
        subject=f"Weather Report for {row['date']}",
        html_content=html,
    )
