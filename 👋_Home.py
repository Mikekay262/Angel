import streamlit as st
from app.assets.styles.UI import UI

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
    layout="wide"
)

UI()
st.write("# Welcome to UCL Angel App! 👋")

st.sidebar.success("Select a page above.")

st.markdown(
    """
    The UCL Angel App is a data-driven, web application aimed at assisting with tasks like order fulfillment tracking, inventory management, and revenue analysis.
    It integrates features such as and **Predictive Analytics** to 
    of what Streamlit can do!
    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)
    ### See more complex demos
    - Use a neural net to [analyze the Udacity Self-driving Car Image
        Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)

