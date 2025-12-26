import streamlit as st
import pandas as pd
import numpy as np

st.title("The 80 Minutes Journey")
st.write("A Data-Driven Analysis of Marathon Progression (Feb 2022 – Oct 2025)")

# Load datasets
activities_df = pd.read_csv("activities_dataset.csv")
challenges_df = pd.read_csv("global_challenges.csv")

# Display both CSV files in Streamlit
with st.expander("Show activities_dataset.csv"):
	st.dataframe(activities_df)

with st.expander("Show global_challenges.csv"):
	st.dataframe(challenges_df)
