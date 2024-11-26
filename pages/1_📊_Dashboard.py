import streamlit as st
import datetime
import pandas as pd
import plotly.express as px
import seaborn as sns
import altair as alt
import plotly.graph_objects as go
from numerize.numerize import numerize  # Import numerize for compact number formatting
from app.assets.styles.UI import *  # Make sure this exists and contains UI()
from matplotlib import pyplot as plt
from streamlit_extras.dataframe_explorer import dataframe_explorer


st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
st.title("📊 Dashboard")

theme_plotly = None  # Define theme_plotly

# Styled header
st.markdown(
    "<h1 style='color:#002B50; margin-top: 20px;'>⚛ Order Fulfillment Dashboard</h1>",
    unsafe_allow_html=True
)

def dashboard():
    # Load CSS Style
    with open('app/assets/styles/style.css') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    
    # Load dataset
    df = pd.read_csv('app/assets/data/data.csv')

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

            # Convert numeric columns to native Python types before using numerize
            df2['OrderValue'] = df2['OrderValue'].astype(float)
            df2['ValueActualized'] = df2['ValueActualized'].astype(float)
            df2['RevenueLost'] = df2['RevenueLost'].astype(float)

            # Display dataframe explorer
            with st.expander("Filter Excel Dataset"):
                filtered_df = dataframe_explorer(df2, case=False)
                st.dataframe(filtered_df, use_container_width=True)

            # Main KPIs Section
            st.header("Main Dashboard", divider="rainbow")
            b1, b2 = st.columns(2)

            ### ORDER FULFILMENT SECTION ###
            with b1:  
                st.subheader('Fulfillment KPIs', divider='rainbow')
                ##ADD DOUGHNUT GRAPHS HERE!!!!
                
                ## CALCULATIONS ##
                item_count_total = int(df2.Item.count())
                fully_fulfilled_items = len(df2[df2['QuantityFulfilled'] == df2['QuantityOrdered']])
                percent_fully_fulfilled = (fully_fulfilled_items / item_count_total) * 100
                partially_fulfilled_items = len(df2[(df2['QuantityFulfilled'] > 0) & (df2['QuantityFulfilled'] < df2['QuantityOrdered'])])
                percent_partially_fulfilled = (partially_fulfilled_items / item_count_total) * 100
                items_not_fulfilled = len(df2[df2['QuantityFulfilled'] == 0])
                percent_not_fulfilled = (items_not_fulfilled / item_count_total) * 100
                quantity_fulfill_rate = (df2['QuantityFulfilled'].sum() / df2['QuantityOrdered'].sum()) * 100

                # Use the provided metrics for fulfillment status
                item_count_total = int(df2.Item.count())
                fully_fulfilled_items = len(df2[df2['QuantityFulfilled'] == df2['QuantityOrdered']])
                percent_fully_fulfilled = (fully_fulfilled_items / item_count_total) * 100

                partially_fulfilled_items = len(df2[(df2['QuantityFulfilled'] > 0) & (df2['QuantityFulfilled'] < df2['QuantityOrdered'])])
                percent_partially_fulfilled = (partially_fulfilled_items / item_count_total) * 100

                items_not_fulfilled = len(df2[df2['QuantityFulfilled'] == 0])
                percent_not_fulfilled = (items_not_fulfilled / item_count_total) * 100

                quantity_fulfill_rate = (df2['QuantityFulfilled'].sum() / df2['QuantityOrdered'].sum()) * 100

                # Function to generate the donut chart
                def make_donut(input_response, input_text, input_color):
                    # Set chart colors based on the input color
                    color_mapping = {
                        'blue': ['#29b5e8', '#155F7A'],
                        'green': ['#27AE60', '#12783D'],  # Fully fulfilled
                        'orange': ['#F39C12', '#875A12'],  # Partially fulfilled
                        'red': ['#E74C3C', '#781F16'],  # Not fulfilled
                    }
                    chart_color = color_mapping.get(input_color, ['#CCCCCC', '#888888'])  # Default color

                    # Data for the chart
                    source = pd.DataFrame({
                        "Topic": ['', input_text],
                        "% value": [100 - input_response, input_response]
                    })
                    source_bg = pd.DataFrame({
                        "Topic": ['', input_text],
                        "% value": [100, 0]
                    })

                    # Plot foreground donut
                    plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
                        theta="% value",
                        color=alt.Color("Topic:N",
                                        scale=alt.Scale(
                                            domain=[input_text, ''],
                                            range=chart_color),
                                        legend=None),
                    ).properties(width=150, height=150)

                    # Text overlay on the donut chart
                    text = plot.mark_text(align='center', color=chart_color[0], font="Lato", fontSize=20, fontWeight=600, fontStyle="italic").encode(
                        text=alt.value(f'{input_response:.2f} %')
                    )

                    # Background donut chart
                    plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
                        theta="% value",
                        color=alt.Color("Topic:N",
                                        scale=alt.Scale(
                                            domain=[input_text, ''],
                                            range=chart_color),
                                        legend=None),
                    ).properties(width=150, height=150)

                    return plot_bg + plot + text

                # Display the Donut Charts for Fulfillment Metrics
                
                colA, colB = st.columns(2)
                with colA:
                    st.markdown("#### Fully Fulfilled")
                    st.altair_chart(make_donut(percent_fully_fulfilled, "Fully Fulfilled", "green"))

                with colB:
                    st.markdown("#### Partially Fulfilled")
                    st.altair_chart(make_donut(percent_partially_fulfilled, "Partially Fulfilled", "orange"))

                colA1, colB1 = st.columns(2)
                with colA1:
                    st.markdown("#### Not Fulfilled")
                    st.altair_chart(make_donut(percent_not_fulfilled, "Not Fulfilled", "red"))
                        
                with colB1:
                    st.markdown("#### Order Fill Rate(by QTY)")
                    st.altair_chart(make_donut(quantity_fulfill_rate, "Order Fill Rate", "green"))
                            
                            ##### SECTION END FOR FULLFILMENT METRICS######

            # Metric cards section (Revenue metrics)
            with b2:
                st.subheader('Order Value Metrics', divider='rainbow')
                from streamlit_extras.metric_cards import style_metric_cards
                col1, col2 = st.columns(2)
                col1.metric(label="Item Count:", value=numerize(int(df2.Item.count())), delta="Number of Items Per Order")
                col2.metric(label="Total Order Value:", value=numerize(float(df2.OrderValue.sum())), delta=numerize(float(df2.OrderValue.median())))
                
                col11, col22, col33 = st.columns(3)
                col11.metric(label="Revenue Actualized GHS:", value=numerize(float(df2.ValueActualized.sum())), delta="High Price")
                col22.metric(label="Revenue Lost GHS:", value=numerize(float(df2.RevenueLost.sum())), delta="Low Price")
                
                # Calculate % Revenue Actualized
                total_order_value = float(df2.OrderValue.sum())  # Ensure native type
                value_actualized = float(df2.ValueActualized.sum())  # Ensure native type
                percent_revenue_actualized = (value_actualized / total_order_value) * 100 if total_order_value > 0 else 0

                # Update the metric to display the percentage
                col33.metric(label="% Revenue Actualized:", value=f"{percent_revenue_actualized:.2f}%", delta="Percentage of Revenue Fulfilled")
                
                # Style metric cards
                style_metric_cards(background_color="#fff", border_left_color="#F71938", border_color="#1f66bd", box_shadow="#F71938")

            # PARETO ANALYSIS SECTION
            #st.subheader("Pareto Analysis", divider="rainbow")
            a1, a2 = st.columns(2)
            with a1:
                st.subheader('Pareto Analysis: By Items', divider='rainbow')
                source = df2
                                # Function to create Pareto Graph for Revenue Lost
                def create_pareto_chart(source):
                    # Group by Items and calculate total revenue lost
                    revenue_lost_df = source.groupby('Item', as_index=False)['RevenueLost'].sum()

                    # Sort by revenue lost in descending order
                    revenue_lost_df = revenue_lost_df.sort_values('RevenueLost', ascending=False)

                    # Add a cumulative percentage column
                    revenue_lost_df['CumulativePercentage'] = revenue_lost_df['RevenueLost'].cumsum() / revenue_lost_df['RevenueLost'].sum() * 100

                    # Create Pareto Chart using Altair
                    base = alt.Chart(revenue_lost_df).encode(
                        x=alt.X('Item:N', sort='-y', title='Item'),
                    )

                    # Bar chart for revenue lost
                    bar_chart = base.mark_bar(color='#F39C12').encode(
                        y=alt.Y('RevenueLost:Q', title='Revenue Lost')
                    )

                    # Line chart for cumulative percentage
                    line_chart = base.mark_line(color='#2E86C1', interpolate='monotone').encode(
                        y=alt.Y('CumulativePercentage:Q', title='Cumulative %'),
                        tooltip=['Item', 'RevenueLost', 'CumulativePercentage']
                    )

                    # Overlay the two charts and add a secondary axis
                    #threshold_line = alt.Chart(pd.DataFrame({'y': [80]})).mark_rule(color='red', strokeDash=[5, 5]).encode(y='y:Q')

                    combined_chart = alt.layer(bar_chart, line_chart).resolve_scale(
                        y='independent'
                    ).properties(
                        title="Pareto Chart: Products Contributing to Revenue Lost",
                        width=800,
                        height=400
                    )
                    
                    return combined_chart

                # Call the function and display the Pareto chart
                pareto_chart = create_pareto_chart(df2)
                st.altair_chart(pareto_chart, use_container_width=True)

            with a2:
            
                st.subheader('By Source', divider='rainbow')
                source = df2
                                # Function to create Pareto Graph for Revenue Lost
                def create_pareto_chart(source):
                    # Group by Items and calculate total revenue lost
                    revenue_lost_df = source.groupby('Customer', as_index=False)['RevenueLost'].sum()

                    # Sort by revenue lost in descending order
                    revenue_lost_df = revenue_lost_df.sort_values('RevenueLost', ascending=False)

                    # Add a cumulative percentage column
                    revenue_lost_df['CumulativePercentage'] = revenue_lost_df['RevenueLost'].cumsum() / revenue_lost_df['RevenueLost'].sum() * 100

                    # Create Pareto Chart using Altair
                    base = alt.Chart(revenue_lost_df).encode(
                        x=alt.X('Customer:N', sort='-y', title='Customer'),
                    )

                    # Bar chart for revenue lost
                    bar_chart = base.mark_bar(color='#F39C12').encode(
                        y=alt.Y('RevenueLost:Q', title='Revenue Lost')
                    )

                    # Line chart for cumulative percentage
                    line_chart = base.mark_line(color='#2E86C1', interpolate='monotone').encode(
                        y=alt.Y('CumulativePercentage:Q', title='Cumulative %'),
                        tooltip=['Customer', 'RevenueLost', 'CumulativePercentage']
                    )

                    # Overlay the two charts and add a secondary axis
                    combined_chart = alt.layer(bar_chart, line_chart).resolve_scale(
                        y='independent'
                    ).properties(
                        title="Pareto Chart: Sources Contributing to Revenue Lost",
                        width=800,
                        height=400
                    )

                    return combined_chart

                # Call the function and display the Pareto chart
                pareto_chart = create_pareto_chart(df2)
                st.altair_chart(pareto_chart, use_container_width=True)


            # Trend Analysis
            st.header("Analyze Trends", divider="rainbow")
            p1, p2 = st.columns(2) 
            
            with p1:
                st.subheader('Visualize Trends', divider='rainbow')
                            
                            # Load data
                trend_data = pd.read_csv('app/assets/data/data_tables.csv')

                # Customer selection
                customer_options = ['All Customers'] + trend_data['Customer'].unique().tolist()
                selected_customer = st.selectbox('Select Customer:', customer_options)

                # Filter data by date and customer
                trend_data['OrderDate'] = pd.to_datetime(trend_data['OrderDate'])
                filtered_data = trend_data[
                    (trend_data['OrderDate'] >= pd.to_datetime(start_date)) &
                    (trend_data['OrderDate'] <= pd.to_datetime(end_date))
                ]

                if selected_customer != 'All Customers':
                    filtered_data = filtered_data[filtered_data['Customer'] == selected_customer]

                # Interval selection
                interval_options = ['Daily', 'Weekly', 'Monthly', 'Quarterly']
                selected_interval = st.selectbox('Select Interval for Analysis:', interval_options)

                # Resample data based on the selected interval
                if selected_interval == 'Daily':
                    filtered_data['Interval'] = filtered_data['OrderDate']
                elif selected_interval == 'Weekly':
                    filtered_data['Interval'] = filtered_data['OrderDate'].dt.to_period('W').apply(lambda r: r.start_time)
                elif selected_interval == 'Monthly':
                    filtered_data['Interval'] = filtered_data['OrderDate'].dt.to_period('M').apply(lambda r: r.start_time)
                elif selected_interval == 'Quarterly':
                    filtered_data['Interval'] = filtered_data['OrderDate'].dt.to_period('Q').apply(lambda r: r.start_time)

                # User selection for trend analysis
                trend_options = [
                    "ItemCount", "percentage_fully_fulfilled", "percentage_partially_fulfilled",
                    "percentage_not_fulfilled", "quantity_fulfill_rate", "OrderValue",
                    "RevenueActualized", "RevenueLost", "percent_revenue_actualized"
                ]
                selected_trend = st.selectbox('Select Trend to Analyze:', trend_options)

                # Group by Interval and aggregate the selected trend
                trend_analysis = filtered_data.groupby('Interval')[selected_trend].sum().reset_index()

                # Plot bar chart using Altair
                chart = alt.Chart(trend_analysis).mark_bar(color='#2E86C1').encode(
                    x=alt.X('Interval:T', title=selected_interval),
                    y=alt.Y(selected_trend, title=selected_trend),
                    tooltip=['Interval', selected_trend]
                ).properties(
                    title=f'{selected_trend} Over Time ({selected_customer}, {selected_interval})',
                    width='container',
                    height=400
                )

                # Display the chart
                st.altair_chart(chart, use_container_width=True)
                
            with p2:
                st.subheader('Compare Trends', divider='rainbow')
                                        
                # Load data
                data = pd.read_csv('app/assets/data/data_tables.csv')
                data['OrderDate'] = pd.to_datetime(data['OrderDate'])

                # Customer selection (Single select instead of multi-select)
                customer_list = ['All Customers'] + data["Customer"].unique().tolist()
                selected_customer = st.selectbox("Select Customer:", customer_list, key="customer_selectbox")
                
                # Metric selection (allowing multiple selections)
                metrics = [
                    "ItemCount", "percentage_fully_fulfilled", "percentage_partially_fulfilled",
                    "percentage_not_fulfilled", "quantity_fulfill_rate", "OrderValue",
                    "RevenueActualized", "RevenueLost", "percent_revenue_actualized"
                ]
                selected_metrics = st.multiselect("Select Metrics to Plot:", metrics, default=["OrderValue"], key="metrics_multiselect")

                # Interval selection
                interval_options = ['Daily', 'Weekly', 'Monthly', 'Quarterly']
                selected_interval = st.selectbox('Select Interval for Analysis:', interval_options, key="interval_selectbox")

                # Filter data by customer
                filtered_data = data.copy()
                if selected_customer != "All Customers":
                    filtered_data = filtered_data[filtered_data["Customer"] == selected_customer]
                else:
                    filtered_data["Customer"] = "All Customers"

                # Resample data based on the selected interval
                if selected_interval == 'Daily':
                    filtered_data['Interval'] = filtered_data['OrderDate']
                elif selected_interval == 'Weekly':
                    filtered_data['Interval'] = filtered_data['OrderDate'].dt.to_period('W').apply(lambda r: r.start_time)
                elif selected_interval == 'Monthly':
                    filtered_data['Interval'] = filtered_data['OrderDate'].dt.to_period('M').apply(lambda r: r.start_time)
                elif selected_interval == 'Quarterly':
                    filtered_data['Interval'] = filtered_data['OrderDate'].dt.to_period('Q').apply(lambda r: r.start_time)

                # Aggregate data based on Interval and selected metrics
                trend_analysis = filtered_data.groupby(['Interval']).agg({metric: 'sum' for metric in selected_metrics}).reset_index()

                # Melt data for easier visualization (long format)
                trend_analysis_melted = trend_analysis.melt(id_vars=['Interval'], var_name='Metric', value_name='Value')

                # Plotting the line chart
                chart = alt.Chart(trend_analysis_melted).mark_line().encode(
                    x=alt.X('Interval:T', title=selected_interval),
                    y=alt.Y('Value:Q', title='Metric Value'),
                    color=alt.Color('Metric:N', title="Metrics"),
                    tooltip=['Interval:T', 'Metric:N', 'Value:Q']
                ).properties(
                    title=f'Trend Comparison for Selected Metrics ({selected_interval} Interval)',
                    width='container',
                    height=400
                )

                # Display the chart
                st.altair_chart(chart, use_container_width=True)
        except Exception as e:
            st.error(f"An error occurred during filtering: {e}")
    else:
        st.warning("Please select a valid date range.")
        
        
        
         # Ensure UI function is defined in the imported module
    UI()  

# Call the dashboard function to render the app
dashboard()