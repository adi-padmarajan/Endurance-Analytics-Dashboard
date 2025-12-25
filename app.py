# =============================================================================
# THE 80-MINUTE JOURNEY: STREAMLIT DASHBOARD (DARK MODE)
# =============================================================================
# Based on: endurance_analytics.ipynb
# Author: Aditya Padmarajan
# 
# Dark Mode Color Palette:
# - Background: Slate (#0F172A → #1E293B)
# - Primary: Cyan/Teal (#22D3EE → #06B6D4)
# - Accent: Amber (#FBBF24)
# - Text: Light (#F8FAFC → #94A3B8)
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
# DARK MODE CSS
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Dark mode background */
    .stApp {
        background-color: #0F172A;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Headers */
    h1, h2, h3 {
        color: #F8FAFC !important;
    }
    
    /* Paragraphs */
    p, span, label {
        color: #CBD5E1 !important;
    }
    
    /* Dividers */
    hr {
        border-color: #334155 !important;
    }
    
    /* Plotly chart container */
    .stPlotlyChart {
        background-color: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DARK MODE COLOR PALETTE
# -----------------------------------------------------------------------------
COLORS = {
    # Backgrounds
    'bg_dark': '#0F172A',
    'bg_card': '#1E293B',
    'bg_elevated': '#334155',
    
    # Primary gradient (cyan/teal - vibrant on dark)
    'primary_gradient': ['#67E8F9', '#22D3EE', '#06B6D4', '#0891B2', '#0E7490', '#155E75'],
    
    # Accent (amber - warm contrast)
    'accent': '#FBBF24',
    'accent_light': '#FEF3C7',
    'accent_dark': '#F59E0B',
    'accent_bg': 'rgba(251, 191, 36, 0.15)',
    
    # Text
    'text_bright': '#F8FAFC',
    'text_primary': '#E2E8F0',
    'text_secondary': '#94A3B8',
    'text_muted': '#64748B',
    
    # Chart elements
    'line': '#22D3EE',
    'fill': 'rgba(34, 211, 238, 0.15)',
    'grid': 'rgba(148, 163, 184, 0.15)',
    'border': '#475569'
}

# -----------------------------------------------------------------------------
# DATA LOADING
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("activities_dataset.csv")
    df2 = df.query("`Activity Type` == 'Run'").reset_index(drop=True)
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

@st.cache_data
def preprocess_data(df2):
    df2["Activity Date"] = pd.to_datetime(df2["Activity Date"], format="%b %d, %Y, %I:%M:%S %p")
    df2["Year"] = df2["Activity Date"].dt.year
    df2["Month"] = df2["Activity Date"].dt.month
    df2["Week"] = df2["Activity Date"].dt.isocalendar().week
    df2["Day"] = df2["Activity Date"].dt.day_name()
    df2["Pace (min/km)"] = 1000 / (df2["Avg Speed (m/s)"] * 60)
    df2["Pace (min:sec/km)"] = df2["Pace (min/km)"].apply(
        lambda x: f"{int(x)}:{int((x % 1) * 60):02d}"
    )
    df2["Moving Time (H:M:S)"] = df2["Moving Time (s)"].apply(
        lambda x: f"{int(x // 3600)}:{int((x % 3600) // 60):02d}:{int(x % 60):02d}" if pd.notna(x) else None
    )
    
    cols_to_keep = [
        "Activity ID", "Activity Date", "Year", "Month", "Week", "Day",
        "Activity Name", "Activity Type", "Distance (km)", "Pace (min/km)",
        "Pace (min:sec/km)", "Moving Time (s)", "Moving Time (H:M:S)",
        "Avg HR (bpm)", "Max HR (bpm)", "Elevation Gain (m)", "Calories"
    ]
    
    running_df = df2[[c for c in cols_to_keep if c in df2.columns]].reset_index(drop=True)
    marathon_df = running_df[running_df["Distance (km)"] > 40].reset_index(drop=True)
    
    return running_df, marathon_df

@st.cache_data
def get_marathon_data(marathon_df):
    marathon_df = marathon_df.copy()
    marathon_df["Race"] = ["RVM 2022", "BMO 2023", "RVM 2023", "RVM 2024", "BMO 2025", "RVM 2025"]
    marathon_df["Official Time"] = ["4:46:07", "4:25:48", "4:16:58", "3:47:47", "3:37:23", "3:26:00"]
    marathon_df["Official Time (s)"] = [
        4*3600 + 46*60 + 7, 4*3600 + 25*60 + 48, 4*3600 + 16*60 + 58,
        3*3600 + 47*60 + 47, 3*3600 + 37*60 + 23, 3*3600 + 26*60 + 0
    ]
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
st.markdown(f"""
<div style="text-align: center; padding: 2rem 0 2.5rem 0;">
    <h1 style="font-size: 2.8rem; margin-bottom: 0.5rem; color: {COLORS['text_bright']}; font-weight: 700;">
        🏃 The 80-Minute Journey
    </h1>
    <p style="font-size: 1.1rem; color: {COLORS['text_secondary']}; font-style: italic; margin-bottom: 0.5rem;">
        A Data-Driven Analysis of Marathon Progression
    </p>
    <p style="font-size: 0.9rem; color: {COLORS['text_muted']};">
        2022 – 2025 &nbsp;•&nbsp; Aditya Padmarajan &nbsp;•&nbsp; Strava Data
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# =============================================================================
# VISUALIZATION 1: THE 80-MINUTE JOURNEY
# =============================================================================

st.markdown(f"""
<h2 style="margin-bottom: 0.25rem; font-size: 1.5rem; color: {COLORS['text_bright']}; font-weight: 600;">
    The 80-Minute Journey
</h2>
<p style="color: {COLORS['text_secondary']}; font-size: 0.9rem; margin-top: 0.25rem; margin-bottom: 1.5rem;">
    Marathon finish times from first race to personal best
</p>
""", unsafe_allow_html=True)

# Data
races = marathon_df["Race"].tolist()
times = marathon_df["Official Time (min)"].tolist()
labels = marathon_df["Official Time"].tolist()

# Cyan gradient (light → dark as times improve)
marker_colors_1 = COLORS['primary_gradient']

fig1 = go.Figure()

# Soft glow fill
fig1.add_trace(go.Scatter(
    x=races + races[::-1],
    y=[max(times) + 10] * len(races) + times[::-1],
    fill='toself',
    fillcolor=COLORS['fill'],
    line=dict(color='rgba(0,0,0,0)'),
    showlegend=False,
    hoverinfo='skip'
))

# Main line (glowing effect)
fig1.add_trace(go.Scatter(
    x=races, y=times,
    mode='lines',
    line=dict(color=COLORS['line'], width=3),
    showlegend=False,
    hoverinfo='skip'
))

# Gradient markers
fig1.add_trace(go.Scatter(
    x=races, y=times,
    mode='markers',
    marker=dict(
        size=16,
        color=marker_colors_1,
        line=dict(color=COLORS['bg_dark'], width=2)
    ),
    showlegend=False,
    hovertemplate="<b>%{x}</b><br>Finish Time: %{customdata}<extra></extra>",
    customdata=labels
))

# Time labels (alternating positions)
for i, (race, time, label) in enumerate(zip(races, times, labels)):
    yshift = -22 if i % 2 == 0 else 22
    
    fig1.add_annotation(
        x=race, y=time,
        text=f"<b>{label}</b>",
        showarrow=False,
        yshift=yshift,
        font=dict(size=10, color=COLORS['text_bright']),
        bgcolor=COLORS['bg_card'],
        bordercolor=COLORS['border'],
        borderwidth=1,
        borderpad=5
    )

# "80 min faster" badge
fig1.add_annotation(
    x=2.5, y=250,
    text="<b>⚡ 80 min faster</b>",
    showarrow=False,
    font=dict(size=11, color=COLORS['accent']),
    bgcolor=COLORS['accent_bg'],
    bordercolor=COLORS['accent'],
    borderwidth=1,
    borderpad=8
)

# PB badge
fig1.add_annotation(
    x=5, y=times[-1],
    text="<b>🏆 PB</b>",
    showarrow=False,
    yshift=-32,
    font=dict(size=10, color=COLORS['bg_dark']),
    bgcolor=COLORS['accent'],
    borderpad=5
)

# Layout
fig1.update_layout(
    yaxis=dict(
        autorange="reversed",
        title=dict(text="<b>Finish Time</b>", font=dict(size=11, color=COLORS['text_secondary'])),
        tickvals=times,
        ticktext=labels,
        tickfont=dict(size=10, color=COLORS['text_secondary']),
        showgrid=True,
        gridwidth=1,
        gridcolor=COLORS['grid'],
        zeroline=False,
        showline=False
    ),
    xaxis=dict(
        title=dict(text="<b>Race</b>", font=dict(size=11, color=COLORS['text_secondary'])),
        tickfont=dict(size=10, color=COLORS['text_secondary']),
        showgrid=False,
        zeroline=False,
        showline=False
    ),
    height=480,
    plot_bgcolor=COLORS['bg_dark'],
    paper_bgcolor=COLORS['bg_dark'],
    margin=dict(l=90, r=50, t=20, b=60),
    hoverlabel=dict(
        bgcolor=COLORS['bg_card'],
        font_size=12,
        font_family="Arial",
        font_color=COLORS['text_bright'],
        bordercolor=COLORS['border']
    )
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# =============================================================================
# VISUALIZATION 2: PACE EVOLUTION
# =============================================================================

st.markdown(f"""
<h2 style="margin-bottom: 0.25rem; font-size: 1.5rem; color: {COLORS['text_bright']}; font-weight: 600;">
    Pace Evolution
</h2>
<p style="color: {COLORS['text_secondary']}; font-size: 0.9rem; margin-top: 0.25rem; margin-bottom: 1.5rem;">
    Average pace progression across six marathons
</p>
""", unsafe_allow_html=True)

# Data
pace_to_plot = marathon_df["Pace (min/km)"].tolist()
pace_labels = marathon_df["Pace (min:sec/km)"].tolist()

fig2 = go.Figure()

# Soft glow fill
fig2.add_trace(go.Scatter(
    x=races + races[::-1],
    y=[max(pace_to_plot) + 0.3] * len(races) + pace_to_plot[::-1],
    fill='toself',
    fillcolor=COLORS['fill'],
    line=dict(color='rgba(0,0,0,0)'),
    showlegend=False,
    hoverinfo='skip'
))

# Main line
fig2.add_trace(go.Scatter(
    x=races, y=pace_to_plot,
    mode='lines',
    line=dict(color=COLORS['line'], width=3),
    showlegend=False,
    hoverinfo='skip'
))

# Gradient markers
fig2.add_trace(go.Scatter(
    x=races, y=pace_to_plot,
    mode='markers',
    marker=dict(
        size=16,
        color=COLORS['primary_gradient'],
        line=dict(color=COLORS['bg_dark'], width=2)
    ),
    showlegend=False,
    hovertemplate="<b>%{x}</b><br>Pace: %{customdata}/km<extra></extra>",
    customdata=pace_labels
))

# Pace labels (alternating)
for i, (race, pace, label) in enumerate(zip(races, pace_to_plot, pace_labels)):
    yshift = 22 if i % 2 == 0 else -22
    
    fig2.add_annotation(
        x=race, y=pace,
        text=f"<b>{label}/km</b>",
        showarrow=False,
        yshift=yshift,
        font=dict(size=10, color=COLORS['text_bright']),
        bgcolor=COLORS['bg_card'],
        bordercolor=COLORS['border'],
        borderwidth=1,
        borderpad=5
    )

# Pace improvement badge
pace_improvement = pace_to_plot[0] - pace_to_plot[-1]
fig2.add_annotation(
    x=2.5, y=5.5,
    text=f"<b>⚡ {pace_improvement:.1f} min/km faster</b>",
    showarrow=False,
    font=dict(size=11, color=COLORS['accent']),
    bgcolor=COLORS['accent_bg'],
    bordercolor=COLORS['accent'],
    borderwidth=1,
    borderpad=8
)

# PB badge
fig2.add_annotation(
    x=5, y=pace_to_plot[-1],
    text="<b>🏆 PB</b>",
    showarrow=False,
    yshift=32,
    font=dict(size=10, color=COLORS['bg_dark']),
    bgcolor=COLORS['accent'],
    borderpad=5
)

# Corner badge
fig2.add_annotation(
    x=0.98, y=0.08,
    xref="paper", yref="paper",
    text="<b>6:30 → 4:50 /km</b>",
    showarrow=False,
    font=dict(size=10, color=COLORS['line']),
    bgcolor=COLORS['bg_card'],
    bordercolor=COLORS['border'],
    borderwidth=1,
    borderpad=6,
    xanchor='right'
)

# Layout
fig2.update_layout(
    yaxis=dict(
        autorange="reversed",
        title=dict(text="<b>Pace (min/km)</b>", font=dict(size=11, color=COLORS['text_secondary'])),
        tickvals=pace_to_plot,
        ticktext=pace_labels,
        tickfont=dict(size=10, color=COLORS['text_secondary']),
        showgrid=True,
        gridwidth=1,
        gridcolor=COLORS['grid'],
        zeroline=False,
        showline=False
    ),
    xaxis=dict(
        title=dict(text="<b>Race</b>", font=dict(size=11, color=COLORS['text_secondary'])),
        tickfont=dict(size=10, color=COLORS['text_secondary']),
        showgrid=False,
        zeroline=False,
        showline=False
    ),
    height=480,
    plot_bgcolor=COLORS['bg_dark'],
    paper_bgcolor=COLORS['bg_dark'],
    margin=dict(l=90, r=50, t=20, b=60),
    hoverlabel=dict(
        bgcolor=COLORS['bg_card'],
        font_size=12,
        font_family="Arial",
        font_color=COLORS['text_bright'],
        bordercolor=COLORS['border']
    )
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# =============================================================================
# VISUALIZATION 3: BUILDING THE BASE
# =============================================================================

st.markdown(f"""
<h2 style="margin-bottom: 0.25rem; font-size: 1.5rem; color: {COLORS['text_bright']}; font-weight: 600;">
    Building the Base
</h2>
<p style="color: {COLORS['text_secondary']}; font-size: 0.9rem; margin-top: 0.25rem; margin-bottom: 1.5rem;">
    Total running distance per year
</p>
""", unsafe_allow_html=True)

# Data
cumulative_distance_year_df = running_df.groupby("Year")["Distance (km)"].sum().reset_index()
years = cumulative_distance_year_df["Year"].astype(int).tolist()
year_distance = cumulative_distance_year_df["Distance (km)"].tolist()
runs_per_year = running_df.groupby("Year").size().tolist()

# Cyan gradient for bars
bar_colors = ['#67E8F9', '#22D3EE', '#06B6D4', '#0891B2']

fig3 = go.Figure()

# Bar chart
fig3.add_trace(go.Bar(
    x=years,
    y=year_distance,
    marker_color=bar_colors,
    marker_line=dict(color=COLORS['bg_dark'], width=2),
    width=0.55,
    hovertemplate="<b>%{x}</b><br>Distance: %{y:,.0f} km<extra></extra>"
))

# Distance labels on top
for i, (year, dist) in enumerate(zip(years, year_distance)):
    fig3.add_annotation(
        x=year, y=dist + 35,
        text=f"<b>{dist:,.0f} km</b>",
        showarrow=False,
        font=dict(size=12, color=COLORS['text_bright']),
        yanchor='bottom'
    )

# Run count inside bars
for i, (year, dist, runs) in enumerate(zip(years, year_distance, runs_per_year)):
    fig3.add_annotation(
        x=year, y=dist / 2,
        text=f"<b>{runs} runs</b>",
        showarrow=False,
        font=dict(size=10, color=COLORS['bg_dark'])
    )

# Growth badge
growth = year_distance[-1] / year_distance[0]
fig3.add_annotation(
    x=2023.5, y=max(year_distance) * 1.15,
    text=f"<b>📈 {growth:.0f}x volume growth</b>",
    showarrow=False,
    font=dict(size=12, color=COLORS['accent']),
    bgcolor=COLORS['accent_bg'],
    bordercolor=COLORS['accent'],
    borderwidth=1,
    borderpad=8
)

# Total badge
total_km = sum(year_distance)
fig3.add_annotation(
    x=0.98, y=0.96,
    xref="paper", yref="paper",
    text=f"<b>Total: {total_km:,.0f} km</b>",
    showarrow=False,
    font=dict(size=11, color=COLORS['line']),
    bgcolor=COLORS['bg_card'],
    bordercolor=COLORS['border'],
    borderwidth=1,
    borderpad=8,
    xanchor='right', yanchor='top'
)

# Layout
fig3.update_layout(
    yaxis=dict(
        title=dict(text="<b>Distance (km)</b>", font=dict(size=11, color=COLORS['text_secondary'])),
        range=[0, max(year_distance) * 1.30],
        tickfont=dict(size=10, color=COLORS['text_secondary']),
        showgrid=True,
        gridwidth=1,
        gridcolor=COLORS['grid'],
        zeroline=False,
        showline=False
    ),
    xaxis=dict(
        title=dict(text="<b>Year</b>", font=dict(size=11, color=COLORS['text_secondary'])),
        tickmode='array',
        tickvals=years,
        ticktext=[str(y) for y in years],
        tickfont=dict(size=11, color=COLORS['text_secondary']),
        showgrid=False,
        zeroline=False,
        showline=False
    ),
    height=480,
    plot_bgcolor=COLORS['bg_dark'],
    paper_bgcolor=COLORS['bg_dark'],
    margin=dict(l=70, r=50, t=20, b=60),
    hoverlabel=dict(
        bgcolor=COLORS['bg_card'],
        font_size=12,
        font_family="Arial",
        font_color=COLORS['text_bright'],
        bordercolor=COLORS['border']
    ),
    bargap=0.3
)

st.plotly_chart(fig3, use_container_width=True)

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 1.5rem 0 2rem 0;">
    <p style="margin: 0; font-size: 0.85rem; color: {COLORS['text_muted']};">
        Built with Streamlit &nbsp;•&nbsp; Data from Strava
    </p>
    <p style="margin: 0.3rem 0 0 0; font-size: 0.8rem; color: {COLORS['text_muted']};">
        The 80-Minute Journey: A Data-Driven Analysis of Marathon Progression
    </p>
</div>
""", unsafe_allow_html=True)