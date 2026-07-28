import requests
import pandas as pd
from include.config import url, bucket_name
import boto3
from io import StringIO
from datetime import date

s3 = boto3.client("s3")
today_date = date.today().strftime("%Y-%m-%d")


def extract_data():
    """
    Fetch hourly weather data from the Open-Meteo API and land it
    as a raw CSV in S3, partitioned by today's date.
    """

    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data=data["hourly"])
    print(df)

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)

    s3.put_object(
        Bucket=bucket_name, Key=f"raw/{today_date}.csv",
        Body=csv_buffer.getvalue()
    )
