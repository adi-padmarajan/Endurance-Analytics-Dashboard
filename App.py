import streamlit as st
import pandas as pd

# Import page modules
import home
import marathon_performance
import training_metrics
import heart_rate_analysis
import route_visualization

# Page configuration for a wide layout
st.set_page_config(
    page_title="The Sub-3:30 Protocol",  # Browser tab title
    page_icon="⭐",                       # Browser tab icon
    layout="wide"                         # Use full width of the page
)

colors = ["#00d9ff", "#b957ff", "#1a0d2e", "#0a0420", "#e0f4ff"]

# Load external CSS file
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css("styles.css")


# Sidebar Navigation
with st.sidebar:
    st.title("The Sub-3:30 Protocol")
    st.markdown("<hr>", unsafe_allow_html=True)

    # Navigation Menu
    page = st.radio(
        "Navigation",
        ["Home", "Marathon Performance Metrics", "Training Metrics", "Heart Rate Analysis","Route Visualization"],
        label_visibility="collapsed"
    )

    st.markdown("<hr>", unsafe_allow_html=True)

# Load datasets
activities_df = pd.read_csv("datasets/activities_dataset.csv")
challenges_df = pd.read_csv("datasets/global_challenges.csv")
vo2max_df = pd.read_csv("datasets/VO₂ Max.csv", skiprows=1, names=['Month', 'Activity Type', 'VO2 Max'])

# Prepare Heart Rate Data
# Filter out race distances (marathons > 40km) and ensure HR data exists
df_hr = activities_df[
    (activities_df['Activity Type'] == 'Run') &
    (activities_df['Average Heart Rate'].notna()) &
    (activities_df['Distance'] <= 40)
].copy()

# Parse dates and add Year column
df_hr['Activity Date'] = pd.to_datetime(df_hr['Activity Date'], format="%b %d, %Y, %I:%M:%S %p")
df_hr['Year'] = df_hr['Activity Date'].dt.year

# Calculate pace
df_hr['Pace (min/km)'] = 1000 / (df_hr['Average Speed'] * 60)
df_hr = df_hr.rename(columns={'Average Heart Rate': 'Avg HR (bpm)'})

# ===== PAGE ROUTING =====
if page == "Home":
    home.render(colors)

elif page == "Marathon Performance Metrics":
    marathon_performance.render(colors, vo2max_df)

elif page == "Training Metrics":
    training_metrics.render(colors, activities_df)

elif page == "Heart Rate Analysis":
    heart_rate_analysis.render(colors, df_hr)

elif page == "Route Visualization":
    route_visualization.render(colors)


# Footer (displayed on all pages)
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    f"""
    <div style='text-align: center; color: {colors[4]}; font-size: 0.85rem; text-shadow: 0 0 8px {colors[4]}30;'>
        Built by <strong style='color: {colors[0]};'>Aditya Padmarajan</strong> • Data from Strava • 2022-2025
    </div>
    """,
    unsafe_allow_html=True
)
