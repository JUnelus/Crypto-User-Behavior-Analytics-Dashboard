import pandas as pd
from db_connection import engine  # Import the engine from db_connection.py

# Function to transform data
def transform_data():
    # Read data from PostgreSQL
    df = pd.read_sql('SELECT * FROM onchain_data', engine)

    # Ensure data types are correct
    df['balance'] = df['balance'].astype(float)  # Ensure balance is float
    df['address'] = df['address'].astype(str)   # Ensure address is string
    df['description'] = df['description'].astype(str)  # Ensure description is string

    # Example: Calculate total balance for all addresses (if needed)
    total_balance = df['balance'].sum()
    print(f"Total ETH balance of all addresses: {total_balance:.4f}")

    # Example: Display unique descriptions
    unique_descriptions = df['description'].unique()
    print(f"Unique descriptions: {unique_descriptions}")

    return df

if __name__ == '__main__':
    transformed_data = transform_data()
    print(transformed_data.head())  # Print the first few rows of the transformed data
