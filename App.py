import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go 

# Page Configuration
st.set_page_config(
    page_title="The 80-Minute Journey",
    page_icon="Gold Medal 🥇",
    layout="wide",  # Uses full width of browser
    initial_sidebar_state="expanded"  # Sidebar open by default
)

# Color Pallete
COLORS = {
    'bg_dark': '#0F172A',       # Dark background
    'bg_card': '#1E293B',       # Card background
    'bg_elevated': '#334155',   # Elevated elements
    'border': '#475569',        # Borders
    'text_bright': '#F8FAFC',   # Bright text
    'text_secondary': '#94A3B8', # Secondary text
    'text_muted': '#64748B',    # Muted text
    'emerald': '#10B981',       # Green accent
    'violet': '#8B5CF6',        # Purple accent
    'rose': '#F43F5E',          # Pink/red accent
    'amber': '#FBBF24',         # Gold accent
}

# Custom CSS Styling
st.markdown(f"""
<style>
    /* Dark gradient background for the whole app */
    .stApp {{
        background: linear-gradient(180deg, {COLORS['bg_dark']} 0%, {COLORS['bg_card']} 100%);
    }}
    
    /* Hide Streamlit's default branding */
    #MainMenu, footer, header {{visibility: hidden;}}
    .stDeployButton {{display: none;}}
    
    /* Style the sidebar */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {COLORS['bg_card']} 0%, {COLORS['bg_dark']} 100%) !important;
        border-right: 1px solid {COLORS['border']};
    }}
    
    /* Style the sidebar toggle arrow (green pill shape) */
    [data-testid="collapsedControl"] {{
        background: linear-gradient(135deg, {COLORS['emerald']} 0%, #059669 100%) !important;
        border-radius: 0 10px 10px 0 !important;
    }}
    
    /* Make headings bright white */
    h1, h2, h3 {{ color: {COLORS['text_bright']} !important; }}
    
    /* Make body text a readable gray */
    p, span, label, li {{ color: {COLORS['text_secondary']} !important; }}
    
    /* Style for metric/stat cards */
    .stat-card {{
        background: linear-gradient(135deg, {COLORS['bg_card']} 0%, {COLORS['bg_elevated']} 100%);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid {COLORS['border']};
        text-align: center;
        transition: transform 0.2s, box-shadow 0.2s;
    }}
    
    .stat-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }}
    
    /* Style for content section cards */
    .section-card {{
        background: {COLORS['bg_card']};
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid {COLORS['border']};
        margin-bottom: 1.5rem;
    }}
    
    /* Custom styled table */
    .styled-table {{
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        border-radius: 12px;
        overflow: hidden;
    }}
    
    .styled-table thead tr {{
        background: linear-gradient(135deg, {COLORS['emerald']} 0%, #059669 100%);
    }}
    
    .styled-table th {{
        padding: 1rem;
        text-align: left;
        font-weight: 600;
        color: white !important;
    }}
    
    .styled-table td {{
        padding: 0.875rem 1rem;
        border-bottom: 1px solid {COLORS['border']};
        color: {COLORS['text_secondary']} !important;
    }}
    
    .styled-table tbody tr {{
        background: {COLORS['bg_card']};
        transition: background 0.2s;
    }}
    
    .styled-table tbody tr:hover {{
        background: {COLORS['bg_elevated']};
    }}
    
    /* Highlight the last row (PB) in gold */
    .styled-table tbody tr:last-child {{
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.15) 0%, rgba(251, 191, 36, 0.05) 100%);
    }}
    
    .styled-table tbody tr:last-child td {{
        color: {COLORS['amber']} !important;
        font-weight: 600;
    }}
    
    /* Gradient dividers */
    hr {{
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, {COLORS['border']}, transparent);
        margin: 2rem 0;
    }}
    
    /* Mobile responsive adjustments */
    @media (max-width: 768px) {{
        .stat-card {{ padding: 1rem; }}
        .section-card {{ padding: 1rem; }}
        .styled-table th, .styled-table td {{ padding: 0.5rem; font-size: 0.8rem; }}
    }}
</style>
""", unsafe_allow_html=True)

# Load datasets and calculate initial metrics
activities_df = pd.read_csv("activities_dataset.csv")
challenges_df = pd.read_csv("global_challenges.csv")
running_df = activities_df[activities_df["Activity Type"] == "Run"].reset_index(drop=True)
total_runs = len(running_df)
total_distance = running_df["Distance"].sum()


# Title 
st.markdown(f"""
<div style="background: linear-gradient(135deg, {COLORS['bg_card']} 0%, {COLORS['bg_elevated']} 100%);
     border-radius: 20px; padding: 2rem; border: 1px solid {COLORS['border']}; margin-bottom: 1.5rem;">
    <div style="display: flex; align-items: center; gap: 1.25rem; flex-wrap: wrap;">
        <div>
            <h1 style="color: {COLORS['text_bright']}; font-size: 2.5rem; font-weight: 800; margin: 0;">
                The 80-Minute Journey
            </h1>
            <p style="color: {COLORS['text_secondary']}; font-size: 1.1rem; margin: 0.5rem 0 0 0;">
                A Data-Driven Analysis of Marathon Progression (2022 – 2025)
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# Project Overview 
st.markdown(f"""
<div class="section-card">
    <h2 style="color: {COLORS['emerald']}; font-size: 1.4rem; margin: 0 0 1rem 0;">
        Project Overview
    </h2>
    <p style="color: {COLORS['text_secondary']}; font-size: 1rem; line-height: 1.7; margin: 0;">
        This dashboard analyzes <span style="color: {COLORS['text_bright']}; font-weight: 600;">347 running activities over 3.5 years</span>, 
        documenting the progression from a first-time marathoner 
        (<span style="color: {COLORS['rose']}; font-weight: 600;">4:46:07</span> at Royal Victoria Marathon 2022) 
        to a sub-3:30 finisher (<span style="color: {COLORS['emerald']}; font-weight: 600;">3:26:00</span> at Royal Victoria Marathon 2025) 
        — an improvement of <span style="color: {COLORS['amber']}; font-weight: 600;">80 minutes</span> across 6 marathon races.
    </p>
    <br>
    <p style="color: {COLORS['text_secondary']}; font-size: 1rem; line-height: 1.7; margin: 0;">
        The analysis explores how training patterns, physiological adaptations, and race execution evolved to produce 
        consistent performance gains at two recurring races: the <span style="color: {COLORS['violet']}; font-weight: 600;">Royal Victoria Marathon</span> (4 finishes) 
        and <span style="color: {COLORS['emerald']}; font-weight: 600;">BMO Vancouver Marathon</span> (2 finishes).
    </p>
</div>
""", unsafe_allow_html=True)

# Datasets
st.markdown(f"""
<div class="section-card">
<h2 style="color: {COLORS['violet']}; font-size: 1.4rem; margin: 0 0 1rem 0;">
	Datasets
</h2>
<p style="color: {COLORS['text_secondary']}; font-size: 1rem; line-height: 1.7; margin: 0 0 1.25rem 0;">
	The dataset is sourced from a complete Strava activity export containing <span style="color: {COLORS['text_bright']}; font-weight: 600;">449 total activities</span>. 
	For this analysis, we filter exclusively to <span style="color: {COLORS['emerald']}; font-weight: 600;">running activities (347 runs)</span> 
	spanning February 2022 to October 2025.
</p>

<!-- [ADDED] Grid layout for key columns instead of bullet list -->
<div style="background: {COLORS['bg_elevated']}; border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem;">
	<p style="color: {COLORS['text_muted']}; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; margin: 0 0 0.75rem 0; font-weight: 600;">
		Key Columns Extracted
	</p>
	<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.75rem;">
		<div style="display: flex; align-items: center; gap: 0.5rem;">
			<span style="color: {COLORS['emerald']};">●</span>
			<span style="color: {COLORS['text_secondary']}; font-size: 0.9rem;"><strong style="color: {COLORS['text_bright']};">Activity metadata:</strong> ID, Date, Name, Type</span>
		</div>
		<div style="display: flex; align-items: center; gap: 0.5rem;">
			<span style="color: {COLORS['violet']};">●</span>
			<span style="color: {COLORS['text_secondary']}; font-size: 0.9rem;"><strong style="color: {COLORS['text_bright']};">Performance:</strong> Distance, Speed, Pace, Time</span>
		</div>
		<div style="display: flex; align-items: center; gap: 0.5rem;">
			<span style="color: {COLORS['rose']};">●</span>
			<span style="color: {COLORS['text_secondary']}; font-size: 0.9rem;"><strong style="color: {COLORS['text_bright']};">Physiological:</strong> Heart Rate (avg/max)</span>
		</div>
		<div style="display: flex; align-items: center; gap: 0.5rem;">
			<span style="color: {COLORS['amber']};">●</span>
			<span style="color: {COLORS['text_secondary']}; font-size: 0.9rem;"><strong style="color: {COLORS['text_bright']};">Terrain:</strong> Elevation Gain/Loss</span>
		</div>
	</div>
</div>

<!-- [ADDED] Warning note styled as alert box -->
<div style="background: rgba(251, 191, 36, 0.1); border-radius: 10px; padding: 0.875rem; border: 1px solid rgba(251, 191, 36, 0.3);">
	<p style="color: {COLORS['amber']}; font-size: 0.85rem; margin: 0;">
		<strong>Note:</strong> Heart rate data is unavailable for the first 20 runs (Feb–Jun 2022) due to the absence of a heart rate monitor during that period.
	</p>
</div>
</div>
""", unsafe_allow_html=True)