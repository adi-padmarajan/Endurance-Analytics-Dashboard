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

colors = ["#00d9ff", "#b957ff", "#1a0d2e", "#0a0420", "#e0f4ff"]

# Load external CSS file
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css("styles.css")


# Sidebar Navigation
with st.sidebar:
    st.title("The Sub-3:30 Protocol")
    st.markdown("<hr>", unsafe_allow_html=True)

    # Navigation Menu
    page = st.radio(
        "Navigation",
        ["Home", "Marathon Performance Metrics", "Training Metrics", "Heart Rate Analysis"],
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
        <h3 style = "text-align: center;">A Data-Driven Journey from a Sub 5-hour to a Sub 3:30 Marathon</h3>
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
    - **3400 Km+** logged across 3.5 years
    - **Sub-5 Hour** debut at RVM 2022 (4:46:07)
    - **Sub-3:30** achieved at RVM 2025 (3:26:00)

    #### Key Insights

    Navigate through the sections to explore:

    - **Marathon Performance**: Track race times, pace evolution, and annual running volume
    - **Heart Rate Analysis**: Discover how aerobic efficiency improved year-over-year

    Use the navigation menu on the left to dive deeper into the data.
    """)


# PAGE: MARATHON PERFORMANCE 
elif page == "Marathon Performance Metrics":
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

elif page == "Training Metrics":
    st.title("Training Metrics")
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
