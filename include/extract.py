import requests
import pandas as pd
from config import url, bucket_name
import boto3
from io import StringIO
from datetime import date

s3 = boto3.client('s3')
today_date = date.today().strftime('%Y-%m-%d')


def extract_data():
    def fetch_data():
        response = requests.get(url)
        data = response.json()
        return pd.DataFrame(data=data['hourly'])

    df = fetch_data()

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)

    s3.put_object(
        Bucket=bucket_name,
        Key=f'raw/{today_date}.csv',
        Body=csv_buffer.getvalue()
    )


extract_data()
