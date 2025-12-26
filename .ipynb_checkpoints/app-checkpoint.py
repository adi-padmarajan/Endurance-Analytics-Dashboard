# =============================================================================
# THE 80-MINUTE JOURNEY: STREAMLIT DASHBOARD
# =============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="The 80-Minute Journey",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# CSS STYLING
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Dark background */
    .stApp {
        background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E293B 0%, #0F172A 100%) !important;
        border-right: 1px solid #334155;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 0;
    }
    
    /* Text colors */
    h1, h2, h3 { color: #F8FAFC !important; }
    p, span, label { color: #CBD5E1 !important; }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        color: #22D3EE !important;
        font-size: 1.75rem !important;
        font-weight: 700 !important;
    }
    [data-testid="stMetricLabel"] { color: #94A3B8 !important; }
    [data-testid="stMetricDelta"] { color: #FBBF24 !important; }
    
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        border: 1px solid #475569;
        border-radius: 16px;
        padding: 1rem;
    }
    
    /* Dividers */
    hr { border-color: #334155 !important; }
    
    /* Radio buttons in sidebar */
    [data-testid="stSidebar"] .stRadio > div > label {
        background: transparent;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin: 2px 0;
        transition: all 0.2s;
    }
    [data-testid="stSidebar"] .stRadio > div > label:hover {
        background: rgba(34, 211, 238, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# COLORS
# -----------------------------------------------------------------------------
COLORS = {
    'bg_dark': '#0F172A',
    'bg_card': '#1E293B',
    'bg_elevated': '#334155',
    'primary_gradient': ['#67E8F9', '#22D3EE', '#06B6D4', '#0891B2', '#0E7490', '#155E75'],
    'accent': '#FBBF24',
    'accent_bg': 'rgba(251, 191, 36, 0.15)',
    'text_bright': '#F8FAFC',
    'text_secondary': '#94A3B8',
    'text_muted': '#64748B',
    'line': '#22D3EE',
    'fill': 'rgba(34, 211, 238, 0.12)',
    'grid': 'rgba(148, 163, 184, 0.12)',
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
        "Moving Time": "Moving Time (s)",
    })
    return df2

@st.cache_data
def preprocess_data(df2):
    df2["Activity Date"] = pd.to_datetime(df2["Activity Date"], format="%b %d, %Y, %I:%M:%S %p")
    df2["Year"] = df2["Activity Date"].dt.year
    df2["Pace (min/km)"] = 1000 / (df2["Avg Speed (m/s)"] * 60)
    df2["Pace (min:sec/km)"] = df2["Pace (min/km)"].apply(lambda x: f"{int(x)}:{int((x % 1) * 60):02d}")
    
    cols = ["Activity Date", "Year", "Distance (km)", "Pace (min/km)", "Pace (min:sec/km)", "Moving Time (s)"]
    running_df = df2[[c for c in cols if c in df2.columns]].reset_index(drop=True)
    marathon_df = running_df[running_df["Distance (km)"] > 40].reset_index(drop=True)
    return running_df, marathon_df

@st.cache_data
def get_marathon_data(marathon_df):
    marathon_df = marathon_df.copy()
    marathon_df["Race"] = ["RVM 2022", "BMO 2023", "RVM 2023", "RVM 2024", "BMO 2025", "RVM 2025"]
    marathon_df["Official Time"] = ["4:46:07", "4:25:48", "4:16:58", "3:47:47", "3:37:23", "3:26:00"]
    marathon_df["Official Time (s)"] = [17167, 15948, 15418, 13667, 13043, 12360]
    marathon_df["Official Time (min)"] = marathon_df["Official Time (s)"] / 60
    return marathon_df

# Load data
df2 = load_data()
running_df, marathon_df_raw = preprocess_data(df2)
marathon_df = get_marathon_data(marathon_df_raw)

# Metrics
total_distance = running_df["Distance (km)"].sum()
total_runs = len(running_df)
total_marathons = len(marathon_df)

# -----------------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------------
with st.sidebar:
    # Header
    st.markdown(f"""
    <div style="text-align: center; padding: 1.5rem 0; border-bottom: 1px solid {COLORS['border']}; margin-bottom: 1rem;">
        <div style="font-size: 3.5rem; margin-bottom: 0.5rem;">🏃</div>
        <h2 style="color: {COLORS['text_bright']}; font-size: 1.2rem; margin: 0; font-weight: 700;">
            The 80-Minute Journey
        </h2>
        <p style="color: {COLORS['text_muted']}; font-size: 0.75rem; margin-top: 0.5rem;">
            Marathon Analytics Dashboard
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation label
    st.markdown(f"""
    <p style="color: {COLORS['text_muted']}; font-size: 0.7rem; text-transform: uppercase; 
       letter-spacing: 0.1em; margin-bottom: 0.5rem; font-weight: 600;">
        📍 Navigation
    </p>
    """, unsafe_allow_html=True)
    
    # Navigation
    page = st.radio(
        "Navigation",
        ["🏠 Overview", "🏃 Race Times", "⚡ Pace Analysis", "📈 Training Volume"],
        label_visibility="collapsed"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quick Stats
    st.markdown(f"""
    <div style="background: {COLORS['bg_elevated']}; border-radius: 12px; padding: 1rem; 
         border: 1px solid {COLORS['border']}; margin-top: 1rem;">
        <p style="color: {COLORS['text_muted']}; font-size: 0.7rem; text-transform: uppercase; 
           letter-spacing: 0.1em; margin-bottom: 0.75rem; font-weight: 600;">
            📊 Quick Stats
        </p>
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="color: {COLORS['text_secondary']}; font-size: 0.85rem;">Distance</span>
            <span style="color: {COLORS['line']}; font-weight: 700;">{total_distance:,.0f} km</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="color: {COLORS['text_secondary']}; font-size: 0.85rem;">Runs</span>
            <span style="color: {COLORS['line']}; font-weight: 700;">{total_runs}</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="color: {COLORS['text_secondary']}; font-size: 0.85rem;">Marathons</span>
            <span style="color: {COLORS['accent']}; font-weight: 700;">{total_marathons}</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <span style="color: {COLORS['text_secondary']}; font-size: 0.85rem;">Best Time</span>
            <span style="color: {COLORS['accent']}; font-weight: 700;">3:26:00</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown(f"""
    <div style="position: fixed; bottom: 0; left: 0; width: inherit; padding: 1rem; 
         border-top: 1px solid {COLORS['border']}; background: {COLORS['bg_dark']}; text-align: center;">
        <p style="color: {COLORS['text_muted']}; font-size: 0.7rem; margin: 0;">
            Built by <span style="color: {COLORS['line']};">Aditya Padmarajan</span>
        </p>
        <p style="color: {COLORS['text_muted']}; font-size: 0.65rem; margin-top: 0.25rem;">
            Data from Strava
        </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MAIN HEADER
# -----------------------------------------------------------------------------
st.markdown(f"""
<div style="background: linear-gradient(135deg, {COLORS['bg_card']} 0%, {COLORS['bg_elevated']} 50%, {COLORS['bg_card']} 100%);
     border-radius: 20px; padding: 1.5rem 2rem; margin-bottom: 1.5rem; border: 1px solid {COLORS['border']};">
    <div style="display: flex; align-items: center; gap: 1rem;">
        <span style="font-size: 2.5rem;">🏃</span>
        <div>
            <h1 style="color: {COLORS['text_bright']}; font-size: 1.8rem; font-weight: 700; margin: 0;">
                The 80-Minute Journey
            </h1>
            <p style="color: {COLORS['text_secondary']}; font-size: 0.95rem; margin: 0.25rem 0 0 0;">
                A Data-Driven Analysis of Marathon Progression
            </p>
        </div>
    </div>
    <div style="display: flex; gap: 2rem; margin-top: 1rem; flex-wrap: wrap;">
        <span style="color: {COLORS['text_muted']}; font-size: 0.85rem;">📅 2022 – 2025</span>
        <span style="color: {COLORS['text_muted']}; font-size: 0.85rem;">👤 Aditya Padmarajan</span>
        <span style="color: {COLORS['accent']}; font-size: 0.85rem;">🏆 PB: 3:26:00</span>
    </div>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# PAGE: OVERVIEW
# =============================================================================
if page == "🏠 Overview":
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🛣️ Total Distance", f"{total_distance:,.0f} km", f"{total_runs} runs")
    with col2:
        st.metric("🏅 Marathons", "6", "All Finished")
    with col3:
        st.metric("⏱️ Improved", "80 min", "4:46 → 3:26")
    with col4:
        st.metric("🏆 Personal Best", "3:26:00", "Oct 2025")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Two charts side by side
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"<h3 style='font-size: 1.1rem; margin-bottom: 0.5rem;'>📉 Race Progression</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: {COLORS['text_muted']}; font-size: 0.8rem; margin-bottom: 1rem;'>Finish times across 6 marathons</p>", unsafe_allow_html=True)
        
        races = marathon_df["Race"].tolist()
        times = marathon_df["Official Time (min)"].tolist()
        labels = marathon_df["Official Time"].tolist()
        
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=races, y=times, mode='lines+markers',
            line=dict(color=COLORS['line'], width=2.5),
            marker=dict(size=10, color=COLORS['primary_gradient'], line=dict(color=COLORS['bg_dark'], width=1.5)),
            hovertemplate="<b>%{x}</b><br>%{customdata}<extra></extra>", customdata=labels
        ))
        fig1.update_layout(
            yaxis=dict(autorange="reversed", tickvals=times, ticktext=labels, 
                      tickfont=dict(size=9, color=COLORS['text_secondary']), showgrid=True, gridcolor=COLORS['grid']),
            xaxis=dict(tickfont=dict(size=8, color=COLORS['text_secondary'])),
            height=280, plot_bgcolor=COLORS['bg_dark'], paper_bgcolor=COLORS['bg_dark'],
            margin=dict(l=55, r=15, t=10, b=35),
            hoverlabel=dict(bgcolor=COLORS['bg_card'], font_color=COLORS['text_bright'])
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.markdown(f"<h3 style='font-size: 1.1rem; margin-bottom: 0.5rem;'>📊 Yearly Volume</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: {COLORS['text_muted']}; font-size: 0.8rem; margin-bottom: 1rem;'>Distance per year</p>", unsafe_allow_html=True)
        
        yearly = running_df.groupby("Year")["Distance (km)"].sum().reset_index()
        years = yearly["Year"].astype(int).tolist()
        distances = yearly["Distance (km)"].tolist()
        
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=years, y=distances, marker_color=['#67E8F9', '#22D3EE', '#06B6D4', '#0891B2'],
            marker_line=dict(color=COLORS['bg_dark'], width=1.5),
            hovertemplate="<b>%{x}</b><br>%{y:,.0f} km<extra></extra>"
        ))
        fig2.update_layout(
            yaxis=dict(tickfont=dict(size=9, color=COLORS['text_secondary']), showgrid=True, gridcolor=COLORS['grid']),
            xaxis=dict(tickmode='array', tickvals=years, ticktext=[str(y) for y in years],
                      tickfont=dict(size=9, color=COLORS['text_secondary'])),
            height=280, plot_bgcolor=COLORS['bg_dark'], paper_bgcolor=COLORS['bg_dark'],
            margin=dict(l=45, r=15, t=10, b=35),
            hoverlabel=dict(bgcolor=COLORS['bg_card'], font_color=COLORS['text_bright'])
        )
        st.plotly_chart(fig2, use_container_width=True)

# =============================================================================
# PAGE: RACE TIMES
# =============================================================================
elif page == "🏃 Race Times":
    st.markdown(f"<h2 style='font-size: 1.4rem; margin-bottom: 0.25rem;'>The 80-Minute Journey</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: {COLORS['text_secondary']}; margin-bottom: 1.5rem;'>Marathon finish times from first race to personal best</p>", unsafe_allow_html=True)
    
    races = marathon_df["Race"].tolist()
    times = marathon_df["Official Time (min)"].tolist()
    labels = marathon_df["Official Time"].tolist()
    
    fig = go.Figure()
    
    # Fill
    fig.add_trace(go.Scatter(
        x=races + races[::-1], y=[max(times) + 10] * len(races) + times[::-1],
        fill='toself', fillcolor=COLORS['fill'], line=dict(color='rgba(0,0,0,0)'),
        showlegend=False, hoverinfo='skip'
    ))
    
    # Line
    fig.add_trace(go.Scatter(x=races, y=times, mode='lines', line=dict(color=COLORS['line'], width=3),
                             showlegend=False, hoverinfo='skip'))
    
    # Markers
    fig.add_trace(go.Scatter(
        x=races, y=times, mode='markers',
        marker=dict(size=16, color=COLORS['primary_gradient'], line=dict(color=COLORS['bg_dark'], width=2)),
        hovertemplate="<b>%{x}</b><br>%{customdata}<extra></extra>", customdata=labels, showlegend=False
    ))
    
    # Labels
    for i, (r, t, l) in enumerate(zip(races, times, labels)):
        fig.add_annotation(x=r, y=t, text=f"<b>{l}</b>", showarrow=False, yshift=-22 if i % 2 == 0 else 22,
            font=dict(size=10, color=COLORS['text_bright']), bgcolor=COLORS['bg_card'],
            bordercolor=COLORS['border'], borderwidth=1, borderpad=5)
    
    # Badges
    fig.add_annotation(x=2.5, y=250, text="<b>⚡ 80 min faster</b>", showarrow=False,
        font=dict(size=11, color=COLORS['accent']), bgcolor=COLORS['accent_bg'],
        bordercolor=COLORS['accent'], borderwidth=1, borderpad=8)
    fig.add_annotation(x=5, y=times[-1], text="<b>🏆 PB</b>", showarrow=False, yshift=-30,
        font=dict(size=10, color=COLORS['bg_dark']), bgcolor=COLORS['accent'], borderpad=5)
    
    fig.update_layout(
        yaxis=dict(autorange="reversed", title="<b>Finish Time</b>", tickvals=times, ticktext=labels,
                  tickfont=dict(size=10, color=COLORS['text_secondary']), showgrid=True, gridcolor=COLORS['grid'],
                  title_font=dict(size=11, color=COLORS['text_secondary'])),
        xaxis=dict(title="<b>Race</b>", tickfont=dict(size=10, color=COLORS['text_secondary']),
                  title_font=dict(size=11, color=COLORS['text_secondary'])),
        height=500, plot_bgcolor=COLORS['bg_dark'], paper_bgcolor=COLORS['bg_dark'],
        margin=dict(l=80, r=40, t=20, b=60),
        hoverlabel=dict(bgcolor=COLORS['bg_card'], font_color=COLORS['text_bright'], bordercolor=COLORS['border'])
    )
    st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# PAGE: PACE ANALYSIS
# =============================================================================
elif page == "⚡ Pace Analysis":
    st.markdown(f"<h2 style='font-size: 1.4rem; margin-bottom: 0.25rem;'>Pace Evolution</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: {COLORS['text_secondary']}; margin-bottom: 1.5rem;'>Average pace progression across six marathons</p>", unsafe_allow_html=True)
    
    races = marathon_df["Race"].tolist()
    paces = marathon_df["Pace (min/km)"].tolist()
    pace_labels = marathon_df["Pace (min:sec/km)"].tolist()
    
    fig = go.Figure()
    
    # Fill
    fig.add_trace(go.Scatter(
        x=races + races[::-1], y=[max(paces) + 0.3] * len(races) + paces[::-1],
        fill='toself', fillcolor=COLORS['fill'], line=dict(color='rgba(0,0,0,0)'),
        showlegend=False, hoverinfo='skip'
    ))
    
    # Line
    fig.add_trace(go.Scatter(x=races, y=paces, mode='lines', line=dict(color=COLORS['line'], width=3),
                             showlegend=False, hoverinfo='skip'))
    
    # Markers
    fig.add_trace(go.Scatter(
        x=races, y=paces, mode='markers',
        marker=dict(size=16, color=COLORS['primary_gradient'], line=dict(color=COLORS['bg_dark'], width=2)),
        hovertemplate="<b>%{x}</b><br>%{customdata}/km<extra></extra>", customdata=pace_labels, showlegend=False
    ))
    
    # Labels
    for i, (r, p, l) in enumerate(zip(races, paces, pace_labels)):
        fig.add_annotation(x=r, y=p, text=f"<b>{l}/km</b>", showarrow=False, yshift=22 if i % 2 == 0 else -22,
            font=dict(size=10, color=COLORS['text_bright']), bgcolor=COLORS['bg_card'],
            bordercolor=COLORS['border'], borderwidth=1, borderpad=5)
    
    # Badges
    improvement = paces[0] - paces[-1]
    fig.add_annotation(x=2.5, y=5.5, text=f"<b>⚡ {improvement:.1f} min/km faster</b>", showarrow=False,
        font=dict(size=11, color=COLORS['accent']), bgcolor=COLORS['accent_bg'],
        bordercolor=COLORS['accent'], borderwidth=1, borderpad=8)
    fig.add_annotation(x=5, y=paces[-1], text="<b>🏆 PB</b>", showarrow=False, yshift=30,
        font=dict(size=10, color=COLORS['bg_dark']), bgcolor=COLORS['accent'], borderpad=5)
    fig.add_annotation(x=0.98, y=0.08, xref="paper", yref="paper", text="<b>6:30 → 4:50 /km</b>",
        showarrow=False, font=dict(size=10, color=COLORS['line']), bgcolor=COLORS['bg_card'],
        bordercolor=COLORS['border'], borderwidth=1, borderpad=6, xanchor='right')
    
    fig.update_layout(
        yaxis=dict(autorange="reversed", title="<b>Pace (min/km)</b>", tickvals=paces, ticktext=pace_labels,
                  tickfont=dict(size=10, color=COLORS['text_secondary']), showgrid=True, gridcolor=COLORS['grid'],
                  title_font=dict(size=11, color=COLORS['text_secondary'])),
        xaxis=dict(title="<b>Race</b>", tickfont=dict(size=10, color=COLORS['text_secondary']),
                  title_font=dict(size=11, color=COLORS['text_secondary'])),
        height=500, plot_bgcolor=COLORS['bg_dark'], paper_bgcolor=COLORS['bg_dark'],
        margin=dict(l=80, r=40, t=20, b=60),
        hoverlabel=dict(bgcolor=COLORS['bg_card'], font_color=COLORS['text_bright'], bordercolor=COLORS['border'])
    )
    st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# PAGE: TRAINING VOLUME
# =============================================================================
elif page == "📈 Training Volume":
    st.markdown(f"<h2 style='font-size: 1.4rem; margin-bottom: 0.25rem;'>Building the Base</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: {COLORS['text_secondary']}; margin-bottom: 1.5rem;'>Total running distance per year</p>", unsafe_allow_html=True)
    
    yearly = running_df.groupby("Year")["Distance (km)"].sum().reset_index()
    years = yearly["Year"].astype(int).tolist()
    distances = yearly["Distance (km)"].tolist()
    runs = running_df.groupby("Year").size().tolist()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=years, y=distances, marker_color=['#67E8F9', '#22D3EE', '#06B6D4', '#0891B2'],
        marker_line=dict(color=COLORS['bg_dark'], width=2), width=0.55,
        hovertemplate="<b>%{x}</b><br>%{y:,.0f} km<extra></extra>"
    ))
    
    # Distance labels
    for i, (y, d) in enumerate(zip(years, distances)):
        fig.add_annotation(x=y, y=d + 35, text=f"<b>{d:,.0f} km</b>", showarrow=False,
            font=dict(size=12, color=COLORS['text_bright']), yanchor='bottom')
    
    # Run count labels
    for i, (y, d, r) in enumerate(zip(years, distances, runs)):
        fig.add_annotation(x=y, y=d / 2, text=f"<b>{r} runs</b>", showarrow=False,
            font=dict(size=10, color=COLORS['bg_dark']))
    
    # Badges
    growth = distances[-1] / distances[0]
    fig.add_annotation(x=2023.5, y=max(distances) * 1.15, text=f"<b>📈 {growth:.0f}x growth</b>",
        showarrow=False, font=dict(size=12, color=COLORS['accent']), bgcolor=COLORS['accent_bg'],
        bordercolor=COLORS['accent'], borderwidth=1, borderpad=8)
    fig.add_annotation(x=0.98, y=0.96, xref="paper", yref="paper", text=f"<b>Total: {sum(distances):,.0f} km</b>",
        showarrow=False, font=dict(size=11, color=COLORS['line']), bgcolor=COLORS['bg_card'],
        bordercolor=COLORS['border'], borderwidth=1, borderpad=8, xanchor='right', yanchor='top')
    
    fig.update_layout(
        yaxis=dict(title="<b>Distance (km)</b>", range=[0, max(distances) * 1.3],
                  tickfont=dict(size=10, color=COLORS['text_secondary']), showgrid=True, gridcolor=COLORS['grid'],
                  title_font=dict(size=11, color=COLORS['text_secondary'])),
        xaxis=dict(title="<b>Year</b>", tickmode='array', tickvals=years, ticktext=[str(y) for y in years],
                  tickfont=dict(size=11, color=COLORS['text_secondary']),
                  title_font=dict(size=11, color=COLORS['text_secondary'])),
        height=500, plot_bgcolor=COLORS['bg_dark'], paper_bgcolor=COLORS['bg_dark'],
        margin=dict(l=70, r=40, t=20, b=60), bargap=0.3,
        hoverlabel=dict(bgcolor=COLORS['bg_card'], font_color=COLORS['text_bright'], bordercolor=COLORS['border'])
    )
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 1rem 0;">
    <p style="color: {COLORS['text_muted']}; font-size: 0.8rem; margin: 0;">
        Built with ❤️ using Streamlit • Data from Strava • The 80-Minute Journey
    </p>
</div>
""", unsafe_allow_html=True)