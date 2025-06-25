# energy_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="Hourly Energy Viewer", layout="wide")
st.title("☀️ Hourly Energy Generation Dashboard")

# --- Load the CSV directly from file ---
csv_path = "hourly_energy_summary.csv"  # Make sure this file is in the same directory
try:
    df = pd.read_csv(csv_path)
except FileNotFoundError:
    st.error("❌ The file 'hourly_energy_summary.csv' was not found. Please add it to the app folder.")
    st.stop()

# Show the table
st.subheader("📋 Hourly Energy Data")
st.dataframe(df)

# Dropdown to select date
unique_dates = df['Date'].unique()
selected_date = st.selectbox("Select a Date to Visualize", unique_dates)

# Filter for the selected date
df_day = df[df['Date'] == selected_date]

if not df_day.empty:
    st.subheader(f"📊 Hourly Energy Plot for {selected_date}")

    fig, ax = plt.subplots(figsize=(12, 6))
    x = df_day['Hour']
    width = 0.25

    ax.bar(x - width, df_day['Energy_Actual'], width=width, label='Actual Energy', color='black')
    ax.bar(x, df_day['Energy_Predicted'], width=width, label='Predicted Energy', color='orange')
    ax.bar(x + width, df_day['Energy_LowerBound'], width=width, label='Lower Bound', color='blue')

    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Energy (Wh/m²)")
    ax.set_title(f"Hourly Energy on {selected_date}")
    ax.set_xticks(x)
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)

    st.pyplot(fig)
else:
    st.warning("No data available for the selected date.")
