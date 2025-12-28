import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Page configuration for a wide layout
st.set_page_config(
    page_title="The Sub-3:30 Protocol",  # Browser tab title
    page_icon="⭐",                       # Browser tab icon
    layout="wide"                         # Use full width of the page
)

# ===== CURATED CINEMATIC PALETTE: "Electric Dreams" =====
# Cyberpunk-inspired palette with electric blues and neon purples
# Optimized for visual impact, readability, and cinematic depth
#
# Color Philosophy:
# - Electric blue and neon purple for cyberpunk aesthetic
# - Deep purples and blues for immersive backgrounds
# - Cyan accents for that iconic cyberpunk glow
# - High contrast for cinematic punch while maintaining readability
#
colors = ["#00d9ff", "#b957ff", "#1a0d2e", "#0a0420", "#e0f4ff"]
# [0] Electric Cyan   - Primary highlights, titles, electric accents
# [1] Neon Purple     - Data lines, charts, secondary highlights
# [2] Deep Violet     - Containers, expander backgrounds
# [3] Dark Abyss      - Secondary backgrounds, depth layers
# [4] Ice Blue        - Text, borders, high readability

# ===== ARCHIVED COLOR SCHEMES =====
# Blade Runner 2049 color palette
# colors =   ["#a30502", "#f78b04", "#2b1718", "#153a42","#027f93" ]

# Cyberpunk
# colors = ["#FF6F61", "#FFB400", "#00FFFF", "#008B8B", "#00CED1"]

# Cyberpunk 2
# colors = ["#F887FF", "#DE004E", "#860029", "#321450", "#29132E"]

# Cyberpunk 3
# colors = ["#ff6e27", "#fbf665", "#73fffe", "#6287f8", "#383e65"]

# Cyberpunk 4
#colors = ["#63345E", "#ac61b9", "#b7c1de", "#0b468c", "#092047"]

# Cyberpunk 5
# colors = ["#a0ffe3", "#65dc98", "#8d8980", "#575267", "#222035" ]

# Cyberpunk 6 (Best one yet)
#colors = ["#8f704b", "#daae6d", "#89e3f6", "#4d9e9b", "#44786a"]

# Cyberpunk 7
# colors = ["#ff184c", "#ff577d", "#ffccdc", "#0a9cf5", "#003062"]

# Electric Dreams Custom CSS Styling
st.markdown(f"""
    <style>
    /* Main background - pure black for maximum contrast */
    .stApp {{
        background-color: #000000;
        color: {colors[4]};
    }}

    /* Title styling with electric cyan glow */
    h1 {{
        color: {colors[0]} !important;
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        text-shadow: 0 0 30px {colors[0]}80, 0 0 50px {colors[0]}50, 0 0 70px {colors[0]}30;
    }}

    /* Subtitle styling - cyan with stronger glow */
    h2 {{
        color: {colors[0]} !important;
        font-family: 'Arial', sans-serif;
        text-shadow: 0 0 25px {colors[0]}70, 0 0 40px {colors[0]}40;
    }}

    h3 {{
        color: {colors[4]} !important;
        font-family: 'Arial', sans-serif;
        text-shadow: 0 0 15px {colors[4]}40;
    }}

    h4 {{
        color: {colors[1]} !important;
        font-family: 'Arial', sans-serif;
        font-weight: 600;
        text-shadow: 0 0 20px {colors[1]}60, 0 0 35px {colors[1]}30;
    }}

    /* Expander styling with neon borders */
    .streamlit-expanderHeader {{
        background-color: {colors[2]} !important;
        color: {colors[0]} !important;
        border: 2px solid {colors[1]} !important;
        border-radius: 4px;
        box-shadow: 0 0 15px {colors[1]}40, inset 0 0 10px {colors[1]}20;
    }}

    .streamlit-expanderContent {{
        background-color: {colors[3]} !important;
        border: 1px solid {colors[1]}80 !important;
        color: {colors[4]} !important;
        box-shadow: inset 0 0 20px {colors[2]}60;
    }}

    /* Markdown text - ice blue for high contrast readability */
    p, li, .stMarkdown {{
        color: {colors[4]} !important;
    }}

    /* Table styling with cyberpunk borders */
    table {{
        background-color: {colors[3]} !important;
        color: {colors[4]} !important;
        border: 1px solid {colors[1]}60 !important;
    }}

    table th {{
        background-color: {colors[2]} !important;
        color: {colors[0]} !important;
        border: 1px solid {colors[1]} !important;
        font-weight: bold;
        text-shadow: 0 0 10px {colors[0]}50;
    }}

    table td {{
        border: 1px solid {colors[2]} !important;
        color: {colors[4]} !important;
    }}

    /* Horizontal rule with electric gradient glow */
    hr {{
        border: none;
        height: 3px;
        background: linear-gradient(90deg, {colors[0]}, {colors[1]}, {colors[0]});
        box-shadow: 0 0 20px {colors[0]}70, 0 0 30px {colors[1]}60, 0 0 40px {colors[0]}40;
        margin: 2rem 0;
    }}

    /* Links with electric cyan highlights */
    a {{
        color: {colors[0]} !important;
        text-shadow: 0 0 12px {colors[0]}60;
        transition: all 0.3s ease;
    }}

    a:hover {{
        color: {colors[1]} !important;
        text-shadow: 0 0 18px {colors[1]}80, 0 0 25px {colors[1]}50;
    }}

    /* Sidebar styling with cyberpunk theme */
    [data-testid="stSidebar"] {{
        background-color: {colors[3]} !important;
        border-right: 2px solid {colors[1]} !important;
        box-shadow: 0 0 30px {colors[1]}30;
    }}

    /* Sidebar title styling */
    [data-testid="stSidebar"] h1 {{
        color: {colors[0]} !important;
        text-shadow: 0 0 25px {colors[0]}70, 0 0 40px {colors[0]}40;
    }}

    /* Sidebar radio buttons */
    [data-testid="stSidebar"] .stRadio > label {{
        color: {colors[4]} !important;
        font-size: 1.1rem;
    }}

    /* Radio button options */
    [data-testid="stSidebar"] [role="radiogroup"] label {{
        color: {colors[4]} !important;
        padding: 0.75rem 1rem;
        border-radius: 4px;
        transition: all 0.3s ease;
    }}

    /* Radio button hover effect */
    [data-testid="stSidebar"] [role="radiogroup"] label:hover {{
        background-color: {colors[2]} !important;
        border-left: 3px solid {colors[0]};
        box-shadow: 0 0 15px {colors[0]}30;
    }}

    /* Selected radio button */
    [data-testid="stSidebar"] [role="radiogroup"] label[data-baseweb="radio"] {{
        background-color: {colors[2]} !important;
        border-left: 3px solid {colors[1]};
        box-shadow: 0 0 20px {colors[1]}40, inset 0 0 10px {colors[1]}20;
        color: {colors[0]} !important;
    }}

    /* Radio button circle */
    [data-testid="stSidebar"] [data-baseweb="radio"] > div {{
        border-color: {colors[1]} !important;
    }}

    /* Radio button checked circle */
    [data-testid="stSidebar"] [data-baseweb="radio"] > div[data-checked="true"] {{
        background-color: {colors[1]} !important;
        box-shadow: 0 0 10px {colors[1]}60;
    }}

    /* Sidebar horizontal rules */
    [data-testid="stSidebar"] hr {{
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, {colors[1]}, transparent);
        box-shadow: 0 0 15px {colors[1]}50;
    }}
    </style>
    """, unsafe_allow_html=True)


# Sidebar Navigation
with st.sidebar:
    st.title("The Sub-3:30 Protocol")
    st.markdown("<hr>", unsafe_allow_html=True)

    # Navigation Menu
    page = st.radio(
        "Navigation",
        ["Home", "Marathon Performance", "Heart Rate Analysis"],
        label_visibility="collapsed"
    )

    st.markdown("<hr>", unsafe_allow_html=True)

# Load datasets
activities_df = pd.read_csv("activities_dataset.csv")
challenges_df = pd.read_csv("global_challenges.csv")

# Prepare Heart Rate Data
# Filter out race distances (marathons > 40km) and ensure HR data exists
df_hr = activities_df[
    (activities_df['Activity Type'] == 'Run') &
    (activities_df['Average Heart Rate'].notna()) &
    (activities_df['Distance'] <= 40)
].copy()

# Parse dates and add Year column
df_hr['Activity Date'] = pd.to_datetime(df_hr['Activity Date'], format="%b %d, %Y, %I:%M:%S %p")
df_hr['Year'] = df_hr['Activity Date'].dt.year

# Calculate pace
df_hr['Pace (min/km)'] = 1000 / (df_hr['Average Speed'] * 60)
df_hr = df_hr.rename(columns={'Average Heart Rate': 'Avg HR (bpm)'})

# ===== PAGE: HOME =====
if page == "Home":
    st.markdown(
        """
        <h1 style = "text-align: center;">The Sub-3:30 Protocol</h1>
        <h3 style = "text-align: center;">A Data-Driven Journey from 4:46 to 3:26 Marathon</h3>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown(f"""
    #### Welcome to The Sub-3:30 Protocol

    This dashboard chronicles a remarkable 3-year journey of marathon progression, showcasing how
    consistent training, data-driven decisions, and unwavering dedication transformed a Sub 5-hour marathoner
    into a sub-3:30 athlete.
                
    #### Project Overview
    
    This project analyzes **347 running activities over 3.5 years**, documenting the progression from a first-time marathoner (4:46:07 at Royal Victoria Marathon 2022) 
    to a sub-3:30 finisher (3:26:00 at Royal Victoria Marathon 2025) — an improvement of **80 minutes** across 6 marathon races.
    The analysis explores how training patterns, physiological adaptations, and race execution evolved to produce consistent performance gains at two 
    recurring races: the **Royal Victoria Marathon** (4 finishes) and **BMO Vancouver Marathon** (2 finishes).

    #### The Journey at a Glance

    - **6 Marathons** completed between 2022-2025
    - **80 minutes** improvement in finish time
    - **3400 Km+** logged across 3 years
    - **Sub-5 Hour** debut at RVM 2022 (4:46:07)
    - **Sub-3:30** achieved at RVM 2025 (3:26:00)

    #### Key Insights

    Navigate through the sections to explore:

    - **Marathon Performance**: Track race times, pace evolution, and annual running volume
    - **Heart Rate Analysis**: Discover how aerobic efficiency improved year-over-year

    Use the navigation menu on the left to dive deeper into the data.
    """)


# PAGE: MARATHON PERFORMANCE 
elif page == "Marathon Performance":
    st.title("Marathon Performance Metrics")
    st.markdown("*Tracking progression across all 6 marathon races and annual training volume*")

    st.markdown("<hr>", unsafe_allow_html=True)

    # Marathon Progression Timeline

    st.markdown("#### Marathon Progression Timeline")
    st.markdown("*Finish time improvements across all 6 marathon races*")

    # Define the data for the chart
    races = ["RVM 2022", "BMO 2023", "RVM 2023", "RVM 2024", "BMO 2025", "RVM 2025"]
    times_minutes = [286.12, 265.80, 256.97, 227.78, 217.38, 206.00]
    times_labels = ["4:46:07", "4:25:48", "4:16:58", "3:47:47", "3:37:23", "3:26:00"]

    # Create Plotly figure
    fig1 = go.Figure()

    # Add line trace with markers (Electric Cyan with Neon Purple accents)
    fig1.add_trace(go.Scatter(
        x=races,
        y=times_minutes,
        mode='lines+markers',
        marker=dict(size=12, color=colors[0], line=dict(color=colors[1], width=2)),
        line=dict(width=3, color=colors[0], shape='spline'),
        hovertemplate="<b>%{x}</b><br>Time: %{customdata}<extra></extra>",
        customdata=times_labels
    ))

    # Update layout with inverted y-axis and H:M:S tick labels
    fig1.update_layout(
        xaxis=dict(
            title=dict(text="Race", font=dict(size=14, color=colors[0], family='Arial')),
            tickfont=dict(size=12, color=colors[4]),
            showgrid=True,
            gridcolor=f'rgba(0, 217, 255, 0.15)',
            showline=True,
            linecolor=colors[1],
            linewidth=1
        ),
        yaxis=dict(
            title=dict(text="Finish Time (H:M:S)", font=dict(size=14, color=colors[0], family='Arial')),
            tickvals=times_minutes,
            ticktext=times_labels,
            autorange="reversed",
            tickfont=dict(size=12, color=colors[4]),
            showgrid=True,
            gridcolor=f'rgba(0, 217, 255, 0.15)',
            showline=True,
            linecolor=colors[1],
            linewidth=1
        ),
        height=600,
        margin=dict(l=70, r=30, t=30, b=60),
        hovermode='x unified',
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(family='Arial', color=colors[0]),
        hoverlabel=dict(
            bgcolor="#0d1f26",
            font_size=13,
            font_family='Arial',
            bordercolor=colors[1],
        font_color=colors[4]
        )
    )

    st.plotly_chart(fig1, use_container_width=True)

    # Pace Evolution Curve (NEW - Green color, right column)

    st.markdown("#### Pace Evolution Curve")
    st.markdown("*Average pace progression from 6:30/km to 4:50/km*")

    # Define pace data for the chart
    races = ["RVM 2022", "BMO 2023", "RVM 2023", "RVM 2024", "BMO 2025", "RVM 2025"]
    pace_decimal = [6.50, 6.22, 6.07, 5.37, 5.12, 4.83]  # Pace in decimal minutes (e.g., 6:30 = 6.5)
    pace_labels = ["6:30", "6:13", "6:04", "5:22", "5:07", "4:50"]  # M:SS format labels

    # Create Plotly figure for pace chart
    fig2 = go.Figure()

    # Add line trace with markers (Neon Purple with depth)
    fig2.add_trace(go.Scatter(
        x=races,
        y=pace_decimal,
        mode='lines+markers',
        marker=dict(size=12, color=colors[1], line=dict(color=colors[0], width=2)),
        line=dict(width=3, color=colors[1], shape='spline'),
        hovertemplate="<b>%{x}</b><br>Pace: %{customdata}/km<extra></extra>",
        customdata=pace_labels
    ))

    # Update layout with inverted y-axis and pace labels
    fig2.update_layout(
        xaxis=dict(
            title=dict(text="Race", font=dict(size=14, color=colors[0], family='Arial')),
            tickfont=dict(size=12, color=colors[4]),
            showgrid=True,
            gridcolor=f'rgba(0, 217, 255, 0.15)',
            showline=True,
            linecolor=colors[1],
            linewidth=1
        ),
        yaxis=dict(
            title=dict(text="Pace (min/km)", font=dict(size=14, color=colors[0], family='Arial')),
            tickvals=pace_decimal,
            ticktext=pace_labels,
            autorange="reversed",
            tickfont=dict(size=12, color=colors[4]),
            showgrid=True,
            gridcolor=f'rgba(0, 217, 255, 0.15)',
            showline=True,
            linecolor=colors[1],
            linewidth=1
        ),
        height=600,
        margin=dict(l=70, r=30, t=30, b=60),
        hovermode='x unified',
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(family='Arial', color=colors[0]),
        hoverlabel=dict(
            bgcolor="#0d1f26",
            font_size=13,
            font_family='Arial',
            bordercolor=colors[1],
        font_color=colors[4]
        )
    )

    # Display the pace chart
    st.plotly_chart(fig2, use_container_width=True)

    
    # Building the Base
    st.markdown("#### Annual Running Volume")
    st.markdown("*Total running distance per year*")

    # Calculate yearly totals
    yearly_data = activities_df[activities_df['Activity Type'] == 'Run'].copy()
    yearly_data['Activity Date'] = pd.to_datetime(yearly_data['Activity Date'], format="%b %d, %Y, %I:%M:%S %p")
    yearly_data['Year'] = yearly_data['Activity Date'].dt.year

    yearly_summary = yearly_data.groupby('Year').agg({
        'Distance': 'sum',
        'Activity ID': 'count'
    }).reset_index()
    yearly_summary.columns = ['Year', 'Total Distance (km)', 'Number of Runs']

    years = yearly_summary['Year'].astype(int).tolist()
    distances = yearly_summary['Total Distance (km)'].tolist()
    run_counts = yearly_summary['Number of Runs'].tolist()

    # Color Gradient (Electric Dreams - from purple to cyan)
    bar_colors = ['#8b3fff', '#b957ff', '#00a8ff', '#00d9ff']

    # Create Plotly figure
    fig3 = go.Figure()

    # Add bar trace
    fig3.add_trace(go.Bar(
        x=years,
        y=distances,
        marker=dict(
            color=bar_colors
        ),
        text=[f"{dist:.0f} km" for dist, runs in zip(distances, run_counts)],
        textposition='inside',
        insidetextanchor="middle",
        textfont=dict(size=11, color="#000000", family='Arial', weight='bold'),
        hovertemplate="<b>%{x}</b><br>Distance: %{y:.0f} km<br>Runs: %{customdata}<extra></extra>",
        customdata=run_counts
    ))

    # Update layout
    fig3.update_layout(
        xaxis=dict(
            title=dict(text="Year", font=dict(size=14, color=colors[0], family='Arial')),
            tickfont=dict(size=12, color=colors[4]),
            showgrid=False,
            showline=True,
            linecolor=colors[1],
            linewidth=1
        ),
        yaxis=dict(
            title=dict(text="Total Distance (km)", font=dict(size=14, color=colors[0], family='Arial')),
            tickfont=dict(size=12, color=colors[4]),
            showgrid=True,
            gridcolor=f'rgba(0, 217, 255, 0.15)',
            showline=True,
            linecolor=colors[1],
            linewidth=1
        ),
        height=600,
        margin=dict(l=70, r=30, t=30, b=60),
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(family='Arial', color=colors[0]),
        hoverlabel=dict(
            bgcolor="#0d1f26",
            font_size=13,
            font_family='Arial',
            bordercolor=colors[1],
            font_color=colors[4]
        ),
        showlegend=False
    )

    st.plotly_chart(fig3, use_container_width=True)


# ===== PAGE: HEART RATE ANALYSIS =====
elif page == "Heart Rate Analysis":
    st.title("Heart Rate Efficiency Analysis")
    st.markdown("*Pace vs HR by Year - Training runs only (excludes marathon races >40km)*")

    st.markdown("<hr>", unsafe_allow_html=True)

    # Create 2x2 grid for year-by-year analysis
    years = sorted(df_hr["Year"].unique())

    # Get global min/max for consistent color scale across all years
    hr_min = df_hr["Avg HR (bpm)"].min()
    hr_max = df_hr["Avg HR (bpm)"].max()

    # Create rows for 2x2 layout
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)

    columns = [row1_col1, row1_col2, row2_col1, row2_col2]

    for i, year in enumerate(years):
        with columns[i]:
            # Year title
            st.markdown(f"### {int(year)}")

            # Filter data for this year
            subset = df_hr[df_hr["Year"] == year].copy()

            # Create scatter plot
            fig_hr = go.Figure()

            fig_hr.add_trace(go.Scatter(
                x=subset["Pace (min/km)"],
                y=subset["Avg HR (bpm)"],
                mode='markers',
                marker=dict(
                    size=10,
                    color=subset["Avg HR (bpm)"],
                    colorscale=[
                        [0.0, '#0099ff'],   # Deep Blue (low HR)
                        [0.25, colors[0]],  # Electric Cyan
                        [0.5, '#00ff9f'],   # Cyan-Green
                        [0.75, '#b957ff'],  # Neon Purple
                        [1.0, '#ff00ff']    # Magenta (high HR)
                    ],
                    cmin=hr_min,
                    cmax=hr_max,
                    showscale=True,
                    colorbar=dict(
                        title=dict(
                            text="Avg HR<br>(bpm)",
                            font=dict(size=11, color=colors[0], family='Arial')
                        ),
                        titleside="right",
                        thickness=12,
                        len=0.85,
                        x=1.02,
                        xpad=5,
                        tickfont=dict(size=10, color=colors[4]),
                        outlinewidth=1,
                        outlinecolor=colors[1],
                        bgcolor="#0d1f26"
                    ),
                    line=dict(color=colors[1], width=1),
                    opacity=0.85
                ),
                hovertemplate="<b>Pace:</b> %{x:.2f} min/km<br><b>HR:</b> %{y:.0f} bpm<extra></extra>"
            ))

            # Update layout with Neo-Tokyo styling
            fig_hr.update_layout(
                xaxis=dict(
                    title=dict(
                        text="Pace (min/km)",
                        font=dict(size=12, color=colors[0], family='Arial')
                    ),
                    tickfont=dict(size=10, color=colors[4]),
                    showgrid=True,
                    gridcolor=f'rgba(185, 87, 255, 0.15)',
                    gridwidth=1,
                    showline=True,
                    linecolor=colors[1],
                    linewidth=1.5,
                    autorange="reversed",
                    zeroline=False
                ),
                yaxis=dict(
                    title=dict(
                        text="Avg HR (bpm)",
                        font=dict(size=12, color=colors[0], family='Arial')
                    ),
                    tickfont=dict(size=10, color=colors[4]),
                    showgrid=True,
                    gridcolor=f'rgba(185, 87, 255, 0.15)',
                    gridwidth=1,
                    showline=True,
                    linecolor=colors[1],
                    linewidth=1.5,
                    zeroline=False
                ),
                height=380,
                margin=dict(l=70, r=90, t=20, b=60),
                plot_bgcolor="black",
                paper_bgcolor="black",
                font=dict(family='Arial', color=colors[0]),
                hoverlabel=dict(
                    bgcolor="#0d1f26",
                    font_size=11,
                    font_family='Arial',
                    bordercolor=colors[1],
                    font_color=colors[4]
                )
            )

            st.plotly_chart(fig_hr, use_container_width=True)


# Footer (displayed on all pages)
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    f"""
    <div style='text-align: center; color: {colors[4]}; font-size: 0.85rem; text-shadow: 0 0 8px {colors[4]}30;'>
        Built by <strong style='color: {colors[0]};'>Aditya Padmarajan</strong> • Data from Strava • 2022-2025
    </div>
    """,
    unsafe_allow_html=True
)
