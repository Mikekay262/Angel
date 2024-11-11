import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import date
from numerize import numerize  # Importing numerize for currency formatting

# Set the page layout to wide mode
st.set_page_config(layout="wide")

# Helper function to format large numbers as currency
def format_currency(value):
    return f"GHS {numerize.numerize(value)}"

# Custom CSS styling
st.markdown("""
    <style>
        .big-metric {
            font-size: 32px;
            font-weight: bold;
            margin-top: -5px;
        }
        .sub-metric {
            font-size: 16px;
            color: #4CAF50; /* green color */
            margin-bottom: -10px;
        }
        .card {
            background-color: #f9f9f9;
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0px;
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Dummy data
months = ['Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb']
sales = np.random.randint(100, 500, size=len(months))
weekly_data = pd.DataFrame({
    'Day': range(18, 26),
    'Visitors': np.random.randint(1000, 3000, 8)
})

# Header section
st.title("Main Dashboard")

# Top Metrics with formatted currency values
with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown('<div class="card"><div class="sub-metric">Order Fulfillment</div><div class="big-metric">60%</div></div>', unsafe_allow_html=True)
        
    with col2:
        order_value = format_currency(6_000_000)
        st.markdown(f'<div class="card"><div class="sub-metric">Order Value</div><div class="big-metric">{order_value}</div></div>', unsafe_allow_html=True)
        
    with col3:
        value_actualized = format_currency(500_000)
        st.markdown(f'<div class="card"><div class="sub-metric">Value Actualized</div><div class="big-metric">{value_actualized}</div></div>', unsafe_allow_html=True)
        
    with col4:
        revenue_lost = format_currency(5_500_000)
        st.markdown(f'<div class="card"><div class="sub-metric">Revenue Lost</div><div class="big-metric">{revenue_lost}</div></div>', unsafe_allow_html=True)
        
    with col5:
        percentage_revenue_lost = "80%"  # This is a percentage, so no formatting is needed
        st.markdown(f'<div class="card"><div class="sub-metric">Percentage of Revenue Lost</div><div class="big-metric">{percentage_revenue_lost}</div></div>', unsafe_allow_html=True)

# Monthly Spend Chart
st.markdown("### Monthly Spend Analysis")
with st.container():
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Line chart for monthly spend
        fig, ax = plt.subplots()
        sns.lineplot(x=months, y=sales, ax=ax, marker="o", color="#3B82F6", linewidth=2)
        ax.set_title("Total Spent")
        ax.set_xlabel("")
        ax.set_ylabel("")
        st.pyplot(fig)
        
    with col2:
        # Bar chart for weekly revenue
        fig, ax = plt.subplots()
        sns.barplot(x="Day", y="Visitors", data=weekly_data, ax=ax, palette="Blues")
        ax.set_title("Weekly Revenue")
        st.pyplot(fig)

# Check Table
st.markdown("### Check Table")
data = {
    "Name": ["Horizon UI PRO", "Horizon UI Free", "Weekly Update", "Venus 3D Asset"],
    "Progress": ["17.5%", "10.8%", "21.3%", "31.5%"],
    "Quantity": [2458, 1485, 1024, 858],
    "Date": ["12 Jan 2021", "21 Feb 2021", "13 Mar 2021", "24 Jan 2021"]
}
df = pd.DataFrame(data)
st.dataframe(df)

# Daily Traffic Bar Chart
st.markdown("### Daily Traffic Analysis")
fig, ax = plt.subplots()
sns.barplot(x="Day", y="Visitors", data=weekly_data, ax=ax, palette="Purples")
ax.set_title("Daily Traffic")
st.pyplot(fig)

# Your Pie Chart
st.markdown("### Your Pie Chart")
with st.container():
    fig, ax = plt.subplots()
    pie_data = [60, 30, 10]
    labels = ["Your files", "System", "Others"]
    colors = ["#1E3A8A", "#6366F1", "#E0E7FF"]
    ax.pie(pie_data, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    st.pyplot(fig)
