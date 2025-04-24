import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Rx Share Dashboard", layout="wide")
st.title("📊 Rx Share Analysis Dashboard")

# File uploader
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Filter out rows with missing ING or VC2
    df = df[df['ING'].notna() & df['VC2'].notna()]

    # Add a new column to mark if it's our product
    df['IS_OUR_PRODUCT'] = df['VC2'] == 'RNT'

    # Calculate Rx counts
    product_group = df.groupby('ING')['IS_OUR_PRODUCT'].agg([
        ('Our Rx', 'sum'),
        ('Total Rx', 'count')
    ]).reset_index()

    product_group['Rx Share (%)'] = (product_group['Our Rx'] / product_group['Total Rx']) * 100

    st.subheader("📈 Rx Share by Product")
    st.dataframe(product_group.sort_values(by='Rx Share (%)', ascending=False), use_container_width=True)

    # Bar chart of Rx Share
    st.bar_chart(product_group.set_index('ING')['Rx Share (%)'])

    # Filters
    st.sidebar.header("🔎 Filters")
    month_filter = st.sidebar.multiselect("Select Month", df['MONTH'].unique())
    pso_filter = st.sidebar.multiselect("Select PSO", df['PSO NAMES'].unique())
    
    filtered_df = df.copy()
    if month_filter:
        filtered_df = filtered_df[filtered_df['MONTH'].isin(month_filter)]
    if pso_filter:
        filtered_df = filtered_df[filtered_df['PSO NAMES'].isin(pso_filter)]

    # List doctors with RNT prescriptions only
    potential_doctors = filtered_df[filtered_df['VC2'] == 'RNT']
    doctor_list = potential_doctors[['PHY_NM', 'CH_ADD', 'PSO NAMES', 'MONTH']].drop_duplicates()

    st.subheader("👨‍⚕️ Potential Doctors Prescribing Our Product")
    st.dataframe(doctor_list, use_container_width=True)

else:
    st.info("Please upload an Excel file to begin analysis.")
