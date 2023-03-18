# app/utils.py

import json
import pandas as pd


def convert_response_to_df(response):
    data_dict = json.loads(response.json())
    df = pd.DataFrame(data_dict["rows"], columns=data_dict["columns"])
    df.rename(columns={'LAST_ACTIVITY_BLOCK_TIMESTAMP': 'date'}, inplace=True)
    df.rename(columns={'SYMBOL': 'token'}, inplace=True)
    df.rename(columns={'CURRENT_BAL': 'balance'}, inplace=True)
    return df
