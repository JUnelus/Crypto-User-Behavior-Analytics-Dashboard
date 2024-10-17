import json   # Import json for JSON file
import pandas as pd
import requests
from db_connection import engine  # Import the engine from db_connection.py
import os
from dotenv import load_dotenv
import time  # Import time for adding delays

# Load environment variables from .env file
load_dotenv()

# Set up your Etherscan API key
ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')

# Function to load addresses from a JSON file
def load_addresses_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    # Return a list of dictionaries containing address and description
    return [{'address': address['address'], 'description': address['description']} for address in data['addresses']]

# Function to fetch on-chain data from Etherscan
def fetch_onchain_data(address):
    url = f'https://api.etherscan.io/api'
    params = {
        'module': 'account',
        'action': 'balance',
        'address': address,
        'tag': 'latest',
        'apikey': ETHERSCAN_API_KEY
    }

    print(f"Fetching data for address: {address}")
    print(f"Request URL: {url}, Params: {params}")

    response = requests.get(url, params=params)
    data = response.json()

    if data['status'] == '1':  # Status '1' means success
        balance = int(data['result']) / 10 ** 18  # Convert Wei to Ether
        return balance
    else:
        print(f"API Response: {data}")  # Print the entire response for debugging
        raise Exception(f"Error fetching data: {data['message']}")

# Save data to PostgreSQL database
def save_to_db(df):
    # Drop duplicates based on address and balance
    df = df.drop_duplicates()

    # Print the DataFrame to debug
    print("DataFrame to save:", df)

    # Save DataFrame to PostgreSQL
    df.to_sql('onchain_data', engine, if_exists='append', index=False)

if __name__ == '__main__':
    try:
        # Load addresses from the JSON file
        eth_addresses = load_addresses_from_json('../data/eth_addresses.json')

        # Initialize an empty DataFrame to collect all data
        all_data = pd.DataFrame(columns=['address', 'description', 'balance'])

        for item in eth_addresses:
            address = item['address']
            description = item['description']
            balance = fetch_onchain_data(address)

            # Create a temporary DataFrame for the current entry
            temp_df = pd.DataFrame({'address': [address], 'description': [description], 'balance': [balance]})

            # Only concatenate if temp_df has non-NA entries
            if not temp_df.isna().all().any():
                all_data = pd.concat([all_data, temp_df], ignore_index=True)

            print(f"Data extracted and saved for address: {address}, Description: {description}")
            time.sleep(1)  # Adding a delay of 1 second between requests

        # Save all data to the database at once
        save_to_db(all_data)

    except Exception as e:
        print(f"An error occurred: {e}")
