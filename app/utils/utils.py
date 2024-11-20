import pandas as pd
import streamlit as st
import altair as alt
import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns



#utils for add_data.py
def load_and_clean_inventory(file_path):
    """Load and clean the inventory dataset."""
    inventory_df = pd.read_csv(file_path)
    inventory_df.fillna(0, inplace=True)  # Handle missing data
    return inventory_df

def calculate_kpis(order_df):
    """Calculate KPIs and add columns to the DataFrame."""
    if 'QuantityOrdered' in order_df and 'QuantityFulfilled' in order_df and 'Price' in order_df:
        order_df['Expected Revenue'] = order_df['QuantityOrdered'] * order_df['Price']
        order_df['Actual Revenue'] = order_df['QuantityFulfilled'] * order_df['Price']
        order_df['Revenue Lost'] = order_df['Expected Revenue'] - order_df['Actual Revenue']
        order_df['Percent Revenue Actualized'] = (order_df['Actual Revenue'] / order_df['Expected Revenue']) * 100
        order_df['Percent Revenue Actualized'].fillna(0, inplace=True)  # Handle NaN
    else:
        st.warning("Required columns for KPI calculation are missing!")
    return order_df

def ensure_columns_exist(df, columns):
    """Ensure necessary columns exist in the DataFrame."""
    for column in columns:
        if column not in df.columns:
            df[column] = 0  # Initialize missing columns
    return df

def validate_invoice_number(invoice_number, existing_invoice_numbers):
    """Check if the invoice number already exists."""
    return invoice_number in existing_invoice_numbers

def initialize_session_state():
    """Initialize session state variables."""
    if "order_entries" not in st.session_state:
        st.session_state["order_entries"] = []

    if "order_metadata" not in st.session_state:
        st.session_state["order_metadata"] = {
            "order_date": None,
            "customer_name": None,
            "invoice_number": None
        }

def append_order_entry(item, quantity_ordered, quantity_fulfilled, inventory_df):
    """Append an order entry to the session state."""
    price = inventory_df[inventory_df['Item'] == item]['Price'].values[0]
    order_value = quantity_ordered * price  # Calculate OrderValue
    value_actualized = quantity_fulfilled * price  # Calculate ValueActualized
    revenue_lost = order_value - value_actualized

    st.session_state["order_entries"].append({
        "InvoiceNumber": st.session_state["order_metadata"]["invoice_number"],
        "OrderDate": st.session_state["order_metadata"]["order_date"],
        "Customer": st.session_state["order_metadata"]["customer_name"],
        "Item": item,
        "QuantityOrdered": quantity_ordered,
        "QuantityFulfilled": quantity_fulfilled,
        "Price": price,
        "OrderValue": order_value,
        "ValueActualized": value_actualized,
        "RevenueLost": revenue_lost,
    })

##utils for dashboard.py
def load_dataset(filepath):
    """Load dataset and preprocess."""
    df = pd.read_csv(filepath)
    if df['OrderDate'].dtype != 'datetime64[ns]':
        df['OrderDate'] = pd.to_datetime(df['OrderDate'], errors='coerce')
    return df


def validate_and_filter_dates(df, start_date, end_date):
    """Filter dataset based on date range."""
    return df[(df['OrderDate'] >= pd.Timestamp(start_date)) & (df['OrderDate'] <= pd.Timestamp(end_date))]


def prepare_fulfillment_metrics(df):
    """Calculate metrics for order fulfillment."""
    item_count_total = int(df.Item.count())
    fully_fulfilled_items = len(df[df['QuantityFulfilled'] == df['QuantityOrdered']])
    partially_fulfilled_items = len(
        df[(df['QuantityFulfilled'] > 0) & (df['QuantityFulfilled'] < df['QuantityOrdered'])]
    )
    items_not_fulfilled = len(df[df['QuantityFulfilled'] == 0])
    quantity_fulfill_rate = (df['QuantityFulfilled'].sum() / df['QuantityOrdered'].sum()) * 100

    total_order_value = float(df.OrderValue.sum())
    value_actualized = float(df.ValueActualized.sum())
    revenue_lost = float(df.RevenueLost.sum())
    percent_revenue_actualized = (value_actualized / total_order_value) * 100 if total_order_value > 0 else 0

    return {
        'item_count_total': item_count_total,
        'percent_fully_fulfilled': (fully_fulfilled_items / item_count_total) * 100,
        'percent_partially_fulfilled': (partially_fulfilled_items / item_count_total) * 100,
        'percent_not_fulfilled': (items_not_fulfilled / item_count_total) * 100,
        'quantity_fulfill_rate': quantity_fulfill_rate,
        'total_order_value': total_order_value,
        'value_actualized': value_actualized,
        'revenue_lost': revenue_lost,
        'percent_revenue_actualized': percent_revenue_actualized,
    }


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



def create_pareto_chart(df, group_by_column, value_column):
    """Create a Pareto chart for analysis."""
    grouped_df = df.groupby(group_by_column, as_index=False)[value_column].sum()
    grouped_df = grouped_df.sort_values(value_column, ascending=False)
    grouped_df['CumulativePercentage'] = grouped_df[value_column].cumsum() / grouped_df[value_column].sum() * 100

    base = alt.Chart(grouped_df).encode(x=alt.X(f'{group_by_column}:N', sort='-y'))
    bar_chart = base.mark_bar(color='#F39C12').encode(y=alt.Y(f'{value_column}:Q', title=value_column))
    line_chart = base.mark_line(color='#2E86C1').encode(
        y=alt.Y('CumulativePercentage:Q', title='Cumulative %'),
        tooltip=[group_by_column, value_column, 'CumulativePercentage']
    )

    return alt.layer(bar_chart, line_chart).resolve_scale(y='independent')