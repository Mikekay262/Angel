import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import altair as alt
from app.assets.styles.UI import *  # Make sure this exists and contains UI()
from matplotlib import pyplot as plt
from streamlit_extras.dataframe_explorer import dataframe_explorer
from app.modules.order_fulfillment_tracker.add_data import add_data  # Import specific function

theme_plotly = None  # Define theme_plotly

def dashboard():
    # Load CSS Style
    with open('app/assets/styles/style.css') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Ensure UI function is defined in the imported module
    UI()  
    
    # Load dataset
    df = pd.read_csv('app/assets/data/data.csv')


    # Filter date range
    with st.sidebar:
        st.title("Select Date Range")
        start_date = st.date_input(label="Start Date")
        end_date = st.date_input(label="End Date")
    
    st.error(f"Business Metrics between [{start_date}] and [{end_date}]")

    # Filter data based on date
    df2 = df[(df['OrderDate'] >= str(start_date)) & (df['OrderDate'] <= str(end_date))]

    # Display dataframe explorer
    with st.expander("Filter Excel Dataset"):
        filtered_df = dataframe_explorer(df2, case=False)
        st.dataframe(filtered_df, use_container_width=True)

    st.subheader("Order Fulfillment")
    b1, b2 = st.columns(2)

    # Bar chart and add data section
    with b1:  
        st.subheader('Add New Record to Database', divider='rainbow')
        add_data()  # Call the imported add_data function

    # Metric cards section
    with b2:
        st.subheader('Order Fulfillment Metrics', divider='rainbow')
        from streamlit_extras.metric_cards import style_metric_cards
        col1, col2 = st.columns(2)
        col1.metric(label="Item Count:", value=df2.Product.count(), delta="Number of Items Per Order")
        col2.metric(label="Total Order Value:", value=f"{df2.TotalPrice.sum():,.0f}", delta=df2.TotalPrice.median())
        
        col11, col22, col33 = st.columns(3)
        col11.metric(label="Revenue Actualized GHS:", value=f"{df2.TotalPrice.max():,.0f}", delta="High Price")
        col22.metric(label="Revenue Lost GHS:", value=f"{df2.TotalPrice.min():,.0f}", delta="Low Price")
        col33.metric(label="% Revenue Actualized:", value=f"{df2.TotalPrice.max() - df2.TotalPrice.min():,.0f}", delta="Annual Salary Range")
        
        # Style metric cards
        style_metric_cards(background_color="#596073", border_left_color="#F71938", border_color="#1f66bd", box_shadow="#F71938")

    # Dot plot
    a1, a2 = st.columns(2)
    with a1:
        st.subheader('Customer Vs Fulfillment & Total Price', divider='rainbow')
        source = df2
        chart = alt.Chart(source).mark_circle().encode(
            x='Product',
            y='TotalPrice',
            color='Category',
        ).interactive()
        st.altair_chart(chart, theme="streamlit", use_container_width=True)

    with a2:
        st.subheader('Products & Unit Price', divider='rainbow')
        energy_source = pd.DataFrame({
            "Product": df2["Product"],
            "UnitPrice ($)": df2["UnitPrice"],
            "Date": df2["OrderDate"]
        })
        
        # Bar chart for products and unit price
        bar_chart = alt.Chart(energy_source).mark_bar().encode(
            x="month(Date):O",
            y="sum(UnitPrice ($)):Q",
            color="Product:N"
        )
        st.altair_chart(bar_chart, use_container_width=True, theme=theme_plotly)

    # Scatter plot with selected features
    p1, p2 = st.columns(2) 
    with p1:
        st.subheader('Features by Frequency', divider='rainbow')
        feature_x = st.selectbox('Select feature for x (Qualitative)', df2.select_dtypes("object").columns)
        feature_y = st.selectbox('Select feature for y (Quantitative)', df2.select_dtypes("number").columns)

        fig, ax = plt.subplots()
        sns.scatterplot(data=df2, x=feature_x, y=feature_y, hue="Product", ax=ax)
        st.pyplot(fig)

    with p2:
        st.subheader('Products & Quantities', divider='rainbow')
        source = pd.DataFrame({
            "Quantity": df2["Quantity"],
            "Product": df2["Product"]
        })
        
        bar_chart = alt.Chart(source).mark_bar().encode(
            x="sum(Quantity):Q",
            y=alt.Y("Product:N", sort="-x")
        )
        st.altair_chart(bar_chart, use_container_width=True, theme=theme_plotly)

# Call the dashboard function to render the app
dashboard()
