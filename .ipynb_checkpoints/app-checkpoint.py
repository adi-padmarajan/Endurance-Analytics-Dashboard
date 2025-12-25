
# =============================================================================
# THE 80-MINUTE JOURNEY: STREAMLIT DASHBOARD
# =============================================================================
# Based on: endurance_analytics.ipynb
# Author: Aditya Padmarajan
# 
# This app contains ONLY the 3 visualizations from the notebook:
# 1. Marathon Progression Timeline
# 2. Pace Evolution Curve
# 3. Building the Base (Yearly Totals)
# =============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="The 80-Minute Journey",
    page_icon="🏃",
    layout="wide"
)

# -----------------------------------------------------------------------------
# DATA LOADING (Same as notebook Cell 4)
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("activities_dataset.csv")
    
    # Filter to running activities FIRST (same as notebook)
    df2 = df.query("`Activity Type` == 'Run'").reset_index(drop=True)
    
    # Rename columns (same as notebook)
    df2 = df2.rename(columns={
        "Distance": "Distance (km)",
        "Average Speed": "Avg Speed (m/s)",
        "Max Speed": "Max Speed (m/s)",
        "Moving Time": "Moving Time (s)",
        "Elapsed Time": "Elapsed Time (s)",
        "Average Heart Rate": "Avg HR (bpm)",
        "Max Heart Rate": "Max HR (bpm)",
        "Elevation Gain": "Elevation Gain (m)",
        "Elevation Loss": "Elevation Loss (m)",
        "Elevation High": "Elevation High (m)",
        "Elevation Low": "Elevation Low (m)"
    })
    
    return df2

# -----------------------------------------------------------------------------
# PRE-PROCESSING (Same as notebook Cell 6)
# -----------------------------------------------------------------------------
@st.cache_data
def preprocess_data(df2):
    # Parse dates
    df2["Activity Date"] = pd.to_datetime(df2["Activity Date"], format="%b %d, %Y, %I:%M:%S %p")
    
    # Time-Based Columns for grouping
    df2["Year"] = df2["Activity Date"].dt.year
    df2["Month"] = df2["Activity Date"].dt.month
    df2["Week"] = df2["Activity Date"].dt.isocalendar().week
    df2["Day"] = df2["Activity Date"].dt.day_name()
    
    # Calculate pace
    df2["Pace (min/km)"] = 1000 / (df2["Avg Speed (m/s)"] * 60)
    
    # Formatted pace columns
    df2["Pace (min:sec/km)"] = df2["Pace (min/km)"].apply(
        lambda x: f"{int(x)}:{int((x % 1) * 60):02d}"
    )
    
    # Formatted Moving Time (seconds -> H:MM:SS)
    df2["Moving Time (H:M:S)"] = df2["Moving Time (s)"].apply(
        lambda x: f"{int(x // 3600)}:{int((x % 3600) // 60):02d}:{int(x % 60):02d}" if pd.notna(x) else None
    )
    
    # Select columns
    cols_to_keep = [
        "Activity ID", "Activity Date", "Year", "Month", "Week", "Day",
        "Activity Name", "Activity Type", "Distance (km)", "Pace (min/km)",
        "Pace (min:sec/km)", "Moving Time (s)", "Moving Time (H:M:S)",
        "Avg HR (bpm)", "Max HR (bpm)", "Elevation Gain (m)", "Calories"
    ]
    
    running_df = df2[[c for c in cols_to_keep if c in df2.columns]].reset_index(drop=True)
    
    # Extract Marathons
    marathon_df = running_df[running_df["Distance (km)"] > 40].reset_index(drop=True)
    
    return running_df, marathon_df

# -----------------------------------------------------------------------------
# MARATHON DATA (Same as notebook Cell 8)
# -----------------------------------------------------------------------------
@st.cache_data
def get_marathon_data(marathon_df):
    marathon_df = marathon_df.copy()
    
    # Add race names
    marathon_df["Race"] = ["RVM 2022", "BMO 2023", "RVM 2023", "RVM 2024", "BMO 2025", "RVM 2025"]
    
    # Official times (H:MM:SS format for display)
    marathon_df["Official Time"] = [
        "4:46:07", "4:25:48", "4:16:58", "3:47:47", "3:37:23", "3:26:00"
    ]
    
    # Official times in seconds (for calculations/plotting)
    marathon_df["Official Time (s)"] = [
        4*3600 + 46*60 + 7,
        4*3600 + 25*60 + 48,
        4*3600 + 16*60 + 58,
        3*3600 + 47*60 + 47,
        3*3600 + 37*60 + 23,
        3*3600 + 26*60 + 0
    ]
    
    # Official times in minutes (for plotting)
    marathon_df["Official Time (min)"] = marathon_df["Official Time (s)"] / 60
    
    return marathon_df

# -----------------------------------------------------------------------------
# LOAD DATA
# -----------------------------------------------------------------------------
df2 = load_data()
running_df, marathon_df_raw = preprocess_data(df2)
marathon_df = get_marathon_data(marathon_df_raw)

# -----------------------------------------------------------------------------
# HEADER
# -----------------------------------------------------------------------------
st.title("🏃 The 80-Minute Journey")
st.markdown("*A Data-Driven Analysis of Marathon Progression (2022–2025)*")
st.markdown("**Author:** Aditya Padmarajan | **Dataset:** Strava activity export")

st.markdown("---")

# -----------------------------------------------------------------------------
# VISUALIZATION 1: Marathon Progression Timeline (from notebook Cell 8)
# -----------------------------------------------------------------------------
st.header("The 80-Minute Journey")
st.markdown("*Marathon progression from first race to personal best (2022–2025)*")

# Data
races = marathon_df["Race"].tolist()
times = marathon_df["Official Time (min)"].tolist()
labels = marathon_df["Official Time"].tolist()

# Colors (red → green gradient like notebook)
colors = ['#d32f2f', '#f57c00', '#fbc02d', '#7cb342', '#43a047', '#2e7d32']

fig1 = go.Figure()

# Green fill under the line
fig1.add_trace(go.Scatter(
    x=races, y=times,
    fill='tozeroy',
    fillcolor='rgba(46, 125, 50, 0.15)',
    line=dict(color='#2E7D32', width=3),
    mode='lines',
    showlegend=False
))

# Markers with gradient colors
fig1.add_trace(go.Scatter(
    x=races, y=times,
    mode='markers+text',
    marker=dict(size=20, color=colors, line=dict(color='white', width=2)),
    text=labels,
    textposition="top center",
    textfont=dict(size=11, color='#333'),
    showlegend=False,
    hovertemplate="<b>%{x}</b><br>Time: %{text}<extra></extra>"
))

# Layout
fig1.update_layout(
    yaxis=dict(
        autorange="reversed",
        title="Finish Time (H:M:S)",
        tickvals=times,
        ticktext=labels,
        tickfont=dict(size=11, color='#333')
    ),
    xaxis=dict(title="Race (42.2 km)", tickfont=dict(size=11, color='#333')),
    height=500,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)

# Add gridlines
fig1.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')

# Add annotation for "80 min faster"
fig1.add_annotation(
    x=2.5, y=250,
    text="<b>80 min faster</b>",
    showarrow=False,
    font=dict(size=12, color="#1976D2"),
    bgcolor="#E3F2FD",
    bordercolor="#1976D2",
    borderwidth=1.5,
    borderpad=6
)

# Add PB annotation
fig1.add_annotation(
    x=5.15, y=times[-1],
    text="<b>PB</b>",
    showarrow=False,
    font=dict(size=12, color="#FFD700")
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# -----------------------------------------------------------------------------
# VISUALIZATION 2: Pace Evolution Curve (from notebook Cell 10)
# -----------------------------------------------------------------------------
st.header("Pace Evolution Curve")
st.markdown("*Marathon pace progression across six marathons (2022–2025)*")

# Data
pace_to_plot = marathon_df["Pace (min/km)"].tolist()
pace_labels = marathon_df["Pace (min:sec/km)"].tolist()

# Blue gradient colors (like notebook)
blue_colors = ['#bbdefb', '#90caf9', '#64b5f6', '#42a5f5', '#2196f3', '#1565c0']

fig2 = go.Figure()

# Blue fill under the curve
fig2.add_trace(go.Scatter(
    x=races, y=pace_to_plot,
    fill='tozeroy',
    fillcolor='rgba(21, 101, 192, 0.15)',
    line=dict(color='#1565C0', width=3),
    mode='lines',
    showlegend=False
))

# Markers with blue gradient
fig2.add_trace(go.Scatter(
    x=races, y=pace_to_plot,
    mode='markers+text',
    marker=dict(size=20, color=blue_colors, line=dict(color='white', width=2.5)),
    text=[f"{p}/km" for p in pace_labels],
    textposition="top center",
    textfont=dict(size=11, color='#333'),
    showlegend=False,
    hovertemplate="<b>%{x}</b><br>Pace: %{text}<extra></extra>"
))

# Layout
fig2.update_layout(
    yaxis=dict(
        autorange="reversed",
        title="Marathon Pace (min:sec/km)",
        tickvals=pace_to_plot,
        ticktext=pace_labels,
        tickfont=dict(size=11, color='#333')
    ),
    xaxis=dict(title="Race (42.2 km)", tickfont=dict(size=11, color='#333')),
    height=500,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)

# Add gridlines
fig2.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')

# Pace improvement annotation
pace_improvement = pace_to_plot[0] - pace_to_plot[-1]
fig2.add_annotation(
    x=2.5, y=5.7,
    text=f"<b>{pace_improvement:.1f} min/km faster</b>",
    showarrow=False,
    font=dict(size=12, color="#7B1FA2"),
    bgcolor="#F3E5F5",
    bordercolor="#7B1FA2",
    borderwidth=1.5,
    borderpad=6
)

# Start to end comparison
fig2.add_annotation(
    x=5, y=max(pace_to_plot) - 0.2,
    text="<b>6:30/km → 4:50/km</b>",
    showarrow=False,
    font=dict(size=11, color="#1565C0"),
    bgcolor="#E3F2FD",
    bordercolor="#1565C0",
    borderwidth=1.5,
    borderpad=4
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# -----------------------------------------------------------------------------
# VISUALIZATION 3: Building the Base (from notebook Cell 12)
# -----------------------------------------------------------------------------
st.header("Building the Base")
st.markdown("*Total running distance per year*")

# Data (same as notebook)
cumulative_distance_year_df = running_df.groupby("Year")["Distance (km)"].sum().reset_index()
years = cumulative_distance_year_df["Year"].astype(int).tolist()
year_distance = cumulative_distance_year_df["Distance (km)"].tolist()
runs_per_year = running_df.groupby("Year").size().tolist()

# Green gradient colors (like notebook)
green_colors = ['#a5d6a7', '#66bb6a', '#43a047', '#2e7d32']

fig3 = go.Figure()

# Bar chart
fig3.add_trace(go.Bar(
    x=years,
    y=year_distance,
    marker_color=green_colors,
    marker_line=dict(color='white', width=2.5),
    width=0.65,
    text=[f"{d:,.0f} Km" for d in year_distance],
    textposition='outside',
    textfont=dict(size=14, color='#333'),
    hovertemplate="<b>%{x}</b><br>Distance: %{y:,.0f} km<extra></extra>"
))

# Add run count as annotation inside bars
for i, (year, dist, runs) in enumerate(zip(years, year_distance, runs_per_year)):
    fig3.add_annotation(
        x=year, y=dist/2,
        text=f"<b>{runs} runs</b>",
        showarrow=False,
        font=dict(size=12, color='white')
    )

# Layout
fig3.update_layout(
    yaxis=dict(
        title="Cumulative Distance (Km)",
        range=[0, max(year_distance) * 1.35],
        tickfont=dict(size=11, color='#333')
    ),
    xaxis=dict(
        title="Year",
        tickmode='array',
        tickvals=years,
        ticktext=[str(y) for y in years],
        tickfont=dict(size=13, color='#333')
    ),
    height=500,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)

# Add gridlines
fig3.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')

# Growth annotation
growth = year_distance[-1] / year_distance[0]
fig3.add_annotation(
    x=2023.5,
    y=(year_distance[0] + 250 + year_distance[-1] + 250) / 2 + 50,
    text=f"<b>{growth:.0f}x growth</b>",
    showarrow=False,
    font=dict(size=13, color="#2E7D32"),
    bgcolor="#E8F5E9",
    bordercolor="#2E7D32",
    borderwidth=1.5,
    borderpad=6
)

# Total km annotation
total_km = sum(year_distance)
fig3.add_annotation(
    x=0.97, y=0.95,
    xref="paper", yref="paper",
    text=f"<b>Total: {total_km:,.0f} km</b>",
    showarrow=False,
    font=dict(size=14, color="#2E7D32"),
    bgcolor="#E8F5E9",
    bordercolor="#2E7D32",
    borderwidth=2,
    borderpad=8
)

st.plotly_chart(fig3, use_container_width=True)

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Built with Streamlit • Data from Strava • The 80-Minute Journey"
    "</div>",
    unsafe_allow_html=True
)