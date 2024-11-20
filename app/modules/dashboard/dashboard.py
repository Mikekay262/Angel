import streamlit as st
import pandas as pd
import altair as alt
from numerize.numerize import numerize  # Import numerize for compact number formatting
from app.assets.styles.UI import *  # Make sure this exists and contains UI()
from streamlit_extras.dataframe_explorer import dataframe_explorer
from app.utils.utils import (
    load_dataset,
    validate_and_filter_dates,
    prepare_fulfillment_metrics,
    make_donut,
    create_pareto_chart,
)

theme_plotly = None  # Define theme_plotly


def dashboard():
    # Load CSS Style
    with open('app/assets/styles/style.css') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Ensure UI function is defined in the imported module
    UI()

    # Load dataset
    df = load_dataset('app/assets/data/data.csv')

    # Sidebar date range filter
    with st.sidebar:
        st.title("Select Date Range")
        start_date = st.date_input(label="Start Date")
        end_date = st.date_input(label="End Date")

    st.error(f"Business Metrics between [{start_date}] and [{end_date}]")

    # Validate date inputs and filter data
    if start_date and end_date:
        try:
            df2 = validate_and_filter_dates(df, start_date, end_date)

            # Display dataframe explorer
            with st.expander("Filter Excel Dataset"):
                filtered_df = dataframe_explorer(df2, case=False)
                st.dataframe(filtered_df, use_container_width=True)

            # Main KPIs Section
            st.subheader("Order Fulfillment")
            b1, b2 = st.columns(2)

            # Order Fulfillment KPIs
            with b1:
                st.subheader('Order Fulfillment KPIs', divider='rainbow')

                metrics = prepare_fulfillment_metrics(df2)

                colA, colB = st.columns(2)
                with colA:
                    st.markdown("#### Fully Fulfilled")
                    st.altair_chart(make_donut(metrics['percent_fully_fulfilled'], "Fully Fulfilled", "green"))

                with colB:
                    st.markdown("#### Partially Fulfilled")
                    st.altair_chart(make_donut(metrics['percent_partially_fulfilled'], "Partially Fulfilled", "orange"))

                colA1, colB1 = st.columns(2)
                with colA1:
                    st.markdown("#### Not Fulfilled")
                    st.altair_chart(make_donut(metrics['percent_not_fulfilled'], "Not Fulfilled", "red"))

                with colB1:
                    st.markdown("#### Order Fill Rate (by QTY)")
                    st.altair_chart(make_donut(metrics['quantity_fulfill_rate'], "Order Fill Rate", "green"))

            # Order Value Metrics
            with b2:
                st.subheader('Order Value Metrics', divider='rainbow')
                from streamlit_extras.metric_cards import style_metric_cards

                col1, col2 = st.columns(2)
                col1.metric(label="Item Count:", value=numerize(metrics['item_count_total']))
                col2.metric(label="Total Order Value:", value=numerize(metrics['total_order_value']))

                col11, col22, col33 = st.columns(3)
                col11.metric(label="Revenue Actualized GHS:", value=numerize(metrics['value_actualized']))
                col22.metric(label="Revenue Lost GHS:", value=numerize(metrics['revenue_lost']))
                col33.metric(
                    label="% Revenue Actualized:",
                    value=f"{metrics['percent_revenue_actualized']:.2f}%",
                )

                # Style metric cards
                style_metric_cards(background_color="#fff", border_left_color="#F71938")

            # Pareto Analysis Section
            a1, a2 = st.columns(2)
            with a1:
                st.subheader('Pareto Analysis by Order Items', divider='rainbow')
                pareto_chart_items = create_pareto_chart(df2, 'Item', 'RevenueLost')
                st.altair_chart(pareto_chart_items, use_container_width=True)

            with a2:
                st.subheader('Pareto Analysis by Source', divider='rainbow')
                pareto_chart_customers = create_pareto_chart(df2, 'Customer', 'RevenueLost')
                st.altair_chart(pareto_chart_customers, use_container_width=True)

        except Exception as e:
            st.error(f"An error occurred during filtering: {e}")
    else:
        st.warning("Please select a valid date range.")


# Call the dashboard function to render the app
dashboard()
