import streamlit as st
from order_fulfillment.order_tracker import order_fulfillment_tracker


# Main title of the app
st.title('Welcome to UCL Angel App')


# Sidebar for navigation between different modules
st.sidebar.title("Navigation")
app_mode = st.sidebar.selectbox(
    "Choose the app mode",
    ["Dashboard", "Order Fulfillment Tracker", "Requisition Automation"]
)

# Navigation logic to load different sections of the app
if app_mode == "Order Fulfillment Tracker":
    st.subheader("Order Fulfillment Tracker")
    order_fulfillment_tracker()  # Call the order tracker functionality

elif app_mode == "Requisition Automation":
    st.subheader("Requisition Automation and Demand Forecasting")
    st.write("This section will contain order requisition automation and demand forecasting.")

