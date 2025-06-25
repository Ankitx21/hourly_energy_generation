# energy_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="Hourly Energy Viewer", layout="wide")
st.title("☀️ Hourly Energy Generation Dashboard")

# Load the data
uploaded_file = st.file_uploader("Upload hourly_energy_summary.csv", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Show table
    st.subheader("📋 Data Table")
    st.dataframe(df)

    # Select a date
    unique_dates = df['Date'].unique()
    selected_date = st.selectbox("Select a Date to Visualize", unique_dates)

    # Filter for selected date
    df_day = df[df['Date'] == selected_date]

    if not df_day.empty:
        st.subheader(f"📊 Energy Plot for {selected_date}")

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
else:
    st.info("Upload your `hourly_energy_summary.csv` to get started.")
