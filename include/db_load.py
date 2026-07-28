import boto3
from include.config import bucket_name, db_user, db_password, db_host, db_port, db_name  # noqa: E501
from include.db_engine import engine
from datetime import date
import pandas as pd

s3 = boto3.client('s3')
postgresql_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"  # noqa: E501


def load_data_to_db():
    """
    Read today's raw CSV from S3 and load it into weather_table.
    """
    today_date = date.today().strftime('%Y-%m-%d')
    response = s3.get_object(
        Bucket=bucket_name,
        Key=f'raw/{today_date}.csv'
    )
    df = pd.read_csv(response['Body'])

    print(df)
    df.to_sql(
        name="weather_table",
        con=engine,
        index=False,
        if_exists="replace"
    )
