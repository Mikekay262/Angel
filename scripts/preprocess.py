import pandas as pd

# Function to load and clean the inventory data
def load_and_clean_inventory(inventory_path):
    # Load the inventory CSV
    inventory_df = pd.read_csv(inventory_path)
    
    # Clean the 'Price' column by removing 'GHS' and commas, and converting it to float
    inventory_df['Price'] = inventory_df['Price'].replace({'GHS': '', ',': ''}, regex=True).astype(float)

    # Fill missing quantities and prices with 0
    inventory_df['Price'] = inventory_df['Price'].fillna(0)
    
    return inventory_df
