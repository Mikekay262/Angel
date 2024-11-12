import os
import sys
import streamlit as st
import app.utils.utils as ut

st.set_page_config(
    layout = 'wide',
    page_title = 'UCL Angel App',
)

st.header( "Welcome to UCL Angel App", divider=True)
# Add the parent directory of 'app' to sys.path
sys.path.append("C:/Angel")

# Dynamically build correct paths for each module
base_dir = "C:/Angel"
dashboard_path = os.path.join(base_dir, "app", "order_fulfillment", "dashboard.py")
data_tables_path = os.path.join(base_dir, "app", "data_tables.py")
# alerts_path = os.path.join(base_dir, "reports", "alerts.py")
order_tracker_path = os.path.join(base_dir, "app", "order_fulfillment", "order_tracker.py")
demand_forecast_path = os.path.join(base_dir, "app", "requisition_automation", "demand_forecast.py")
product_settings_path = os.path.join(base_dir, "app", "product_settings.py")
login_path = os.path.join(base_dir, "app", "login.py")

#st.header("Welcome to UCL Angel App", divider=True)

# Define pages for navigation
dashboard = st.Page(dashboard_path, title="Dashboard", icon=":material/bar_chart_4_bars:", default=True)
data_tables = st.Page(data_tables_path, title="Data Tables", icon=":material/dataset:")
# alerts = st.Page(alerts_path, title="System alerts", icon=":material/notification_important:")
order_fulfillment_tracker = st.Page(order_tracker_path, title="Order Fulfillment Tracker", icon=":material/database:")
demand_forecaster = st.Page(demand_forecast_path, title="Demand Forecaster", icon=":material/monitoring:")
product_settings = st.Page(product_settings_path, title="Product Settings", icon=":material/settings:")
login = st.Page(login_path, title="Login/Logout", icon=":material/logout:")

# Navigation configuration
pg = st.navigation(
    {
        "Account": [login],
        "Reports": [dashboard, data_tables],  # Alerts can be uncommented when implemented
        "Tools": [order_fulfillment_tracker, demand_forecaster],
        "Settings": [product_settings]
    }
)

# Run the selected page
pg.run()

# Add version information at the bottom of the sidebar
st.sidebar.write("**App Version:** 1.0.0")
st.sidebar.write("© 2024 UCL Angel App")
