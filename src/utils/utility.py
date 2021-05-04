import pandas as pd

def alphavantage_api_csv_download_raw(function, symbol, alphavantage_api_key):
    datatype= 'csv'
    url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&datatype={datatype}&apikey={alphavantage_api_key}"

    return pd.read_csv(url)

def process_alphavantage_data_create_dow_dummies(raw_data_file):
    df= raw_data_file.copy()
    df['timestamp']= pd.to_datetime(df['timestamp'])
    df['day_of_week'] = df['timestamp'].dt.day_name()

    # create dummy variables

    dummies= pd.get_dummies(df['day_of_week'])

    # drop original days of the week column from the original dataframe
    df.drop('day_of_week', axis=1, inplace=True)

    # add two dataframes together
    df= pd.concat([df, dummies], axis= 1)

    # we are only interested in running a regression of volume against the dummy variables 
    # for days of the week. Because of this we will drop the remaining variables before 
    # importing it to our processed data folder
    df.drop(columns=['timestamp', 'open', 'high', 'low', 'close', 
                            'adjusted_close','dividend_amount', 'split_coefficient'], 
                inplace=True)

    return df


