import streamlit as st
from app.assets.styles.UI import UI

st.set_page_config(
    page_title="UCL Angel App",
    page_icon="👼",
    layout="wide"
)

UI()

# Main Heading
st.title("Welcome to UCL Angel App! 👋")

# Sidebar
st.sidebar.success("Select a feature from the menu.")

# Introduction Section
st.markdown(
    """
    ## About the UCL Angel App  
    The **UCL Angel App** is an innovative, data-driven tool designed to support branch-level management with critical tasks such as:  
    - **Order Fulfillment Tracking**  
    - **Inventory Management**  
    - **Revenue Analysis**  

    It incorporates advanced features like an **Order Fulfillment Tracker**, a **Business Intelligence Dashboard**, and a **Demand Forecaster**.  

    ### Advanced Demand Forecasting  
    Our **Demand Forecaster** leverages a hybrid **Facebook Prophet-ARIMA framework**, combining the strengths of both models to accurately predict demand trends.  
    - **Seasonal and Non-Seasonal Data:** Captures complex patterns in pharmaceutical sales.  
    - **Optimized Stocking:** Reduces losses from overstocking and understocking.  
    - **Revenue Maximization:** Helps optimize inventory decisions for better profitability.  
    """
)

# Call-to-Action Section
st.markdown(
    """
    ---
    ## Learn More  
    - Explore **forecasting techniques**: [Neptune.ai](https://neptune.ai/blog/arima-vs-prophet-vs-lstm)  
    - Access the app's **documentation**: [Streamlit Docs](https://docs.streamlit.io)  
    - Share your thoughts: [Send Feedback](https://discuss.streamlit.io)  

    ---
    ## Explore Other Projects  
    - Analyze [NYC Rideshare Data](https://github.com/streamlit/demo-uber-nyc-pickups)  
    - Check out our [Self-Driving Demo](https://github.com/streamlit/demo-self-driving)  
    """
)
