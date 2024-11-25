# Import libraries
import streamlit as st
import pandas as pd
from app.utils.preprocess import load_and_clean_inventory
from app.assets.styles.UI import UI


    # Styled header
st.title("🎯 Order Fulfillment Tracker")

def calculate_kpis(order_df):
    """Calculate KPIs and add columns to the DataFrame."""
    if 'QuantityOrdered' in order_df and 'QuantityFulfilled' in order_df and 'Price' in order_df:
        order_df['Expected Revenue'] = order_df['QuantityOrdered'] * order_df['Price']
        order_df['Actual Revenue'] = order_df['QuantityFulfilled'] * order_df['Price']
        order_df['Revenue Lost'] = order_df['Expected Revenue'] - order_df['Actual Revenue']
        order_df['Percent Revenue Actualized'] = (order_df['Actual Revenue'] / order_df['Expected Revenue']) * 100
        order_df['Percent Revenue Actualized'].fillna(0, inplace=True)  # Handle NaN
    else:
        st.warning("Required columns for KPI calculation are missing!")
    return order_df

def calculate_order_metrics(order_df):
    """Calculate and return aggregated metrics for the entire order."""
    item_count = order_df.shape[0]
    fully_fulfilled_items = len(order_df[order_df['QuantityFulfilled'] == order_df['QuantityOrdered']])
    partially_fulfilled_items = len(
        order_df[(order_df['QuantityFulfilled'] > 0) & (order_df['QuantityFulfilled'] < order_df['QuantityOrdered'])]
    )
    not_fulfilled_items = len(order_df[order_df['QuantityFulfilled'] == 0])
    quantity_fulfill_rate = (order_df['QuantityFulfilled'].sum() / order_df['QuantityOrdered'].sum()) * 100

    order_value = order_df['OrderValue'].sum()
    revenue_actualized = order_df['ValueActualized'].sum()
    revenue_lost = order_value - revenue_actualized
    percent_revenue_actualized = (revenue_actualized / order_value) * 100 if order_value > 0 else 0

    return {
        "ItemCount": item_count,
        "percentage_fully_fulfilled": (fully_fulfilled_items / item_count) * 100,
        "percentage_partially_fulfilled": (partially_fulfilled_items / item_count) * 100,
        "percentage_not_fulfilled": (not_fulfilled_items / item_count) * 100,
        "quantity_fulfill_rate": quantity_fulfill_rate,
        "OrderValue": order_value,
        "RevenueActualized": revenue_actualized,
        "RevenueLost": revenue_lost,
        "percent_revenue_actualized": percent_revenue_actualized,
    }

def ensure_columns_exist(df, columns):
    """Ensure necessary columns exist in the DataFrame."""
    for column in columns:
        if column not in df.columns:
            df[column] = 0  # Initialize missing columns
    return df

def add_data():
    """Main function to add new records to the database."""
    # Load data from CSV files
    df = pd.read_csv("app/assets/data/data.csv")
    df_customers = pd.read_csv("app/assets/data/data_customers.csv")
    df_inventory = pd.read_csv("app/assets/data/inventory/inventory.csv")

    # Clean Inventory
    inventory_df = load_and_clean_inventory("app/assets/data/inventory/inventory.csv")

    st.subheader('Add New Record to Database')

    # Initialize session state for storing multiple items for a single order
    if "order_entries" not in st.session_state:
        st.session_state["order_entries"] = []

    # Initialize session state for persistent fields
    if "order_metadata" not in st.session_state:
        st.session_state["order_metadata"] = {
            "order_date": None,
            "customer_name": None,
            "invoice_number": None
        }

    # Validate invoice number for duplicates
    existing_invoice_numbers = set(df['InvoiceNumber'])  # Extract existing invoice numbers from the dataset

    # Auto-validate metadata input (only ask once per order)
    col1, col2, col3 = st.columns(3)
    if not st.session_state["order_metadata"]["order_date"]:
        order_date = col1.date_input(label="Order Date")
        customer_name = col2.selectbox("Customer", df_customers["Customer"])
        invoice_number = col3.text_input(label="Invoice Number")

        if order_date and customer_name and invoice_number.strip():
            if invoice_number.strip() in existing_invoice_numbers:
                st.error("Invoice Number already exists! Please use a unique Invoice Number.")
            else:
                st.session_state["order_metadata"].update({
                    "order_date": order_date,
                    "customer_name": customer_name,
                    "invoice_number": invoice_number.strip()
                })
        else:
            st.error("Please complete all order details!")
    else:
        st.info(f"Order Date: **{st.session_state['order_metadata']['order_date']}**")
        st.info(f"Customer: **{st.session_state['order_metadata']['customer_name']}**")
        st.info(f"Invoice Number: **{st.session_state['order_metadata']['invoice_number']}**")

    # Form to add multiple items to the order
    with st.form("item_form", clear_on_submit=True):
        item_options = ['Select Item'] + list(inventory_df['Item'])
        item_selected = st.selectbox("Select Item", item_options)
        quantity_ordered = st.number_input("Quantity Ordered", min_value=0)
        quantity_fulfilled = st.number_input("Quantity Fulfilled", min_value=0)
        add_item = st.form_submit_button("Add Item to Order")

        if add_item:
            if not st.session_state["order_metadata"]["order_date"]:
                st.error("Order details are not yet entered. Please complete the order details!")
            elif item_selected == 'Select Item':
                st.error("Please select a valid item.")
            elif quantity_fulfilled > quantity_ordered:
                st.error("Fulfilled quantity cannot exceed the ordered quantity.")
            else:
                # Get the price for the selected item
                price = inventory_df[inventory_df['Item'] == item_selected]['Price'].values[0]
                order_value = quantity_ordered * price  # Calculate OrderValue
                value_actualized = quantity_fulfilled * price  # Calculate ValueActualized
                revenue_lost = order_value - value_actualized

                # Append the order entry to session state
                st.session_state["order_entries"].append({
                    "InvoiceNumber": st.session_state["order_metadata"]["invoice_number"],
                    "OrderDate": st.session_state["order_metadata"]["order_date"],
                    "Customer": st.session_state["order_metadata"]["customer_name"],
                    "Item": item_selected,
                    "QuantityOrdered": quantity_ordered,
                    "QuantityFulfilled": quantity_fulfilled,
                    "Price": price,
                    "OrderValue": order_value,
                    "ValueActualized": value_actualized,
                    "RevenueLost": revenue_lost,
                })

    # Display the current order details in session state
    if st.session_state["order_entries"]:
        order_df = pd.DataFrame(st.session_state["order_entries"])
        st.write("### Current Order Details")
        st.write(order_df)

    # Save Data button
    if st.button("Save Data"):
        if not st.session_state["order_metadata"]["order_date"]:
            st.error("Order details are missing! Please complete them before saving.")
        elif not st.session_state["order_entries"]:
            st.warning("No order entries to save!")
        else:
            order_df = pd.DataFrame(st.session_state["order_entries"])

            # Calculate KPIs and ensure necessary columns exist in df
            order_df = calculate_kpis(order_df)
            df = ensure_columns_exist(df, order_df.columns)

            # Concatenate new data
            df = pd.concat([df, order_df], ignore_index=True)

            # Calculate aggregated metrics for the order
            order_metrics = calculate_order_metrics(order_df)

            # Add order-level KPIs to data_tables.csv
            data_table_path = "app/assets/data/data_tables.csv"
            try:
                data_tables = pd.read_csv(data_table_path)
            except FileNotFoundError:
                data_tables = pd.DataFrame()

            order_row = {
                "OrderDate": st.session_state["order_metadata"]["order_date"],
                "InvoiceNumber": st.session_state["order_metadata"]["invoice_number"],
                "Customer": st.session_state["order_metadata"]["customer_name"],
                **order_metrics
            }

            data_tables = pd.concat([data_tables, pd.DataFrame([order_row])], ignore_index=True)

            try:
                # Save updated datasets
                df.to_csv("app/assets/data/data.csv", index=False)
                data_tables.to_csv(data_table_path, index=False)
                st.success("Order and metrics have been added successfully!")

                # Clear session state after saving
                st.session_state["order_entries"] = []
                st.session_state["order_metadata"] = {"order_date": None, "customer_name": None, "invoice_number": None}
            except Exception as e:
                st.warning(f"Unable to write. Error: {e}")
UI()

# Execute the function to display the form
add_data()
