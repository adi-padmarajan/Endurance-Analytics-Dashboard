import streamlit as st
import pandas as pd
import numpy as np

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

with st.expander("Show activities_dataset.csv"):
	st.dataframe(activities_df)

with st.expander("Show global_challenges.csv"):
	st.dataframe(challenges_df)

