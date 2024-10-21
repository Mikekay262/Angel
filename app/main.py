import streamlit as st

# Main title of the app
st.title('Welcome to Angel App')

# Sidebar for navigation between different modules
st.sidebar.title("Navigation")
app_mode = st.sidebar.selectbox("Choose the app mode",
                                ["Order Fulfillment Tracker", "Requisition Automation"])

# Navigation logic
if app_mode == "Order Fulfillment Tracker":
    st.subheader("Order Fulfillment Tracker")
    st.write("This section will contain order fulfillment metrics and performance dashboards.")
    
    # Add more details or call external scripts to handle this section
    
elif app_mode == "Requisition Automation":
    st.subheader("Requisition Automation and Demand Forecasting")
    st.write("This section will contain order requisition automation and demand forecasting.")
    
    # Add more details or call external scripts to handle this section

