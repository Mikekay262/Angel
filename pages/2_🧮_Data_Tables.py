import streamlit as st
import datetime
import pandas as pd
import plotly.express as px
import seaborn as sns
import altair as alt
from numerize.numerize import numerize  # Import numerize for compact number formatting
from app.assets.styles.UI import *  # Make sure this exists and contains UI()
from matplotlib import pyplot as plt
from streamlit_extras.dataframe_explorer import dataframe_explorer

st.title("🧮 Data Tables")

def data_tables():
    # Load CSS Style
    with open('app/assets/styles/style.css') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    
    # Load dataset
    df = pd.read_csv('app/assets/data/data_tables.csv')
    
    # Convert OrderDate to datetime if not already
    if df['OrderDate'].dtype != 'datetime64[ns]':
        df['OrderDate'] = pd.to_datetime(df['OrderDate'], errors='coerce')  # Handle invalid dates

    # Sidebar date range filter
    with st.sidebar:
        st.title("Select Date Range")
         # Get the first day of the current year
        default_start_date = datetime.date(datetime.date.today().year, 1, 1)
        # Get today's date
        default_end_date = datetime.date.today()

        # Allow users to select dates with the defaults pre-filled
        start_date = st.date_input(label="Start Date", value=default_start_date)
        end_date = st.date_input(label="End Date", value=default_end_date)

    st.error(f"Business Metrics between [{start_date}] and [{end_date}]")

    # Validate date inputs and filter data
    if start_date and end_date:
        try:
            # Filter dataset based on date range
            df2 = df[(df['OrderDate'] >= pd.Timestamp(start_date)) & (df['OrderDate'] <= pd.Timestamp(end_date))]


            # Display dataframe explorer
            
            filtered_df = dataframe_explorer(df2, case=False)
            st.dataframe(filtered_df, use_container_width=True)

        except Exception as e:
            st.error(f"An error occurred during filtering: {e}")
    else:
        st.warning("Please select a valid date range.")
        

    # Ensure UI function is defined in the imported module
    UI()  

# Call the dashboard function to render the app
data_tables()