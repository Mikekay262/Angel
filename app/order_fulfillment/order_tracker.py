import streamlit as st
import pandas as pd
import sys
import os
import plotly.express as px
from streamlit.components.v1 import html

# Adding the preprocess path to import inventory loading function
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../scripts')))
from preprocess import load_and_clean_inventory

# Remove or comment this line to avoid the error
# st.set_page_config(layout="wide")

# Define custom CSS for KPIs, progress bars, and card layout
st.markdown("""
    <style>
    body {
        background-color: #f8f9fa;
    }

    h1 {
        font-family: Arial, sans-serif;
        font-size: 2.5em;
        color: #343a40;
        text-align: center;
        padding-bottom: 10px;
    }

    .section-header {
        font-size: 1.5em;
        color: #495057;
        padding-top: 10px;
        margin-bottom: 20px;
    }

    /* Style KPIs using cards */
    .kpi-card {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        text-align: center;
        transition: transform 0.2s;
    }

    .kpi-card:hover {
        transform: scale(1.02);  /* Slight zoom on hover for interactivity */
    }

    .kpi-header {
        font-size: 1.2em;
        font-weight: bold;
        color: #6c757d;
    }

    .kpi-value {
        font-size: 2.0em;
        color: #343a40;
        font-weight: bold;
    }

    .progress-circle {
        position: relative;
        display: inline-block;
        width: 80px;
        height: 80px;
        background: conic-gradient(#28a745 calc(var(--value) * 1%), #e9ecef calc(var(--value) * 1%));
        border-radius: 50%;
        line-height: 80px;
        text-align: center;
        font-weight: bold;
        color: #495057;
        font-size: 1.1em;
    }

    .progress-circle::before {
        content: attr(data-label);
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 0.9em;
        font-weight: bold;
    }

    .progress-title {
        text-align: center;
        font-weight: bold;
        margin-top: 10px;
        color: #495057;
    }
    </style>
""", unsafe_allow_html=True)

# Define the order fulfillment tracker function
def order_fulfillment_tracker():
    # Title of the section
    st.title('Order Fulfillment Tracker')

    # Path to inventory file
    inventory_path = "data/raw/inventory.csv"

    # Load inventory data
    inventory_df = load_and_clean_inventory(inventory_path)

    # Create two columns: left for order input, right for KPIs (70/30 screen ratio)
    left_col, right_col = st.columns([7, 3])  # 70% left, 30% right

    # Input for customer name and order date (optional) in the left column
    with left_col:
        st.markdown("<div class='section-header'>Enter Order Information</div>", unsafe_allow_html=True)
        customer_name = st.text_input("Enter Customer Name")
        order_date = st.date_input("Order Date")

    # Initialize session state to store multiple items for a single order
    if "order_entries" not in st.session_state:
        st.session_state["order_entries"] = []

    # Add a placeholder option to the item list
    item_options = ['Select Item'] + list(inventory_df['Item'])

    # Create a form for entering multiple items in the order within the left column
    with left_col.form("order_entry_form", clear_on_submit=True):
        st.write("Enter Order Details:")

        # Select item from inventory with a placeholder
        item_selected = st.selectbox("Select Item", item_options)

        # Input requested and fulfilled quantities
        quantity_requested = st.number_input("Quantity Requested", min_value=0)
        quantity_fulfilled = st.number_input("Quantity Fulfilled", min_value=0)

        # Submit button to add item to the list
        add_item = st.form_submit_button("Add Item to Order")

        # Input validation
        if add_item:
            if not customer_name:
                st.error("Please enter the customer name.")
            elif not order_date:
                st.error("Please select an order date.")
            elif item_selected == 'Select Item':
                st.error("Please select a valid item.")
            elif quantity_fulfilled > quantity_requested:
                st.error("Fulfilled quantity cannot exceed the requested quantity.")
            else:
                st.session_state["order_entries"].append({
                    "Customer": customer_name,
                    "Order Date": order_date,
                    "Item": item_selected,
                    "Quantity Requested": quantity_requested,
                    "Quantity Fulfilled": quantity_fulfilled,
                    "Price": inventory_df[inventory_df['Item'] == item_selected]['Price'].values[0]
                })

    # Show the current order details being entered (session state list) in the left column
    if st.session_state["order_entries"]:
        order_df = pd.DataFrame(st.session_state["order_entries"])
        
        # Display order details in the left column
        with left_col:
            st.write("### Current Order Details")
            st.write(order_df)

    # Function to display KPIs using circular progress bars and card layout
    def display_kpi_card(label, value, icon=None, tooltip=None):
        icon_html = f"<i class='fa {icon}'></i> " if icon else ""
        tooltip_html = f"title='{tooltip}'" if tooltip else ""
        st.markdown(f"""
            <div class="kpi-card" {tooltip_html}>
                <span class="kpi-header">{icon_html}{label}</span>
                <div class="kpi-value">{value}</div>
            </div>
        """, unsafe_allow_html=True)

    # Function to display progress circles for percentage KPIs
    def display_progress_circle(label, value):
        percentage = min(max(value, 0), 100)  # Ensure value is between 0 and 100
        st.markdown(f"""
            <div class="progress-circle" style="--value:{percentage};" data-label="{value:.2f}%"></div>
            <div class="progress-title">{label}</div>
        """, unsafe_allow_html=True)

    # Move the 'Submit Order' button into the right column and ensure it only works if there are entries
    with right_col:
        if st.session_state["order_entries"]:  # Only show Submit if items are added
            st.write("### Order KPIs")
            
            if st.button("Submit Order"):
                st.write(f"Order for {customer_name} on {order_date} submitted successfully!")

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

                    # Percentage of Not Fulfilled Items (requested > 0, but fulfilled == 0)
                    not_fulfilled_items = len(order_df[order_df['Quantity Fulfilled'] == 0])
                    percent_not_fulfilled = (not_fulfilled_items / total_items) * 100

                    # Order Fill Rate (by quantity)
                    quantity_fulfill_rate = (order_df['Quantity Fulfilled'].sum() / order_df['Quantity Requested'].sum()) * 100

                    # Perfect Order Rate: number of fully fulfilled orders
                    perfect_order_rate = (fully_fulfilled_items / total_items) * 100

                    # Revenue Loss Due to Unfulfilled Orders
                    revenue_loss = order_df['Expected Revenue'].sum() - order_df['Actual Revenue'].sum()

                    return (order_df, percent_fully_fulfilled, percent_partially_fulfilled, 
                            percent_not_fulfilled, quantity_fulfill_rate, perfect_order_rate, 
                            revenue_loss)

                # Calculate KPIs for the full order
                (order_df, percent_fully_fulfilled, percent_partially_fulfilled, 
                percent_not_fulfilled, quantity_fulfill_rate, perfect_order_rate, 
                revenue_loss) = calculate_kpis(order_df)

                # Display main KPIs in a card layout
                display_kpi_card("Total Expected Revenue", f"GHS {order_df['Expected Revenue'].sum():,.2f}", icon="fa-money", tooltip="Total potential revenue from the requested quantities.")
                display_kpi_card("Total Actual Revenue", f"GHS {order_df['Actual Revenue'].sum():,.2f}", icon="fa-line-chart", tooltip="Revenue generated from the fulfilled quantities.")
                display_kpi_card("Revenue Loss", f"GHS {revenue_loss:,.2f}", icon="fa-exclamation-circle", tooltip="Revenue lost due to unfulfilled or partially fulfilled orders.")

                # Display percentage-based KPIs using circular progress indicators with labels
                st.write("### Fulfillment KPIs")
                display_progress_circle("Order Fill Rate", quantity_fulfill_rate)
                display_progress_circle("Perfect Order Rate", perfect_order_rate)
                display_progress_circle("Fully Fulfilled", percent_fully_fulfilled)
                display_progress_circle("Partially Fulfilled", percent_partially_fulfilled)
                display_progress_circle("Not Fulfilled", percent_not_fulfilled)
                
                # Pie chart for fully, partially, and not fulfilled
                fulfillment_data = pd.DataFrame({
                    "Fulfillment Type": ["Fully Fulfilled", "Partially Fulfilled", "Not Fulfilled"],
                    "Percentage": [percent_fully_fulfilled, percent_partially_fulfilled, percent_not_fulfilled]
                })

                st.write("### Fulfillment Distribution")
                fulfillment_pie = px.pie(
                    fulfillment_data, 
                    values="Percentage", 
                    names="Fulfillment Type", 
                    title="Fulfillment Distribution"
                )
                st.plotly_chart(fulfillment_pie)

                # Fill Rate by Customer
                st.write("### Fill Rate by Customer")
                customer_fill_rate = order_df.groupby('Customer', group_keys=False).apply(
                    lambda x: (x['Quantity Fulfilled'].sum() / x['Quantity Requested'].sum()) * 100
                ).reset_index(drop=True)
                st.write(customer_fill_rate)

                # Top 10 Under-Fulfilled Items
                st.write("### Top 10 Under-Fulfilled Items")
                under_fulfilled_items = order_df.assign(
                    Difference=lambda df: df['Quantity Requested'] - df['Quantity Fulfilled']
                ).sort_values('Difference', ascending=False).head(10)
                st.write(under_fulfilled_items[['Item', 'Quantity Requested', 'Quantity Fulfilled', 'Difference']])

                # Allow user to download the order data as CSV
                st.write("### Export Report")
                st.download_button(label="Download CSV", data=order_df.to_csv(index=False), 
                                   file_name=f"order_fulfillment_report_{customer_name}_{order_date}.csv", mime="text/csv")

                # Clear session state after submission
                st.session_state["order_entries"] = []

        else:
            st.write("No items added to the order yet. Please add items before submitting.")
