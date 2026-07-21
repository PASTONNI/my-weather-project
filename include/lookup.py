import pandas as pd
from extract import connect_to_database

#Weather codes created from the open meteo website
weather_codes = {
    'code': [0, 1, 2, 3, 45, 48, 51, 53, 55, 61, 63, 65, 71, 73, 75, 80, 81, 82, 95, 96, 99],
    'description': ['Clear sky', 'Mainly clear', 'Partly cloudy', 'Overcast', 'Foggy', 'Icy fog', 'Light drizzle', 'Moderate drizzle', 'Dense drizzle', 'Slight rain', 'Moderate rain', 'Heavy rain', 'Slight snow', 'Moderate snow', 'Heavy snow', 'Slight showers', 'Moderate showers', 'Heavy showers', 'Thunderstorm', 'Thunderstorm with hail', 'Thunderstorm with heavy hail' ]
}



def to_weather_code_table():
    '''
    Function to convert the weather code dictionary to a dataframe
    '''
    return pd.DataFrame(data=weather_codes)


df = to_weather_code_table()
engine =  connect_to_database()

# load the table into Postgres
df.to_sql(name="weather_code_table", con=engine, index=False, if_exists='replace') # figure out how to make this a function

