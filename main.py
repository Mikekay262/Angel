import os
import sys
import streamlit as st


# Optional page layout and theme
st.set_page_config(page_title="Analytics", page_icon="🌎", layout="wide")



#st.header( "Welcome to UCL Angel App", divider=True)
# Add the parent directory of 'app' to sys.path
sys.path.append("C:/Angel")

# Dynamically build correct paths for each module
base_dir = "C:/Angel"
dashboard_path = os.path.join(base_dir, "app", "modules", "dashboard", "dashboard.py")
data_tables_path = os.path.join(base_dir, "app", "modules", "data_tables", "data_tables.py")
order_tracker_path = os.path.join(base_dir, "app", "modules", "order_fulfillment_tracker", "add_data.py")
demand_forecast_path = os.path.join(base_dir, "app", "modules", "demand_forecaster", "forecaster.py")
product_settings_path = os.path.join(base_dir, "app", "modules", "product_settings", "product_settings.py")
login_path = os.path.join(base_dir, "app", "modules", "login", "login.py")

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
