# =============================================================================
# THE 80-MINUTE JOURNEY: STREAMLIT DASHBOARD
# =============================================================================
# Converted from: endurance_analytics.ipynb
# Author: Aditya Padmarajan
# 
# This Streamlit app transforms the Jupyter notebook analysis into an
# interactive web dashboard with multiple views and filtering capabilities.
# =============================================================================

# -----------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------
import streamlit as st                    # ADDED: Core Streamlit library
import pandas as pd
import numpy as np
import plotly.express as px               # ADDED: Interactive charts (replaces matplotlib)
import plotly.graph_objects as go         # ADDED: Advanced Plotly charts

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
# ADDED: Configure the Streamlit page settings
st.set_page_config(
    page_title="The 80-Minute Journey",   # Browser tab title
    page_icon="🏃",                        # Browser tab icon
    layout="wide",                         # Use full screen width
    initial_sidebar_state="expanded"       # Sidebar open by default
)

# -----------------------------------------------------------------------------
# CUSTOM CSS STYLING
# -----------------------------------------------------------------------------
# ADDED: Custom CSS for better visual appearance
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        background: linear-gradient(135deg, #2E7D32 0%, #1B5E20 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    
    /* Metric card styling */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #2E7D32;
    }
    
    /* Section headers */
    .section-header {
        color: #1B5E20;
        border-bottom: 2px solid #2E7D32;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATA LOADING FUNCTION
# -----------------------------------------------------------------------------
# ADDED: Cached data loading for performance
@st.cache_data
def load_data():
    """
    Load and preprocess the activities dataset.
    Uses @st.cache_data to avoid reloading on every interaction.
    
    This function replicates the data processing from your notebook's
    Data Collection and Pre-Processing cells.
    """
    # Load raw data (same as notebook Cell 4)
    df = pd.read_csv("activities_dataset.csv")
    
    # Filter to running activities (same as notebook)
    df2 = df.query("`Activity Type` == 'Run'").reset_index(drop=True)
    
    # Rename columns (same as notebook Cell 4)
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
    
    # Parse dates (same as notebook Cell 6)
    df2["Activity Date"] = pd.to_datetime(df2["Activity Date"], format="%b %d, %Y, %I:%M:%S %p")
    
    # Time-based columns (same as notebook Cell 6)
    df2["Year"] = df2["Activity Date"].dt.year
    df2["Month"] = df2["Activity Date"].dt.month
    df2["Week"] = df2["Activity Date"].dt.isocalendar().week
    df2["Day"] = df2["Activity Date"].dt.day_name()
    
    # Calculate pace (same as notebook Cell 6)
    df2["Pace (min/km)"] = 1000 / (df2["Avg Speed (m/s)"] * 60)
    df2["Pace (min:sec/km)"] = df2["Pace (min/km)"].apply(
        lambda x: f"{int(x)}:{int((x % 1) * 60):02d}"
    )
    
    # Formatted time columns (same as notebook Cell 6)
    df2["Moving Time (H:M:S)"] = df2["Moving Time (s)"].apply(
        lambda x: f"{int(x // 3600)}:{int((x % 3600) // 60):02d}:{int(x % 60):02d}" if pd.notna(x) else None
    )
    
    # Select columns (same as notebook Cell 6)
    cols_to_keep = [
        "Activity ID", "Activity Date", "Year", "Month", "Week", "Day",
        "Activity Name", "Activity Type", "Distance (km)", "Pace (min/km)",
        "Pace (min:sec/km)", "Moving Time (s)", "Moving Time (H:M:S)",
        "Elapsed Time (s)", "Avg HR (bpm)", "Max HR (bpm)",
        "Elevation Gain (m)", "Elevation Loss (m)", "Calories", "Relative Effort"
    ]
    
    running_df = df2[[c for c in cols_to_keep if c in df2.columns]].reset_index(drop=True)
    
    # Flag HR availability (same as notebook Cell 6)
    running_df["HR Available"] = running_df["Avg HR (bpm)"].notna()
    
    return running_df

# -----------------------------------------------------------------------------
# MARATHON DATA FUNCTION
# -----------------------------------------------------------------------------
# ADDED: Separate function for marathon-specific data
@st.cache_data
def get_marathon_data(running_df):
    """
    Extract and enrich marathon data with official times.
    Replicates notebook Cell 8.
    """
    # Extract marathons (same as notebook)
    marathon_df = running_df[running_df["Distance (km)"] > 40].copy().reset_index(drop=True)
    
    # Add race names (same as notebook Cell 8)
    marathon_df["Race"] = ["RVM 2022", "BMO 2023", "RVM 2023", "RVM 2024", "BMO 2025", "RVM 2025"]
    
    # Official times (same as notebook Cell 8)
    marathon_df["Official Time"] = ["4:46:07", "4:25:48", "4:16:58", "3:47:47", "3:37:23", "3:26:00"]
    
    # Official times in seconds (same as notebook Cell 8)
    marathon_df["Official Time (s)"] = [
        4*3600 + 46*60 + 7,
        4*3600 + 25*60 + 48,
        4*3600 + 16*60 + 58,
        3*3600 + 47*60 + 47,
        3*3600 + 37*60 + 23,
        3*3600 + 26*60 + 0
    ]
    
    # Official times in minutes (same as notebook Cell 8)
    marathon_df["Official Time (min)"] = marathon_df["Official Time (s)"] / 60
    
    # ADDED: Official pace for plotting
    marathon_df["Official Pace (min/km)"] = marathon_df["Official Time (min)"] / 42.195
    marathon_df["Official Pace"] = marathon_df["Official Pace (min/km)"].apply(
        lambda x: f"{int(x)}:{int((x % 1) * 60):02d}"
    )
    
    return marathon_df

# -----------------------------------------------------------------------------
# LOAD DATA
# -----------------------------------------------------------------------------
# Load the data using cached functions
running_df = load_data()
marathon_df = get_marathon_data(running_df)

# -----------------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------------
# ADDED: Sidebar for navigation and filters
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/running--v1.png", width=80)
    st.title("🏃 Navigation")
    
    # ADDED: Page selection
    page = st.radio(
        "Select View",
        ["🏠 Overview", "📈 Marathon Progression", "🏋️ Training Analysis", 
         "❤️ Heart Rate Efficiency", "📊 Data Explorer", "💡 Insights"],
        index=0
    )
    
    st.markdown("---")
    
    # ADDED: Year filter
    st.subheader("🔍 Filters")
    years = sorted(running_df["Year"].unique())
    selected_years = st.multiselect(
        "Select Years",
        options=years,
        default=years
    )
    
    # ADDED: Distance filter
    min_dist, max_dist = st.slider(
        "Distance Range (km)",
        min_value=0.0,
        max_value=float(running_df["Distance (km)"].max()),
        value=(0.0, float(running_df["Distance (km)"].max()))
    )
    
    st.markdown("---")
    st.markdown("**Author:** Aditya Padmarajan")
    st.markdown("**Data:** Strava Export (2022-2025)")

# -----------------------------------------------------------------------------
# FILTER DATA BASED ON SIDEBAR SELECTIONS
# -----------------------------------------------------------------------------
# ADDED: Apply filters to dataframe
filtered_df = running_df[
    (running_df["Year"].isin(selected_years)) &
    (running_df["Distance (km)"] >= min_dist) &
    (running_df["Distance (km)"] <= max_dist)
]

# =============================================================================
# PAGE: OVERVIEW
# =============================================================================
if page == "🏠 Overview":
    # ADDED: Header section
    st.markdown("""
    <div class="main-header">
        <h1>🏃 The 80-Minute Journey</h1>
        <p style="font-size: 1.2rem; opacity: 0.9;">
            A Data-Driven Analysis of Marathon Progression (2022-2025)
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ADDED: Key metrics row (replaces static text from notebook intro)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_distance = filtered_df["Distance (km)"].sum()
        st.metric(
            label="🛣️ Total Distance",
            value=f"{total_distance:,.0f} km",
            delta=f"{len(filtered_df)} runs"
        )
    
    with col2:
        st.metric(
            label="🏅 Marathons",
            value="6",
            delta="All Finished"
        )
    
    with col3:
        st.metric(
            label="⏱️ Time Improved",
            value="80 min",
            delta="4:46 → 3:26"
        )
    
    with col4:
        st.metric(
            label="🏆 Personal Best",
            value="3:26:00",
            delta="RVM 2025"
        )
    
    st.markdown("---")
    
    # ADDED: Two-column layout for overview charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Marathon Progression Chart (from notebook Cell 8)
        st.subheader("📉 Marathon Progression")
        
        # ADDED: Using Plotly instead of matplotlib for interactivity
        fig = go.Figure()
        
        # Add the line
        fig.add_trace(go.Scatter(
            x=marathon_df["Race"],
            y=marathon_df["Official Time (min)"],
            mode='lines+markers',
            line=dict(color='#2E7D32', width=3),
            marker=dict(
                size=15,
                color=marathon_df["Official Time (min)"],
                colorscale='RdYlGn_r',  # Red to Green reversed
                showscale=False
            ),
            text=marathon_df["Official Time"],
            hovertemplate="<b>%{x}</b><br>Time: %{text}<extra></extra>"
        ))
        
        fig.update_layout(
            yaxis=dict(
                autorange="reversed",  # Faster times at top
                title="Finish Time",
                tickvals=marathon_df["Official Time (min)"].tolist(),
                ticktext=marathon_df["Official Time"].tolist()
            ),
            xaxis_title="Race",
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Yearly Volume Chart (from notebook Cell 12)
        st.subheader("📊 Building the Base")
        
        yearly_data = filtered_df.groupby("Year")["Distance (km)"].sum().reset_index()
        yearly_counts = filtered_df.groupby("Year").size().reset_index(name="Runs")
        yearly_data = yearly_data.merge(yearly_counts, on="Year")
        
        # ADDED: Plotly bar chart
        fig = px.bar(
            yearly_data,
            x="Year",
            y="Distance (km)",
            text=yearly_data["Distance (km)"].apply(lambda x: f"{x:,.0f} km"),
            color="Distance (km)",
            color_continuous_scale="Greens"
        )
        
        fig.update_traces(textposition='outside')
        fig.update_layout(
            showlegend=False,
            coloraxis_showscale=False,
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis_title="Year",
            yaxis_title="Total Distance (km)"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # ADDED: Project overview text (from notebook intro)
    st.markdown("---")
    st.subheader("📖 Project Overview")
    st.markdown("""
    This dashboard analyzes **347 running activities over 3.5 years**, documenting the progression 
    from a first-time marathoner (4:46:07 at Royal Victoria Marathon 2022) to a sub-3:30 finisher 
    (3:26:00 at Royal Victoria Marathon 2025) — an improvement of **80 minutes** across 6 marathon races.
    
    The analysis explores how training patterns, physiological adaptations, and race execution 
    evolved to produce consistent performance gains at two recurring races:
    - **Royal Victoria Marathon** (4 finishes)
    - **BMO Vancouver Marathon** (2 finishes)
    """)

# =============================================================================
# PAGE: MARATHON PROGRESSION
# =============================================================================
elif page == "📈 Marathon Progression":
    st.title("📈 Marathon Progression")
    st.markdown("*Official finish times across all six marathons*")
    
    # ADDED: Tabs for different views
    tab1, tab2 = st.tabs(["📉 Time Progression", "🏃 Pace Evolution"])
    
    with tab1:
        # Marathon Progression Timeline (from notebook Cell 8)
        st.subheader("The 80-Minute Journey")
        
        # ADDED: Enhanced Plotly chart with annotations
        fig = go.Figure()
        
        # Green fill area
        fig.add_trace(go.Scatter(
            x=marathon_df["Race"],
            y=marathon_df["Official Time (min)"],
            fill='tozeroy',
            fillcolor='rgba(46, 125, 50, 0.1)',
            line=dict(color='#2E7D32', width=3),
            mode='lines'
        ))
        
        # Markers with gradient colors
        colors = ['#d32f2f', '#f57c00', '#fbc02d', '#7cb342', '#43a047', '#2e7d32']
        fig.add_trace(go.Scatter(
            x=marathon_df["Race"],
            y=marathon_df["Official Time (min)"],
            mode='markers+text',
            marker=dict(size=20, color=colors, line=dict(color='white', width=2)),
            text=marathon_df["Official Time"],
            textposition="top center",
            textfont=dict(size=12, color='#333'),
            hovertemplate="<b>%{x}</b><br>Time: %{text}<extra></extra>"
        ))
        
        # ADDED: Improvement annotation
        fig.add_annotation(
            x=2.5, y=250,
            text="<b>80 minutes faster</b>",
            showarrow=True,
            arrowhead=2,
            arrowcolor="#1976D2",
            font=dict(size=14, color="#1976D2"),
            bgcolor="#E3F2FD",
            bordercolor="#1976D2",
            borderwidth=2
        )
        
        fig.update_layout(
            yaxis=dict(
                autorange="reversed",
                title="Finish Time",
                tickvals=marathon_df["Official Time (min)"].tolist(),
                ticktext=marathon_df["Official Time"].tolist()
            ),
            xaxis_title="Race",
            height=500,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # ADDED: Description (from your markdown descriptions)
        st.info("""
        **Key Insight:** The consistent downward trend demonstrates that every single marathon 
        was faster than the previous one — **no setbacks across 3 years of racing**. The 80-minute 
        improvement represents a 28% reduction in finish time.
        """)
    
    with tab2:
        # Pace Evolution Curve (from notebook Cell 10)
        st.subheader("Pace Evolution Curve")
        
        # ADDED: Plotly version of pace chart
        fig = go.Figure()
        
        # Blue fill area
        fig.add_trace(go.Scatter(
            x=marathon_df["Race"],
            y=marathon_df["Pace (min/km)"],
            fill='tozeroy',
            fillcolor='rgba(21, 101, 192, 0.1)',
            line=dict(color='#1565C0', width=3),
            mode='lines'
        ))
        
        # Markers with blue gradient
        blue_colors = ['#bbdefb', '#90caf9', '#64b5f6', '#42a5f5', '#2196f3', '#1976d2']
        fig.add_trace(go.Scatter(
            x=marathon_df["Race"],
            y=marathon_df["Pace (min/km)"],
            mode='markers+text',
            marker=dict(size=20, color=blue_colors, line=dict(color='white', width=2)),
            text=marathon_df["Pace (min:sec/km)"].astype(str) + "/km",
            textposition="top center",
            textfont=dict(size=11, color='#333'),
            hovertemplate="<b>%{x}</b><br>Pace: %{text}<extra></extra>"
        ))
        
        fig.update_layout(
            yaxis=dict(
                autorange="reversed",
                title="Pace (min/km)"
            ),
            xaxis_title="Race (42.2 km)",
            height=500,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # ADDED: Description
        st.info("""
        **Why pace matters:** Pace is the universal currency of running performance. 
        The improvement from ~6:47/km to ~5:06/km represents a transformation from a 
        "finish-focused" runner to a "performance-focused" athlete.
        """)
    
    # ADDED: Marathon data table
    st.markdown("---")
    st.subheader("📋 Marathon Summary Table")
    
    display_cols = ["Race", "Activity Date", "Official Time", "Pace (min:sec/km)", "Avg HR (bpm)", "Distance (km)"]
    display_df = marathon_df[[c for c in display_cols if c in marathon_df.columns]].copy()
    display_df["Activity Date"] = display_df["Activity Date"].dt.strftime("%b %d, %Y")
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# =============================================================================
# PAGE: TRAINING ANALYSIS
# =============================================================================
elif page == "🏋️ Training Analysis":
    st.title("🏋️ Training Analysis")
    st.markdown("*Understanding the training that built the performance*")
    
    # ADDED: Tabs for different training views
    tab1, tab2, tab3 = st.tabs(["📊 Yearly Volume", "📈 Cumulative Distance", "📅 Monthly Breakdown"])
    
    with tab1:
        # Building the Base chart (from notebook Cell 12)
        st.subheader("Building the Base")
        
        yearly_data = filtered_df.groupby("Year").agg({
            "Distance (km)": "sum",
            "Activity ID": "count"
        }).reset_index()
        yearly_data.columns = ["Year", "Distance (km)", "Runs"]
        
        # ADDED: Dual-axis chart with bars and line
        fig = go.Figure()
        
        # Bar chart for distance
        fig.add_trace(go.Bar(
            x=yearly_data["Year"],
            y=yearly_data["Distance (km)"],
            name="Distance (km)",
            marker_color=['#a5d6a7', '#66bb6a', '#43a047', '#2e7d32'],
            text=yearly_data["Distance (km)"].apply(lambda x: f"{x:,.0f} km"),
            textposition='outside'
        ))
        
        # Line for number of runs
        fig.add_trace(go.Scatter(
            x=yearly_data["Year"],
            y=yearly_data["Runs"] * 10,  # Scale for visibility
            name="Runs (scaled)",
            mode='lines+markers',
            line=dict(color='#1976D2', width=2, dash='dot'),
            marker=dict(size=10),
            yaxis='y2'
        ))
        
        fig.update_layout(
            yaxis=dict(title="Distance (km)"),
            yaxis2=dict(title="Number of Runs", overlaying='y', side='right'),
            xaxis_title="Year",
            height=500,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # ADDED: Key stats
        col1, col2, col3 = st.columns(3)
        with col1:
            growth = yearly_data["Distance (km)"].iloc[-1] / yearly_data["Distance (km)"].iloc[0]
            st.metric("Volume Growth", f"{growth:.0f}x", "2022 → 2025")
        with col2:
            total_runs = yearly_data["Runs"].sum()
            st.metric("Total Runs", f"{total_runs:,}")
        with col3:
            avg_run = filtered_df["Distance (km)"].mean()
            st.metric("Avg Run Distance", f"{avg_run:.1f} km")
    
    with tab2:
        # ADDED: Cumulative distance over time (from your planned visualizations)
        st.subheader("The Journey: Every Kilometer Counts")
        
        cumulative_df = filtered_df.sort_values("Activity Date").copy()
        cumulative_df["Cumulative Distance (km)"] = cumulative_df["Distance (km)"].cumsum()
        
        fig = go.Figure()
        
        # Area chart
        fig.add_trace(go.Scatter(
            x=cumulative_df["Activity Date"],
            y=cumulative_df["Cumulative Distance (km)"],
            fill='tozeroy',
            fillcolor='rgba(46, 125, 50, 0.2)',
            line=dict(color='#2E7D32', width=2),
            name="Cumulative Distance"
        ))
        
        # ADDED: Mark marathon points
        marathon_dates = marathon_df["Activity Date"].tolist()
        marathon_cumulative = []
        for date in marathon_dates:
            cum_dist = cumulative_df[cumulative_df["Activity Date"] <= date]["Cumulative Distance (km)"].max()
            marathon_cumulative.append(cum_dist)
        
        fig.add_trace(go.Scatter(
            x=marathon_dates,
            y=marathon_cumulative,
            mode='markers',
            marker=dict(size=15, color='#d32f2f', symbol='star'),
            name="Marathons",
            text=marathon_df["Race"],
            hovertemplate="<b>%{text}</b><br>Distance: %{y:,.0f} km<extra></extra>"
        ))
        
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Cumulative Distance (km)",
            height=500,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # ADDED: Monthly breakdown heatmap
        st.subheader("Monthly Training Volume")
        
        monthly_data = filtered_df.groupby(["Year", "Month"])["Distance (km)"].sum().reset_index()
        monthly_pivot = monthly_data.pivot(index="Year", columns="Month", values="Distance (km)").fillna(0)
        
        # Create month labels
        month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                       "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
        fig = go.Figure(data=go.Heatmap(
            z=monthly_pivot.values,
            x=month_labels[:monthly_pivot.shape[1]],
            y=monthly_pivot.index.tolist(),
            colorscale="Greens",
            text=monthly_pivot.values.round(0),
            texttemplate="%{text}",
            textfont={"size": 10},
            hovertemplate="Year: %{y}<br>Month: %{x}<br>Distance: %{z:.0f} km<extra></extra>"
        ))
        
        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Year",
            height=300,
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# PAGE: HEART RATE EFFICIENCY
# =============================================================================
elif page == "❤️ Heart Rate Efficiency":
    st.title("❤️ Heart Rate Efficiency")
    st.markdown("*Faster pace at similar heart rate = improved aerobic fitness*")
    
    # ADDED: Filter for runs with HR data
    hr_df = filtered_df[
        (filtered_df["Avg HR (bpm)"].notna()) &
        (filtered_df["Pace (min/km)"] < 10) &
        (filtered_df["Pace (min/km)"] > 3)
    ].copy()
    
    # ADDED: Scatter plot colored by year
    fig = px.scatter(
        hr_df,
        x="Avg HR (bpm)",
        y="Pace (min/km)",
        color="Year",
        color_continuous_scale="RdYlGn",
        size="Distance (km)",
        hover_data=["Activity Date", "Distance (km)", "Pace (min:sec/km)"],
        opacity=0.7
    )
    
    # ADDED: Mark marathon points
    marathon_hr = marathon_df[marathon_df["Avg HR (bpm)"].notna()].copy()
    fig.add_trace(go.Scatter(
        x=marathon_hr["Avg HR (bpm)"],
        y=marathon_hr["Pace (min/km)"],
        mode='markers',
        marker=dict(size=20, color='black', symbol='diamond'),
        name="Marathons",
        text=marathon_hr["Race"],
        hovertemplate="<b>%{text}</b><br>HR: %{x} bpm<br>Pace: %{y:.2f} min/km<extra></extra>"
    ))
    
    fig.update_layout(
        yaxis=dict(autorange="reversed", title="Pace (min/km)"),
        xaxis_title="Average Heart Rate (bpm)",
        height=600,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # ADDED: Year-over-year comparison
    st.markdown("---")
    st.subheader("Year-over-Year Efficiency")
    
    # Group by year and calculate average pace at similar HR
    yearly_efficiency = hr_df.groupby("Year").agg({
        "Pace (min/km)": "mean",
        "Avg HR (bpm)": "mean"
    }).reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            yearly_efficiency,
            x="Year",
            y="Pace (min/km)",
            color="Pace (min/km)",
            color_continuous_scale="Blues_r",
            text=yearly_efficiency["Pace (min/km)"].apply(lambda x: f"{x:.2f}")
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(
            title="Average Pace by Year",
            yaxis=dict(autorange="reversed"),
            showlegend=False,
            coloraxis_showscale=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            yearly_efficiency,
            x="Year",
            y="Avg HR (bpm)",
            color="Avg HR (bpm)",
            color_continuous_scale="Reds",
            text=yearly_efficiency["Avg HR (bpm)"].apply(lambda x: f"{x:.0f}")
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(
            title="Average Heart Rate by Year",
            showlegend=False,
            coloraxis_showscale=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.info("""
    **Key Insight:** The cluster of 2025 runs (blue) appears lower and to the right compared to 
    2022 runs (red), indicating the ability to run faster at similar heart rates — 
    a clear sign of improved cardiovascular efficiency.
    """)

# =============================================================================
# PAGE: DATA EXPLORER
# =============================================================================
elif page == "📊 Data Explorer":
    st.title("📊 Data Explorer")
    st.markdown("*Explore the raw data behind the analysis*")
    
    # ADDED: Data summary
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Activities", len(filtered_df))
    with col2:
        st.metric("Total Distance", f"{filtered_df['Distance (km)'].sum():,.0f} km")
    with col3:
        st.metric("Avg Distance", f"{filtered_df['Distance (km)'].mean():.1f} km")
    with col4:
        st.metric("Date Range", f"{filtered_df['Activity Date'].min().strftime('%b %Y')} - {filtered_df['Activity Date'].max().strftime('%b %Y')}")
    
    st.markdown("---")
    
    # ADDED: Tabs for different data views
    tab1, tab2 = st.tabs(["🏃 All Runs", "🏅 Marathons Only"])
    
    with tab1:
        st.subheader("All Running Activities")
        
        # ADDED: Column selector
        all_cols = filtered_df.columns.tolist()
        default_cols = ["Activity Date", "Activity Name", "Distance (km)", "Pace (min:sec/km)", 
                       "Moving Time (H:M:S)", "Avg HR (bpm)", "Elevation Gain (m)"]
        selected_cols = st.multiselect(
            "Select columns to display",
            options=all_cols,
            default=[c for c in default_cols if c in all_cols]
        )
        
        if selected_cols:
            display_df = filtered_df[selected_cols].copy()
            if "Activity Date" in selected_cols:
                display_df["Activity Date"] = display_df["Activity Date"].dt.strftime("%Y-%m-%d")
            st.dataframe(display_df.sort_values("Activity Date" if "Activity Date" in selected_cols else selected_cols[0], ascending=False), 
                        use_container_width=True, hide_index=True)
        
        # ADDED: Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv,
            file_name="running_data.csv",
            mime="text/csv"
        )
    
    with tab2:
        st.subheader("Marathon Data")
        
        display_cols = ["Race", "Activity Date", "Official Time", "Pace (min:sec/km)", 
                       "Avg HR (bpm)", "Distance (km)", "Elevation Gain (m)"]
        display_df = marathon_df[[c for c in display_cols if c in marathon_df.columns]].copy()
        display_df["Activity Date"] = display_df["Activity Date"].dt.strftime("%Y-%m-%d")
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)

# =============================================================================
# PAGE: INSIGHTS
# =============================================================================
elif page == "💡 Insights":
    st.title("💡 Key Insights")
    st.markdown("*What the data reveals about the 80-minute journey*")
    
    # ADDED: Insight cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%); 
                    padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;
                    border-left: 4px solid #2E7D32;">
            <h3 style="color: #1B5E20; margin-top: 0;">📈 7x Volume Increase</h3>
            <p>Training volume grew from 246 km (2022) to 1,712 km (2025), directly 
            correlating with performance gains.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%); 
                    padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;
                    border-left: 4px solid #1976D2;">
            <h3 style="color: #0D47A1; margin-top: 0;">❤️ Improved Aerobic Efficiency</h3>
            <p>Running ~1:40/km faster at similar heart rates compared to 2022 — 
            evidence of significant cardiovascular adaptation.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%); 
                    padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;
                    border-left: 4px solid #F57C00;">
            <h3 style="color: #E65100; margin-top: 0;">🎯 Consistent Progression</h3>
            <p>Every single marathon was faster than the previous one — no setbacks 
            across 6 races over 3 years.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #F3E5F5 0%, #E1BEE7 100%); 
                    padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;
                    border-left: 4px solid #7B1FA2;">
            <h3 style="color: #4A148C; margin-top: 0;">🏆 80-Minute Improvement</h3>
            <p>From 4:46:07 to 3:26:00 — a 28% reduction in finish time through 
            dedicated, progressive training.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ADDED: Training-Performance correlation table (from your descriptions)
    st.subheader("📊 Training-Performance Correlation")
    
    correlation_data = pd.DataFrame({
        "Year": [2022, 2023, 2024, 2025],
        "Volume (km)": [246, 682, 837, 1712],
        "Best Marathon": ["4:46:07", "4:16:58", "3:47:47", "3:26:00"],
        "Improvement": ["-", "29 min", "29 min", "22 min"],
        "Insight": [
            "Minimal base, first marathon",
            "2.7x volume increase",
            "Consistent building",
            "2x volume jump → breakthrough"
        ]
    })
    
    st.dataframe(correlation_data, use_container_width=True, hide_index=True)
    
    # ADDED: What's next section
    st.markdown("---")
    st.subheader("🚀 What's Next?")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current PB", "3:26:00")
    with col2:
        st.metric("Next Target", "3:14:59", delta="-11 min")
    with col3:
        st.metric("Ultimate Goal", "Sub-3:00", delta="Boston Qualifier")

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>Built with ❤️ using Streamlit • Data from Strava</p>
    <p>The 80-Minute Journey: A Data-Driven Analysis of Marathon Progression</p>
</div>
""", unsafe_allow_html=True)
