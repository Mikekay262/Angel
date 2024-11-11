import os
import streamlit as st

# Session management
if "page" not in st.session_state:
    st.session_state.page = "dashboard"  # Default page

# Define page paths
base_dir = "C:/Angel"
pages = {
    "dashboard": os.path.join(base_dir, "app", "order_fulfillment", "dashboard.py"),
    "data_tables": os.path.join(base_dir, "app", "data_tables.py"),
    "alerts": os.path.join(base_dir, "reports", "alerts.py"),
    "order_tracker": os.path.join(base_dir, "app", "order_fulfillment", "order_tracker.py"),
    "demand_forecaster": os.path.join(base_dir, "app", "requisition_automation", "demand_forecast.py"),
}

# Page function stubs (for demonstration, replace with imports if needed)
def show_dashboard():
    st.title("Dashboard")
    st.write("This is the dashboard page.")

def show_data_tables():
    st.title("Data Tables")
    st.write("This is the data tables page.")

def show_alerts():
    st.title("Alerts")
    st.write("This is the alerts page.")

def show_order_tracker():
    st.title("Order Tracker")
    st.write("This is the order tracker page.")

def show_demand_forecaster():
    st.title("Demand Forecaster")
    st.write("This is the demand forecaster page.")

# Page Router
def page_router():
    page = st.session_state.page
    if page == "dashboard":
        show_dashboard()
    elif page == "data_tables":
        show_data_tables()
    elif page == "alerts":
        show_alerts()
    elif page == "order_tracker":
        show_order_tracker()
    elif page == "demand_forecaster":
        show_demand_forecaster()
    else:
        st.error("Page not found!")

# Sidebar Navigation
with st.sidebar:
    st.header("Navigation")
    st.button("Dashboard", on_click=lambda: st.session_state.update({"page": "dashboard"}))
    st.button("Data Tables", on_click=lambda: st.session_state.update({"page": "data_tables"}))
    st.button("Alerts", on_click=lambda: st.session_state.update({"page": "alerts"}))
    st.button("Order Tracker", on_click=lambda: st.session_state.update({"page": "order_tracker"}))
    st.button("Demand Forecaster", on_click=lambda: st.session_state.update({"page": "demand_forecaster"}))

# Render Selected Page
page_router()
