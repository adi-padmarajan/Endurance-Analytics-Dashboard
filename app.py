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
# MULTI-COLOR PALETTE
# -----------------------------------------------------------------------------
COLORS = {
    'bg_dark': '#0F172A',
    'bg_card': '#1E293B',
    'bg_elevated': '#334155',
    'border': '#475569',
    'text_bright': '#F8FAFC',
    'text_primary': '#E2E8F0',
    'text_secondary': '#94A3B8',
    'text_muted': '#64748B',
    'accent': '#FBBF24',
    'accent_bg': 'rgba(251, 191, 36, 0.15)',
    'emerald_gradient': ['#6EE7B7', '#34D399', '#10B981', '#059669', '#047857', '#065F46'],
    'emerald_line': '#10B981',
    'emerald_fill': 'rgba(16, 185, 129, 0.15)',
    'violet_gradient': ['#C4B5FD', '#A78BFA', '#8B5CF6', '#7C3AED', '#6D28D9', '#5B21B6'],
    'violet_line': '#8B5CF6',
    'violet_fill': 'rgba(139, 92, 246, 0.15)',
    'rose_gradient': ['#FDA4AF', '#FB7185', '#F43F5E', '#E11D48', '#BE123C', '#9F1239'],
    'rose_line': '#F43F5E',
    'grid': 'rgba(148, 163, 184, 0.15)',
}

# -----------------------------------------------------------------------------
# CSS STYLING - WITH VISIBLE ARROW FOR SIDEBAR TOGGLE
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* ===== DARK MODE ===== */
    .stApp {
        background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* ===== MAKE SIDEBAR TOGGLE ARROW VERY VISIBLE ===== */
    
    /* Style the collapse button (when sidebar is open) */
    [data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
        border-radius: 50% !important;
        width: 36px !important;
        height: 36px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        border: 2px solid white !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4) !important;
        position: absolute !important;
        right: -18px !important;
        top: 50px !important;
        z-index: 9999 !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"]:hover {
        background: linear-gradient(135deg, #34D399 0%, #10B981 100%) !important;
        transform: scale(1.1) !important;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.5) !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] svg {
        color: white !important;
        width: 20px !important;
        height: 20px !important;
    }
    
    /* Style the expand button (when sidebar is closed) - THE ARROW */
    [data-testid="collapsedControl"] {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
        border-radius: 0 12px 12px 0 !important;
        width: 44px !important;
        height: 80px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        border: 2px solid white !important;
        border-left: none !important;
        box-shadow: 4px 4px 20px rgba(16, 185, 129, 0.5) !important;
        position: fixed !important;
        left: 0 !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        z-index: 999999 !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="collapsedControl"]:hover {
        background: linear-gradient(135deg, #34D399 0%, #10B981 100%) !important;
        width: 54px !important;
        box-shadow: 6px 6px 25px rgba(16, 185, 129, 0.6) !important;
    }
    
    [data-testid="collapsedControl"] svg {
        color: white !important;
        width: 28px !important;
        height: 28px !important;
    }
    
    /* Add arrow animation */
    [data-testid="collapsedControl"]::after {
        content: '';
        position: absolute;
        right: 8px;
        width: 0;
        height: 0;
        border-top: 8px solid transparent;
        border-bottom: 8px solid transparent;
        border-left: 10px solid rgba(255,255,255,0.5);
        animation: pulse-arrow 1.5s infinite;
    }
    
    @keyframes pulse-arrow {
        0%, 100% { opacity: 0.5; transform: translateX(0); }
        50% { opacity: 1; transform: translateX(3px); }
    }
    
    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E293B 0%, #0F172A 100%) !important;
        border-right: 1px solid #334155;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 0.5rem;
    }
    
    /* ===== TYPOGRAPHY ===== */
    h1, h2, h3 { color: #F8FAFC !important; }
    p, span, label { color: #CBD5E1 !important; }
    
    /* ===== METRICS ===== */
    [data-testid="stMetricValue"] {
        font-size: 1.6rem !important;
        font-weight: 700 !important;
    }
    [data-testid="stMetricLabel"] { color: #94A3B8 !important; font-size: 0.85rem !important; }
    [data-testid="stMetricDelta"] { color: #FBBF24 !important; }
    
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        border: 1px solid #475569;
        border-radius: 16px;
        padding: 1rem;
    }
    
    /* Metric colors per column */
    div[data-testid="column"]:nth-child(1) [data-testid="stMetricValue"] { color: #10B981 !important; }
    div[data-testid="column"]:nth-child(2) [data-testid="stMetricValue"] { color: #8B5CF6 !important; }
    div[data-testid="column"]:nth-child(3) [data-testid="stMetricValue"] { color: #F43F5E !important; }
    div[data-testid="column"]:nth-child(4) [data-testid="stMetricValue"] { color: #FBBF24 !important; }
    
    /* Dividers */
    hr { border-color: #334155 !important; }
    
    /* Radio buttons */
    [data-testid="stSidebar"] .stRadio > div > label {
        background: transparent;
        padding: 0.75rem 1rem;
        border-radius: 10px;
        margin: 3px 0;
        transition: all 0.2s;
        border: 1px solid transparent;
    }
    [data-testid="stSidebar"] .stRadio > div > label:hover {
        background: rgba(16, 185, 129, 0.1);
        border-color: rgba(16, 185, 129, 0.3);
    }
    
    /* ===== MOBILE RESPONSIVE ===== */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 0.5rem 1rem !important;
        }
        
        [data-testid="stMetricValue"] {
            font-size: 1.2rem !important;
        }
        
        [data-testid="metric-container"] {
            padding: 0.75rem;
        }
        
        h1 { font-size: 1.5rem !important; }
        h2 { font-size: 1.2rem !important; }
        
        div[data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
        }
        
        [data-testid="collapsedControl"] {
            height: 60px !important;
            width: 36px !important;
        }
    }
    
    @media (max-width: 480px) {
        .main .block-container {
            padding: 0.25rem 0.5rem !important;
        }
        
        [data-testid="stMetricValue"] {
            font-size: 1rem !important;
        }
        
        h1 { font-size: 1.25rem !important; }
    }
    
    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #1E293B; }
    ::-webkit-scrollbar-thumb { background: #475569; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #64748B; }
</style>
""", unsafe_allow_html=True)

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
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">🏃</div>
        <h2 style="color: {COLORS['text_bright']}; font-size: 1.1rem; margin: 0; font-weight: 700;">
            The 80-Minute Journey
        </h2>
        <p style="color: {COLORS['text_muted']}; font-size: 0.7rem; margin-top: 0.5rem;">
            Marathon Analytics Dashboard
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tip about arrow
    st.markdown(f"""
    <p style="color: {COLORS['text_muted']}; font-size: 0.65rem; text-align: center; margin-bottom: 1rem; 
       background: {COLORS['bg_elevated']}; padding: 0.5rem; border-radius: 8px;">
        💡 Click the <span style="color: #10B981; font-weight: bold;">green arrow</span> on the edge to close/open
    </p>
    """, unsafe_allow_html=True)
    
    # Navigation
    st.markdown(f"""
    <p style="color: {COLORS['text_muted']}; font-size: 0.65rem; text-transform: uppercase; 
       letter-spacing: 0.15em; margin-bottom: 0.5rem; font-weight: 600;">
        📍 Navigation
    </p>
    """, unsafe_allow_html=True)
    
    page = st.radio(
        "Navigation",
        ["🏠 Overview", "🏃 Race Times", "⚡ Pace Analysis", "📈 Training Volume"],
        label_visibility="collapsed"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quick Stats
    st.markdown(f"""
    <div style="background: {COLORS['bg_elevated']}; border-radius: 12px; padding: 1rem; 
         border: 1px solid {COLORS['border']};">
        <p style="color: {COLORS['text_muted']}; font-size: 0.65rem; text-transform: uppercase; 
           letter-spacing: 0.15em; margin-bottom: 0.75rem; font-weight: 600;">
            📊 Quick Stats
        </p>
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="color: {COLORS['text_secondary']}; font-size: 0.8rem;">Distance</span>
            <span style="color: #10B981; font-weight: 700;">{total_distance:,.0f} km</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="color: {COLORS['text_secondary']}; font-size: 0.8rem;">Runs</span>
            <span style="color: #8B5CF6; font-weight: 700;">{total_runs}</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="color: {COLORS['text_secondary']}; font-size: 0.8rem;">Marathons</span>
            <span style="color: #F43F5E; font-weight: 700;">{total_marathons}</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <span style="color: {COLORS['text_secondary']}; font-size: 0.8rem;">Personal Best</span>
            <span style="color: {COLORS['accent']}; font-weight: 700;">3:26:00</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown(f"""
    <div style="margin-top: 2rem; padding-top: 1rem; border-top: 1px solid {COLORS['border']}; text-align: center;">
        <p style="color: {COLORS['text_muted']}; font-size: 0.7rem; margin: 0;">
            Built by <span style="color: #10B981;">Aditya Padmarajan</span>
        </p>
        <p style="color: {COLORS['text_muted']}; font-size: 0.6rem; margin-top: 0.25rem;">
            Data from Strava • 2022-2025
        </p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MAIN HEADER
# -----------------------------------------------------------------------------
st.markdown(f"""
<div style="background: linear-gradient(135deg, {COLORS['bg_card']} 0%, {COLORS['bg_elevated']} 100%);
     border-radius: 16px; padding: 1.25rem 1.5rem; margin-bottom: 1.5rem; border: 1px solid {COLORS['border']};">
    <div style="display: flex; align-items: center; gap: 1rem; flex-wrap: wrap;">
        <span style="font-size: 2.5rem;">🏃</span>
        <div>
            <h1 style="color: {COLORS['text_bright']}; font-size: 1.6rem; font-weight: 700; margin: 0;">
                The 80-Minute Journey
            </h1>
            <p style="color: {COLORS['text_secondary']}; font-size: 0.9rem; margin: 0.25rem 0 0 0;">
                A Data-Driven Analysis of Marathon Progression
            </p>
        </div>
    </div>
    <div style="display: flex; gap: 1.5rem; margin-top: 1rem; flex-wrap: wrap;">
        <span style="color: {COLORS['text_muted']}; font-size: 0.8rem;">📅 2022 – 2025</span>
        <span style="color: {COLORS['text_muted']}; font-size: 0.8rem;">👤 Aditya Padmarajan</span>
        <span style="color: {COLORS['accent']}; font-size: 0.8rem; font-weight: 600;">🏆 PB: 3:26:00</span>
    </div>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# PAGE: OVERVIEW
# =============================================================================
if page == "🏠 Overview":
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
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <h3 style='font-size: 1rem; margin-bottom: 0.25rem; color: #10B981;'>📉 The 80-Minute Journey</h3>
        <p style='color: {COLORS["text_muted"]}; font-size: 0.75rem; margin-bottom: 0.75rem;'>Marathon finish times from first race to personal best</p>
        """, unsafe_allow_html=True)
        
        races = marathon_df["Race"].tolist()
        times = marathon_df["Official Time (min)"].tolist()
        labels = marathon_df["Official Time"].tolist()
        
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=races, y=times, mode='lines+markers',
            line=dict(color=COLORS['emerald_line'], width=2.5),
            marker=dict(size=10, color=COLORS['emerald_gradient'], line=dict(color=COLORS['bg_dark'], width=1.5)),
            hovertemplate="<b>%{x}</b><br>Time: %{customdata}<extra></extra>", customdata=labels
        ))
        fig1.update_layout(
            yaxis=dict(autorange="reversed", tickvals=times, ticktext=labels, 
                      tickfont=dict(size=9, color=COLORS['text_secondary']), 
                      showgrid=True, gridcolor=COLORS['grid'],
                      title=dict(text="<b>Finish Time (H:M:S)</b>", font=dict(size=10, color=COLORS['text_secondary']))),
            xaxis=dict(tickfont=dict(size=8, color=COLORS['text_secondary']),
                      title=dict(text="<b>Race</b>", font=dict(size=10, color=COLORS['text_secondary']))),
            height=300, plot_bgcolor=COLORS['bg_dark'], paper_bgcolor=COLORS['bg_dark'],
            margin=dict(l=70, r=15, t=10, b=50),
            hoverlabel=dict(bgcolor=COLORS['bg_card'], font_color=COLORS['text_bright'])
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.markdown(f"""
        <h3 style='font-size: 1rem; margin-bottom: 0.25rem; color: #F43F5E;'>📊 Building the Base</h3>
        <p style='color: {COLORS["text_muted"]}; font-size: 0.75rem; margin-bottom: 0.75rem;'>Total running distance per year</p>
        """, unsafe_allow_html=True)
        
        yearly = running_df.groupby("Year")["Distance (km)"].sum().reset_index()
        years = yearly["Year"].astype(int).tolist()
        distances = yearly["Distance (km)"].tolist()
        
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=years, y=distances, 
            marker_color=['#FDA4AF', '#FB7185', '#F43F5E', '#E11D48'],
            marker_line=dict(color=COLORS['bg_dark'], width=1.5),
            hovertemplate="<b>%{x}</b><br>Distance: %{y:,.0f} km<extra></extra>"
        ))
        fig2.update_layout(
            yaxis=dict(tickfont=dict(size=9, color=COLORS['text_secondary']), 
                      showgrid=True, gridcolor=COLORS['grid'],
                      title=dict(text="<b>Distance (km)</b>", font=dict(size=10, color=COLORS['text_secondary']))),
            xaxis=dict(tickmode='array', tickvals=years, ticktext=[str(y) for y in years],
                      tickfont=dict(size=9, color=COLORS['text_secondary']),
                      title=dict(text="<b>Year</b>", font=dict(size=10, color=COLORS['text_secondary']))),
            height=300, plot_bgcolor=COLORS['bg_dark'], paper_bgcolor=COLORS['bg_dark'],
            margin=dict(l=60, r=15, t=10, b=50),
            hoverlabel=dict(bgcolor=COLORS['bg_card'], font_color=COLORS['text_bright'])
        )
        st.plotly_chart(fig2, use_container_width=True)

# =============================================================================
# PAGE: RACE TIMES
# =============================================================================
elif page == "🏃 Race Times":
    st.markdown(f"""
    <h2 style='font-size: 1.4rem; margin-bottom: 0.25rem; color: #10B981;'>🏃 The 80-Minute Journey</h2>
    <p style='color: {COLORS["text_secondary"]}; font-size: 0.9rem; margin-bottom: 1.5rem;'>
        Marathon finish times from first race to personal best • 6 races across 3.5 years
    </p>
    """, unsafe_allow_html=True)
    
    races = marathon_df["Race"].tolist()
    times = marathon_df["Official Time (min)"].tolist()
    labels = marathon_df["Official Time"].tolist()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=races + races[::-1], y=[max(times) + 12] * len(races) + times[::-1],
        fill='toself', fillcolor=COLORS['emerald_fill'], line=dict(color='rgba(0,0,0,0)'),
        showlegend=False, hoverinfo='skip'
    ))
    
    fig.add_trace(go.Scatter(
        x=races, y=times, mode='lines', 
        line=dict(color=COLORS['emerald_line'], width=3.5),
        showlegend=False, hoverinfo='skip'
    ))
    
    fig.add_trace(go.Scatter(
        x=races, y=times, mode='markers',
        marker=dict(size=18, color=COLORS['emerald_gradient'], 
                   line=dict(color=COLORS['bg_dark'], width=2.5)),
        hovertemplate="<b>%{x}</b><br>Finish Time: %{customdata}<extra></extra>", 
        customdata=labels, showlegend=False
    ))
    
    for i, (r, t, l) in enumerate(zip(races, times, labels)):
        yshift = -28 if i % 2 == 0 else 28
        fig.add_annotation(
            x=r, y=t, text=f"<b>{l}</b>", showarrow=False, yshift=yshift,
            font=dict(size=11, color=COLORS['text_bright']), 
            bgcolor=COLORS['bg_card'], bordercolor='#10B981', borderwidth=1, borderpad=6
        )
    
    fig.add_annotation(
        x=2.5, y=252, text="<b>⚡ 80 minutes faster</b>", showarrow=False,
        font=dict(size=12, color='#10B981'), 
        bgcolor='rgba(16, 185, 129, 0.15)', bordercolor='#10B981', borderwidth=1.5, borderpad=10
    )
    fig.add_annotation(
        x=5, y=times[-1], text="<b>🏆 PB</b>", showarrow=False, yshift=-35,
        font=dict(size=11, color=COLORS['bg_dark']), bgcolor=COLORS['accent'], borderpad=6
    )
    
    fig.update_layout(
        yaxis=dict(
            autorange="reversed",
            title=dict(text="<b>Finish Time (H:M:S)</b>", font=dict(size=12, color=COLORS['text_secondary']), standoff=15),
            tickvals=times, ticktext=labels,
            tickfont=dict(size=11, color=COLORS['text_secondary']),
            showgrid=True, gridcolor=COLORS['grid'], gridwidth=1,
            zeroline=False, showline=True, linecolor=COLORS['border'], linewidth=1
        ),
        xaxis=dict(
            title=dict(text="<b>Race</b>", font=dict(size=12, color=COLORS['text_secondary']), standoff=15),
            tickfont=dict(size=11, color=COLORS['text_secondary']),
            showgrid=False, zeroline=False, showline=True, linecolor=COLORS['border'], linewidth=1
        ),
        height=520, plot_bgcolor=COLORS['bg_dark'], paper_bgcolor=COLORS['bg_dark'],
        margin=dict(l=90, r=50, t=30, b=70),
        hoverlabel=dict(bgcolor=COLORS['bg_card'], font_color=COLORS['text_bright'], font_size=12)
    )
    st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# PAGE: PACE ANALYSIS
# =============================================================================
elif page == "⚡ Pace Analysis":
    st.markdown(f"""
    <h2 style='font-size: 1.4rem; margin-bottom: 0.25rem; color: #8B5CF6;'>⚡ Pace Evolution Curve</h2>
    <p style='color: {COLORS["text_secondary"]}; font-size: 0.9rem; margin-bottom: 1.5rem;'>
        Average pace progression across six marathons • From 6:30/km to 4:50/km
    </p>
    """, unsafe_allow_html=True)
    
    races = marathon_df["Race"].tolist()
    paces = marathon_df["Pace (min/km)"].tolist()
    pace_labels = marathon_df["Pace (min:sec/km)"].tolist()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=races + races[::-1], y=[max(paces) + 0.4] * len(races) + paces[::-1],
        fill='toself', fillcolor=COLORS['violet_fill'], line=dict(color='rgba(0,0,0,0)'),
        showlegend=False, hoverinfo='skip'
    ))
    
    fig.add_trace(go.Scatter(
        x=races, y=paces, mode='lines',
        line=dict(color=COLORS['violet_line'], width=3.5),
        showlegend=False, hoverinfo='skip'
    ))
    
    fig.add_trace(go.Scatter(
        x=races, y=paces, mode='markers',
        marker=dict(size=18, color=COLORS['violet_gradient'], 
                   line=dict(color=COLORS['bg_dark'], width=2.5)),
        hovertemplate="<b>%{x}</b><br>Pace: %{customdata}/km<extra></extra>",
        customdata=pace_labels, showlegend=False
    ))
    
    for i, (r, p, l) in enumerate(zip(races, paces, pace_labels)):
        yshift = 28 if i % 2 == 0 else -28
        fig.add_annotation(
            x=r, y=p, text=f"<b>{l}/km</b>", showarrow=False, yshift=yshift,
            font=dict(size=11, color=COLORS['text_bright']),
            bgcolor=COLORS['bg_card'], bordercolor='#8B5CF6', borderwidth=1, borderpad=6
        )
    
    improvement = paces[0] - paces[-1]
    fig.add_annotation(
        x=2.5, y=5.55, text=f"<b>⚡ {improvement:.1f} min/km faster</b>", showarrow=False,
        font=dict(size=12, color='#8B5CF6'),
        bgcolor='rgba(139, 92, 246, 0.15)', bordercolor='#8B5CF6', borderwidth=1.5, borderpad=10
    )
    fig.add_annotation(
        x=5, y=paces[-1], text="<b>🏆 PB</b>", showarrow=False, yshift=35,
        font=dict(size=11, color=COLORS['bg_dark']), bgcolor=COLORS['accent'], borderpad=6
    )
    fig.add_annotation(
        x=0.98, y=0.06, xref="paper", yref="paper",
        text="<b>6:30 → 4:50 /km</b>", showarrow=False,
        font=dict(size=11, color='#8B5CF6'),
        bgcolor=COLORS['bg_card'], bordercolor='#8B5CF6', borderwidth=1, borderpad=8, xanchor='right'
    )
    
    fig.update_layout(
        yaxis=dict(
            autorange="reversed",
            title=dict(text="<b>Pace (min/km)</b>", font=dict(size=12, color=COLORS['text_secondary']), standoff=15),
            tickvals=paces, ticktext=pace_labels,
            tickfont=dict(size=11, color=COLORS['text_secondary']),
            showgrid=True, gridcolor=COLORS['grid'], gridwidth=1,
            zeroline=False, showline=True, linecolor=COLORS['border'], linewidth=1
        ),
        xaxis=dict(
            title=dict(text="<b>Race</b>", font=dict(size=12, color=COLORS['text_secondary']), standoff=15),
            tickfont=dict(size=11, color=COLORS['text_secondary']),
            showgrid=False, zeroline=False, showline=True, linecolor=COLORS['border'], linewidth=1
        ),
        height=520, plot_bgcolor=COLORS['bg_dark'], paper_bgcolor=COLORS['bg_dark'],
        margin=dict(l=90, r=50, t=30, b=70),
        hoverlabel=dict(bgcolor=COLORS['bg_card'], font_color=COLORS['text_bright'], font_size=12)
    )
    st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# PAGE: TRAINING VOLUME
# =============================================================================
elif page == "📈 Training Volume":
    st.markdown(f"""
    <h2 style='font-size: 1.4rem; margin-bottom: 0.25rem; color: #F43F5E;'>📈 Building the Base</h2>
    <p style='color: {COLORS["text_secondary"]}; font-size: 0.9rem; margin-bottom: 1.5rem;'>
        Total running distance per year • From 246 km to 1,712 km
    </p>
    """, unsafe_allow_html=True)
    
    yearly = running_df.groupby("Year")["Distance (km)"].sum().reset_index()
    years = yearly["Year"].astype(int).tolist()
    distances = yearly["Distance (km)"].tolist()
    runs = running_df.groupby("Year").size().tolist()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=years, y=distances,
        marker_color=COLORS['rose_gradient'][:4],
        marker_line=dict(color='white', width=2),
        width=0.6,
        hovertemplate="<b>%{x}</b><br>Distance: %{y:,.0f} km<extra></extra>"
    ))
    
    for i, (y, d) in enumerate(zip(years, distances)):
        fig.add_annotation(
            x=y, y=d + 45, text=f"<b>{d:,.0f} km</b>", showarrow=False,
            font=dict(size=13, color=COLORS['text_bright']), yanchor='bottom'
        )
    
    for i, (y, d, r) in enumerate(zip(years, distances, runs)):
        fig.add_annotation(
            x=y, y=d / 2, text=f"<b>{r} runs</b>", showarrow=False,
            font=dict(size=11, color='white' if i >= 1 else COLORS['bg_dark'])
        )
    
    growth = distances[-1] / distances[0]
    fig.add_annotation(
        x=2023.5, y=max(distances) * 1.18, text=f"<b>📈 {growth:.0f}x volume growth</b>",
        showarrow=False, font=dict(size=13, color='#F43F5E'),
        bgcolor='rgba(244, 63, 94, 0.15)', bordercolor='#F43F5E', borderwidth=1.5, borderpad=10
    )
    total_km = sum(distances)
    fig.add_annotation(
        x=0.98, y=0.96, xref="paper", yref="paper",
        text=f"<b>Total: {total_km:,.0f} km</b>", showarrow=False,
        font=dict(size=12, color='#F43F5E'),
        bgcolor=COLORS['bg_card'], bordercolor='#F43F5E', borderwidth=1, borderpad=10,
        xanchor='right', yanchor='top'
    )
    
    fig.update_layout(
        yaxis=dict(
            title=dict(text="<b>Cumulative Distance (km)</b>", font=dict(size=12, color=COLORS['text_secondary']), standoff=15),
            range=[0, max(distances) * 1.35],
            tickfont=dict(size=11, color=COLORS['text_secondary']),
            showgrid=True, gridcolor=COLORS['grid'], gridwidth=1,
            zeroline=False, showline=True, linecolor=COLORS['border'], linewidth=1
        ),
        xaxis=dict(
            title=dict(text="<b>Year</b>", font=dict(size=12, color=COLORS['text_secondary']), standoff=15),
            tickmode='array', tickvals=years, ticktext=[str(y) for y in years],
            tickfont=dict(size=12, color=COLORS['text_secondary']),
            showgrid=False, zeroline=False, showline=True, linecolor=COLORS['border'], linewidth=1
        ),
        height=520, plot_bgcolor=COLORS['bg_dark'], paper_bgcolor=COLORS['bg_dark'],
        margin=dict(l=80, r=50, t=30, b=70), bargap=0.25,
        hoverlabel=dict(bgcolor=COLORS['bg_card'], font_color=COLORS['text_bright'], font_size=12)
    )
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 1rem 0;">
    <p style="color: {COLORS['text_muted']}; font-size: 0.75rem; margin: 0;">
        Built with ❤️ by <span style="color: #10B981;">Aditya Padmarajan</span> • 
        Data from <span style="color: #8B5CF6;">Strava</span> • 
        <span style="color: #F43F5E;">The 80-Minute Journey</span>
    </p>
</div>
""", unsafe_allow_html=True)