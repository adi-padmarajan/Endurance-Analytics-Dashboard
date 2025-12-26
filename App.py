import streamlit as st
import pandas as pd
import numpy as np

# Set page config for dashboard look
st.set_page_config(
    page_title="The 80-Minute Journey",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="auto"
)

# Load datasets
activities_df = pd.read_csv("activities_dataset.csv")
challenges_df = pd.read_csv("global_challenges.csv")

