import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import altair as alt
from numerize.numerize import numerize  # Import numerize for compact number formatting
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

    # Convert OrderDate to datetime if not already
    if df['OrderDate'].dtype != 'datetime64[ns]':
        df['OrderDate'] = pd.to_datetime(df['OrderDate'], errors='coerce')  # Handle invalid dates

    # Sidebar date range filter
    with st.sidebar:
        st.title("Select Date Range")
        start_date = st.date_input(label="Start Date")
        end_date = st.date_input(label="End Date")
    
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
            st.subheader("Order Fulfillment")
            b1, b2 = st.columns(2)

            ### ORDER FULFILMENT SECTION ###
            with b1:  
                st.subheader('Order Fulfillment KPIs', divider='rainbow')
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
            a1, a2 = st.columns(2)
            with a1:
                st.subheader('Pareto Analysis by Order Items', divider='rainbow')
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
            
                st.subheader('Pareto Analysis by Source', divider='rainbow')
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


            # Scatter plot with selected features
            p1, p2 = st.columns(2) 
            with p1:
                st.subheader('Fulfillment Trends', divider='rainbow')
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

        except Exception as e:
            st.error(f"An error occurred during filtering: {e}")
    else:
        st.warning("Please select a valid date range.")

# Call the dashboard function to render the app
dashboard()
