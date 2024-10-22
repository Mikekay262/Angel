import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../scripts')))
from preprocess import load_and_clean_inventory

# Path to inventory file
inventory_path = "data/raw/inventory.csv"

# Load inventory data
inventory_df = load_and_clean_inventory(inventory_path)

# Title of the section
st.title('Order Fulfillment Tracker')

# Input for customer name (optional)
customer_name = st.text_input("Enter Customer Name")

# Store entered orders in a DataFrame
order_entries = []

# Create a form for entering order details
with st.form("order_entry_form", clear_on_submit=True):
    st.write("Enter Order Details:")

    # Select item from inventory
    item_selected = st.selectbox("Select Item", inventory_df['Item'])

    # Input requested and fulfilled quantities
    quantity_requested = st.number_input("Quantity Requested", min_value=0)
    quantity_fulfilled = st.number_input("Quantity Fulfilled", min_value=0)

    # Submit button to add item to order
    submitted = st.form_submit_button("Add Item to Order")

    if submitted:
        # Append the data to the order entries list
        order_entries.append({
            "Customer": customer_name,
            "Item": item_selected,
            "Quantity Requested": quantity_requested,
            "Quantity Fulfilled": quantity_fulfilled,
            "Price": inventory_df[inventory_df['Item'] == item_selected]['Price'].values[0]
        })

# Ensure that order_entries list is not empty
if order_entries:
    # Convert order entries into a DataFrame
    order_df = pd.DataFrame(order_entries)
    st.write("### Order Data Entered")
    st.write(order_df)

    # Function to calculate KPIs
    def calculate_kpis(order_df):
        # Expected Revenue = Sum of (Quantity Requested * Price)
        order_df['Expected Revenue'] = order_df['Quantity Requested'] * order_df['Price']
        
        # Actual Revenue = Sum of (Quantity Fulfilled * Price)
        order_df['Actual Revenue'] = order_df['Quantity Fulfilled'] * order_df['Price']
        
        # Percent Revenue Actualized = (Actual Revenue / Expected Revenue) * 100
        order_df['Percent Revenue Actualized'] = (order_df['Actual Revenue'] / order_df['Expected Revenue']) * 100

        # Total Items
        total_items = len(order_df)

        # Percentage of Fully Fulfilled Items
        fully_fulfilled_items = len(order_df[order_df['Quantity Fulfilled'] == order_df['Quantity Requested']])
        percent_fully_fulfilled = (fully_fulfilled_items / total_items) * 100

        # Percentage of Partially Fulfilled Items
        partially_fulfilled_items = len(order_df[(order_df['Quantity Fulfilled'] > 0) & 
                                                 (order_df['Quantity Fulfilled'] < order_df['Quantity Requested'])])
        percent_partially_fulfilled = (partially_fulfilled_items / total_items) * 100
        
        return order_df, percent_fully_fulfilled, percent_partially_fulfilled

    # Calculate KPIs
    order_df, percent_fully_fulfilled, percent_partially_fulfilled = calculate_kpis(order_df)

    # Display KPIs
    st.write("### Order KPIs")
    
    # Display as tiles
    st.metric(label="Total Expected Revenue", value=f"GHS {order_df['Expected Revenue'].sum():,.2f}")
    st.metric(label="Total Actual Revenue", value=f"GHS {order_df['Actual Revenue'].sum():,.2f}")
    st.metric(label="% Revenue Actualized", value=f"{order_df['Percent Revenue Actualized'].mean():.2f}%")
    
    # Pie chart for fully vs. partially fulfilled
    fulfillment_data = pd.DataFrame({
        "Fulfillment Type": ["Fully Fulfilled", "Partially Fulfilled"],
        "Percentage": [percent_fully_fulfilled, percent_partially_fulfilled]
    })
    
    st.write("### Fulfillment Distribution")
    st.write(fulfillment_data)
    st.bar_chart(fulfillment_data.set_index("Fulfillment Type"))

    # Allow user to download the order data as CSV
    st.write("### Export Report")
    st.download_button(label="Download CSV", data=order_df.to_csv(index=False), 
                       file_name=f"order_fulfillment_report_{customer_name}.csv", mime="text/csv")

else:
    st.write("No order entries yet.")
