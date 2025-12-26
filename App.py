import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.title("The 80 Minutes Journey")
st.subheader("A Data-Driven Analysis of Marathon Progression (2022 – 2025)")

# Load datasets
activities_df = pd.read_csv("activities_dataset.csv")
challenges_df = pd.read_csv("global_challenges.csv")

st.markdown(
"""
### Project Overview
This dashboard analyzes **347 running activities over 3.5 years**, documenting the progression from a first-time marathoner (4:46:07 at Royal Victoria Marathon 2022) to a sub-3:30 finisher (3:26:00 at Royal Victoria Marathon 2025) — an improvement of **80 minutes** across 6 marathon races.
The analysis explores how training patterns, physiological adaptations, and race execution evolved to produce consistent performance gains at two recurring races: the **Royal Victoria Marathon** (4 finishes) and **BMO Vancouver Marathon** (2 finishes).
"""
)

st.markdown(
""" ### Datasets 
The dataset is sourced from a complete Strava activity export containing 449 total activities. For this analysis, we filter exclusively to **running activities (347 runs)** spanning February 2022 to October 2025.

**Key columns extracted:**
- **Activity metadata:** ID, Date, Name, Type
- **Performance metrics:** Distance, Speed, Pace, Moving Time
- **Physiological data:** Heart Rate (average/max)
- **Terrain data:** Elevation Gain/Loss, High/Low points
- **Effort indicators:** Calories, Relative Effort

*Note: Heart rate data is unavailable for the first 20 runs (Feb–Jun 2022) due to the absence of a heart rate monitor during that period.*
""")

st.markdown(
"""

### Marathon Race Summary (Official Times)

| Race | Date | Finish Time | Pace |
|------|------|-------------|------|
| Royal Victoria Marathon 2022 | Oct 9, 2022 | 4:46:07 | 6:30/km |
| BMO Vancouver Marathon 2023 | May 7, 2023 | 4:25:48 | 6:13/km |
| Royal Victoria Marathon 2023 | Oct 8, 2023 | 4:16:58 | 6:04/km |
| Royal Victoria Marathon 2024 | Oct 13, 2024 | 3:47:47 | 5:22/km |
| BMO Vancouver Marathon 2025 | May 4, 2025 | 3:37:23 | 5:07/km |
| Royal Victoria Marathon 2025 | Oct 12, 2025 | 3:26:00 | 4:50/km |

"""
)

st.markdown("### Marathon Progression Timeline")
st.markdown("*Finish time improvements across all 6 marathon races*")

# Define the data for the chart
races = ["RVM 2022", "BMO 2023", "RVM 2023", "RVM 2024", "BMO 2025", "RVM 2025"]
times_minutes = [286.12, 265.80, 256.97, 227.78, 217.38, 206.00]  # Finish times in minutes
times_labels = ["4:46:07", "4:25:48", "4:16:58", "3:47:47", "3:37:23", "3:26:00"]  # H:M:S format labels

# Create Plotly figure (needed for custom y-axis formatting and inversion)
fig = go.Figure()

# Add line trace with markers
fig.add_trace(go.Scatter(
    x=races,
    y=times_minutes,
    mode='lines+markers',  # Show both line and data points
    marker=dict(size=10, color='#1f77b4'),  # Blue markers
    line=dict(width=2, color='#1f77b4'),  # Blue line
    hovertemplate="<b>%{x}</b><br>Time: %{customdata}<extra></extra>",  # Custom hover text
    customdata=times_labels  # Pass H:M:S labels for hover
))

# ADDED: Update layout with inverted y-axis and H:M:S tick labels
fig.update_layout(
    xaxis=dict(
        title=dict(text="Race", font=dict(size=14)),  # X-axis label
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title=dict(text="Finish Time (H:M:S)", font=dict(size=14)),  # Y-axis label
        tickvals=times_minutes,  # Set tick positions at each data point
        ticktext=times_labels,   # Display H:M:S labels instead of minutes
        autorange="reversed",    # INVERTED: Lower times (faster) appear at top
        tickfont=dict(size=12)
    ),
    height=450,
    margin=dict(l=80, r=40, t=40, b=60),
    hovermode='x unified'
)

# Display the Plotly chart in Streamlit
st.plotly_chart(fig, use_container_width=True)


