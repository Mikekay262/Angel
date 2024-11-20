# Function to calculate KPIs
def calculate_kpis(order_df):
    # Expected Revenue = Sum of (Quantity Requested * Price)
    order_df['Expected Revenue'] = order_df['Quantity Requested'] * order_df['Price']
    
    # Actual Revenue = Sum of (Quantity Fulfilled * Price)
    order_df['Actual Revenue'] = order_df['Quantity Fulfilled'] * order_df['Price']
    
    # Percent Revenue Actualized = (Actual Revenue / Expected Revenue) * 100
    order_df['Percent Revenue Actualized'] = (order_df['Actual Revenue'] / order_df['Expected Revenue']) * 100

    # Total Items
    total_items = len(order_df)

    # Percentage of Fully Fulfilled Items
    fully_fulfilled_items = len(order_df[order_df['Quantity Fulfilled'] == order_df['Quantity Requested']])
    percent_fully_fulfilled = (fully_fulfilled_items / total_items) * 100

    # Percentage of Partially Fulfilled Items
    partially_fulfilled_items = len(order_df[(order_df['Quantity Fulfilled'] > 0) & 
                                                (order_df['Quantity Fulfilled'] < order_df['Quantity Requested'])])
    percent_partially_fulfilled = (partially_fulfilled_items / total_items) * 100

    # Percentage of Not Fulfilled Items (requested > 0, but fulfilled == 0)
    not_fulfilled_items = len(order_df[order_df['Quantity Fulfilled'] == 0])
    percent_not_fulfilled = (not_fulfilled_items / total_items) * 100

    # Order Fill Rate (by quantity)
    quantity_fulfill_rate = (order_df['Quantity Fulfilled'].sum() / order_df['Quantity Requested'].sum()) * 100

    # Perfect Order Rate: number of fully fulfilled orders
    perfect_order_rate = (fully_fulfilled_items / total_items) * 100

    # Revenue Loss Due to Unfulfilled Orders
    revenue_loss = order_df['Expected Revenue'].sum() - order_df['Actual Revenue'].sum()

    return (order_df, percent_fully_fulfilled, percent_partially_fulfilled, 
            percent_not_fulfilled, quantity_fulfill_rate, perfect_order_rate, 
            revenue_loss)

# Calculate KPIs for the full order
(order_df, percent_fully_fulfilled, percent_partially_fulfilled, 
percent_not_fulfilled, quantity_fulfill_rate, perfect_order_rate, 
revenue_loss) = calculate_kpis(order_df)

# Display main KPIs in a card layout
display_kpi_card("Total Expected Revenue", f"GHS {order_df['Expected Revenue'].sum():,.2f}", icon="fa-money", tooltip="Total potential revenue from the requested quantities.")
display_kpi_card("Total Actual Revenue", f"GHS {order_df['Actual Revenue'].sum():,.2f}", icon="fa-line-chart", tooltip="Revenue generated from the fulfilled quantities.")
display_kpi_card("Revenue Loss", f"GHS {revenue_loss:,.2f}", icon="fa-exclamation-circle", tooltip="Revenue lost due to unfulfilled or partially fulfilled orders.")

# Display percentage-based KPIs using circular progress indicators with labels
st.write("### Fulfillment KPIs")
display_progress_circle("Order Fill Rate", quantity_fulfill_rate)
display_progress_circle("Perfect Order Rate", perfect_order_rate)
display_progress_circle("Fully Fulfilled", percent_fully_fulfilled)
display_progress_circle("Partially Fulfilled", percent_partially_fulfilled)
display_progress_circle("Not Fulfilled", percent_not_fulfilled)

# Pie chart for fully, partially, and not fulfilled
fulfillment_data = pd.DataFrame({
    "Fulfillment Type": ["Fully Fulfilled", "Partially Fulfilled", "Not Fulfilled"],
    "Percentage": [percent_fully_fulfilled, percent_partially_fulfilled, percent_not_fulfilled]
})

st.write("### Fulfillment Distribution")
fulfillment_pie = px.pie(
    fulfillment_data, 
    values="Percentage", 
    names="Fulfillment Type", 
    title="Fulfillment Distribution"
)
st.plotly_chart(fulfillment_pie)

# Fill Rate by Customer
st.write("### Fill Rate by Customer")
customer_fill_rate = order_df.groupby('Customer', group_keys=False).apply(
    lambda x: (x['Quantity Fulfilled'].sum() / x['Quantity Requested'].sum()) * 100
).reset_index(drop=True)
st.write(customer_fill_rate)

# Top 10 Under-Fulfilled Items
st.write("### Top 10 Under-Fulfilled Items")
under_fulfilled_items = order_df.assign(
    Difference=lambda df: df['Quantity Requested'] - df['Quantity Fulfilled']
).sort_values('Difference', ascending=False).head(10)
st.write(under_fulfilled_items[['Item', 'Quantity Requested', 'Quantity Fulfilled', 'Difference']])

# Allow user to download the order data as CSV
st.write("### Export Report")
st.download_button(label="Download CSV", data=order_df.to_csv(index=False), 
                    file_name=f"order_fulfillment_report_{customer_name}_{order_date}.csv", mime="text/csv")

