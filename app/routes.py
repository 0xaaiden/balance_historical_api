from shroomdk import ShroomDK
from flask import Blueprint, jsonify, request
import pandas as pd
import json
import os
from dotenv import load_dotenv


main = Blueprint('main', __name__)
load_dotenv()

API_KEY = os.getenv('API_KEY')
sdk = ShroomDK(API_KEY)


@main.route('/token_balances', methods=['GET'])
def get_latest_balances():
    address = request.args.get('address')
    date = request.args.get('date')

    # validate address
    if not address:
        return jsonify({'error': 'Address is required.'}), 400
    if not address.startswith('0x') or len(address) != 42:
        return jsonify({'error': 'Invalid address format.'}), 400

    # validate date
    if not date:
        return jsonify({'error': 'Date is required.'}), 400
    try:
        pd.to_datetime(date)
        # if the date is in the future, return an error
        if pd.to_datetime(date) > pd.to_datetime('today'):
            return jsonify({'error': 'Date cannot be in the future.'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid date format.'}), 400

    # query the database
    query = f'''
            SELECT
        *
        FROM
        ethereum.core.ez_current_balances
        WHERE
        user_address = '{address}'
        AND
        LAST_ACTIVITY_BLOCK_TIMESTAMP <= TO_TIMESTAMP('{date} 00:00:00')
        LIMIT 50
        '''
    try:
        response = sdk.query(query)
        # print(response)
        data_dict = json.loads(response.json())
    except Exception as e:
        return jsonify({'error': f'Error querying data: {str(e)}'}), 500

    # create a DataFrame from the dictionary
    df = pd.DataFrame(data_dict["rows"], columns=data_dict["columns"])

    # rename LAST_ACTIVITY_BLOCK_TIMESTAMP to date
    df.rename(columns={'LAST_ACTIVITY_BLOCK_TIMESTAMP': 'date'}, inplace=True)
    df.rename(columns={'SYMBOL': 'token'}, inplace=True)
    df.rename(columns={'CURRENT_BAL': 'balance'}, inplace=True)

    df = df.sort_values(by='date', ascending=False)

    # create a dictionary to store the latest balance for each token
    latest_balances = {}

    # iterate over each row in the dataframe
    for index, row in df.iterrows():
        # check if we've already recorded the latest balance for this token
        if row['token'] not in latest_balances:
            # if we haven't, check if the current balance is defined or is not None or not NaN
            if row['balance'] is not None and not pd.isna(row['balance']):
                # if it is, record the current balance as the latest balance for this token
                latest_balances[row['token']] = row['balance']
            # if not, record the current balance as the latest balance for this token
        # if we've already recorded the latest balance for this token, move on to the next row
        else:
            continue

    # save the balances to the database

    # return the latest balances in JSON format
    response_data = {
        'address': address,
        'date': date,
        'num_tokens': len(latest_balances),
        'latest_balances': latest_balances
    }
    return jsonify(response_data)
