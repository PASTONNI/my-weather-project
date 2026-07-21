import boto3
from config import bucket_name
from datetime import date
import pandas as pd

s3 = boto3.client('s3')
today_date = date.today().strftime('%Y-%m-%d')


def get_object():
    response = s3.get_object(
        Bucket=bucket_name,
        Key=f'raw/{today_date}.csv'
    )
    df = pd.read_csv(response['Body'])
    return df


df = get_object()
print(df)
