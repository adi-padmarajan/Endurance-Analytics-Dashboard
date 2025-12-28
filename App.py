import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from gpx_utils import parse_activity_file

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
        ["Home", "Marathon Performance Metrics", "Training Metrics", "Heart Rate Analysis", "Route Visualization"],
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
        <h3 style = "text-align: center;">A Data-Driven Journey from a Sub 5:00 to a Sub 3:30 Marathon</h3>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    # ===== EXECUTIVE SUMMARY - KEY METRICS CARDS =====
    st.markdown("### Executive Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div style='text-align: center; padding: 1.5rem; background: linear-gradient(135deg, {colors[3]} 0%, {colors[2]} 100%);
        border: 2px solid {colors[1]}; border-radius: 10px; box-shadow: 0 0 20px rgba(185, 87, 255, 0.3);'>
            <h2 style='color: {colors[0]}; margin: 0; font-size: 2.5rem; text-shadow: 0 0 20px rgba(0, 217, 255, 0.5);'>80</h2>
            <p style='color: {colors[4]}; margin: 0; font-size: 0.9rem; margin-top: 0.5rem;'>Minutes Improved</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style='text-align: center; padding: 1.5rem; background: linear-gradient(135deg, {colors[3]} 0%, {colors[2]} 100%);
        border: 2px solid {colors[1]}; border-radius: 10px; box-shadow: 0 0 20px rgba(185, 87, 255, 0.3);'>
            <h2 style='color: {colors[0]}; margin: 0; font-size: 2.5rem; text-shadow: 0 0 20px rgba(0, 217, 255, 0.5);'>347</h2>
            <p style='color: {colors[4]}; margin: 0; font-size: 0.9rem; margin-top: 0.5rem;'>Training Runs</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style='text-align: center; padding: 1.5rem; background: linear-gradient(135deg, {colors[3]} 0%, {colors[2]} 100%);
        border: 2px solid {colors[1]}; border-radius: 10px; box-shadow: 0 0 20px rgba(185, 87, 255, 0.3);'>
            <h2 style='color: {colors[0]}; margin: 0; font-size: 2.5rem; text-shadow: 0 0 20px rgba(0, 217, 255, 0.5);'>3,400+</h2>
            <p style='color: {colors[4]}; margin: 0; font-size: 0.9rem; margin-top: 0.5rem;'>Kilometers Logged</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div style='text-align: center; padding: 1.5rem; background: linear-gradient(135deg, {colors[3]} 0%, {colors[2]} 100%);
        border: 2px solid {colors[1]}; border-radius: 10px; box-shadow: 0 0 20px rgba(185, 87, 255, 0.3);'>
            <h2 style='color: {colors[0]}; margin: 0; font-size: 2.5rem; text-shadow: 0 0 20px rgba(0, 217, 255, 0.5);'>3.5</h2>
            <p style='color: {colors[4]}; margin: 0; font-size: 0.9rem; margin-top: 0.5rem;'>Years of Training</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ===== PROJECT OVERVIEW =====
    st.markdown("### Project Overview")

    st.markdown(f"""
    This comprehensive data analytics project chronicles a remarkable transformation in marathon performance,
    combining **endurance sports science**, **data visualization**, and **performance analytics** to document
    the journey from a recreational runner to a competitive marathoner.

    The analysis leverages **347 GPS-tracked running activities** spanning 3.5 years (2022-2025), examining the
    physiological, training, and performance adaptations that enabled an **80-minute improvement** across 6 marathon races.
    """)

    st.markdown("<br>", unsafe_allow_html=True)

    # ===== RESEARCH METHODOLOGY =====
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown("### Research Methodology")
        st.markdown(f"""
        #### Data Sources
        - **Primary Dataset**: Strava activity exports (CSV/GPX/TCX/FIT files)
        - **Activity Count**: 347 running sessions
        - **Temporal Range**: 2022 - 2025
        - **Geographic Scope**: Victoria & Vancouver, BC, Canada

        #### Analytical Approach
        - **Performance Metrics**: Race time, pace evolution, split analysis
        - **Training Volume**: Annual distance, frequency patterns
        - **Physiological Data**: Heart rate efficiency, aerobic adaptation
        - **Geospatial Analysis**: Route visualization, elevation profiles

        #### Key Race Events
        - **Royal Victoria Marathon**: 4 finishes (2022, 2023, 2024, 2025)
        - **BMO Vancouver Marathon**: 2 finishes (2023, 2025)
        """)

    with col_right:
        st.markdown("### Performance Timeline")

        # Mini visualization of race progression
        races_mini = ["RVM 2022", "BMO 2023", "RVM 2023", "RVM 2024", "BMO 2025", "RVM 2025"]
        times_mini = [286.12, 265.80, 256.97, 227.78, 217.38, 206.00]
        times_labels_mini = ["4:46:07", "4:25:48", "4:16:58", "3:47:47", "3:37:23", "3:26:00"]

        fig_mini = go.Figure()

        fig_mini.add_trace(go.Scatter(
            x=races_mini,
            y=times_mini,
            mode='lines+markers',
            marker=dict(size=10, color=colors[0], line=dict(color=colors[1], width=2)),
            line=dict(width=3, color=colors[0], shape='spline'),
            hovertemplate="<b>%{x}</b><br>Time: %{customdata}<extra></extra>",
            customdata=times_labels_mini
        ))

        fig_mini.update_layout(
            xaxis=dict(
                tickfont=dict(size=10, color=colors[4]),
                showgrid=True,
                gridcolor=f'rgba(0, 217, 255, 0.15)',
            ),
            yaxis=dict(
                tickvals=times_mini,
                ticktext=times_labels_mini,
                autorange="reversed",
                tickfont=dict(size=10, color=colors[4]),
                showgrid=True,
                gridcolor=f'rgba(0, 217, 255, 0.15)',
            ),
            height=400,
            margin=dict(l=70, r=30, t=10, b=60),
            plot_bgcolor="black",
            paper_bgcolor="black",
            font=dict(family='Arial', color=colors[0]),
            showlegend=False
        )

        st.plotly_chart(fig_mini, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ===== KEY FINDINGS =====
    st.markdown("### Key Research Findings")

    findings_col1, findings_col2 = st.columns(2)

    with findings_col1:
        st.markdown(f"""
        #### Performance Adaptations

        **Marathon Time Improvement**
        - First marathon (RVM 2022): 4:46:07 (6:47/km pace)
        - Latest marathon (RVM 2025): 3:26:00 (4:52/km pace)
        - Total improvement: 80 minutes (27.9% faster)

        **Pace Evolution**
        - Average pace improved from 6:30/km to 4:50/km
        - Consistent sub-5:00/km pacing achieved by 2024
        - Negative splits mastered in final races

        **Training Volume Progression**
        - 2022: Lower baseline volume (building phase)
        - 2023: Volume increase with consistency focus
        - 2024-2025: Peak training years with 1000+ km annually
        """)

    with findings_col2:
        st.markdown(f"""
        #### Physiological Adaptations

        **Aerobic Efficiency Gains**
        - Heart rate efficiency improved year-over-year
        - Same pace achieved at lower heart rates over time
        - Enhanced lactate threshold and VO2max indicators

        **Training Consistency**
        - 347 runs completed over 3.5 years
        - Average of 99 runs per year
        - Maintained injury-free progression through smart periodization

        **Race-Specific Preparation**
        - Course familiarity advantage at RVM (4 races)
        - Consistent improvement at same venue demonstrates adaptation
        - Strategic race selection for optimal progression
        """)

    st.markdown("<br>", unsafe_allow_html=True)

    # ===== SCIENTIFIC CONTEXT =====
    st.markdown("### Scientific Context & Training Principles")

    st.markdown(f"""
    This project demonstrates several well-established principles from exercise physiology and endurance training:

    **Aerobic Base Development**
    The foundation of marathon performance lies in building aerobic capacity through consistent, moderate-intensity training.
    The heart rate analysis reveals progressive improvements in aerobic efficiency—maintaining faster paces at lower heart rates
    over successive years.

    **Progressive Overload**
    Annual training volume increased systematically, allowing for physiological adaptations while minimizing injury risk.
    The progression from recreational to competitive performance exemplifies proper application of progressive overload principles.

    **Specificity & Course Familiarity**
    Multiple races on the same course (Royal Victoria Marathon) provided controlled conditions to measure true performance gains,
    eliminating course difficulty as a confounding variable.

    **Data-Driven Training**
    Leveraging GPS tracking, heart rate monitoring, and performance analytics enabled evidence-based training decisions,
    optimizing the progression toward the sub-3:30 goal.
    """)

    st.markdown("<br>", unsafe_allow_html=True)

    # ===== DASHBOARD NAVIGATION GUIDE =====
    st.markdown("### Dashboard Navigation")

    nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)

    with nav_col1:
        st.markdown(f"""
        <div style='padding: 1.2rem; background-color: {colors[3]}; border-left: 4px solid {colors[0]};
        border-radius: 5px; box-shadow: 0 0 15px rgba(0, 217, 255, 0.2);'>
            <h4 style='color: {colors[0]}; margin: 0;'> Marathon Performance </h4>
            <p style='color: {colors[4]}; font-size: 0.85rem; margin-top: 0.5rem;'>
            Track race-by-race improvements, pace evolution curves, and competitive performance metrics across all 6 marathons.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with nav_col2:
        st.markdown(f"""
        <div style='padding: 1.2rem; background-color: {colors[3]}; border-left: 4px solid {colors[1]};
        border-radius: 5px; box-shadow: 0 0 15px rgba(185, 87, 255, 0.2);'>
            <h4 style='color: {colors[1]}; margin: 0;'> Training Metrics </h4>
            <p style='color: {colors[4]}; font-size: 0.85rem; margin-top: 0.5rem;'>
            Explore annual training volume, consistency patterns, and how progressive overload was applied year-over-year.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with nav_col3:
        st.markdown(f"""
        <div style='padding: 1.2rem; background-color: {colors[3]}; border-left: 4px solid #00ff9f;
        border-radius: 5px; box-shadow: 0 0 15px rgba(0, 255, 159, 0.2);'>
            <h4 style='color: #00ff9f; margin: 0;'> Heart Rate Analysis </h4>
            <p style='color: {colors[4]}; font-size: 0.85rem; margin-top: 0.5rem;'>
            Analyze aerobic efficiency improvements through pace-HR relationships and cardiovascular adaptations over time.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with nav_col4:
        st.markdown(f"""
        <div style='padding: 1.2rem; background-color: {colors[3]}; border-left: 4px solid #51cf66;
        border-radius: 5px; box-shadow: 0 0 15px rgba(81, 207, 102, 0.2);'>
            <h4 style='color: #51cf66; margin: 0;'> Route Visualization</h4>
            <p style='color: {colors[4]}; font-size: 0.85rem; margin-top: 0.5rem;'>
            Interactive GPS route maps of marathon courses, showcasing the terrain and race-day execution.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ===== TECHNICAL IMPLEMENTATION =====
    st.markdown("### Technical Implementation")

    tech_col1, tech_col2 = st.columns(2)

    with tech_col1:
        st.markdown(f"""
        #### Data Processing & Analysis
        - **Python**: Core data processing and analysis
        - **Pandas & NumPy**: Data manipulation and statistical analysis
        - **GPX/TCX/FIT Parsing**: Custom parsers for GPS activity files
        - **Geospatial Analysis**: Haversine distance calculations, route processing
        """)

    with tech_col2:
        st.markdown(f"""
        #### Visualization & Dashboard
        - **Streamlit**: Interactive web dashboard framework
        - **Plotly**: Dynamic, interactive data visualizations
        - **Custom CSS**: Cyberpunk-themed design system
        - **Responsive Design**: Multi-column layouts, optimized UX
        """)

    st.markdown("<br>", unsafe_allow_html=True)

    # ===== CALL TO ACTION =====
    st.markdown(f"""
    <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, {colors[2]} 0%, {colors[3]} 100%);
    border: 2px solid {colors[0]}; border-radius: 10px; box-shadow: 0 0 30px rgba(0, 217, 255, 0.3);'>
        <h3 style='color: {colors[0]}; margin: 0; text-shadow: 0 0 20px rgba(0, 217, 255, 0.5);'>
        Explore the Data
        </h3>
        <p style='color: {colors[4]}; font-size: 1.1rem; margin-top: 1rem;'>
        Use the navigation menu on the left to dive into detailed performance metrics, training analysis,
        heart rate efficiency trends, and interactive route visualizations.
        </p>
    </div>
    """, unsafe_allow_html=True)


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


# ===== PAGE: ROUTE VISUALIZATION =====
elif page == "Route Visualization":
    st.title("Marathon Route Visualization")
    st.markdown("*Marathon Routes*")

    st.markdown("<hr>", unsafe_allow_html=True)

    # BMO 2025 Map
    st.markdown("### BMO Vancouver Marathon")

    try:
        trackpoints_bmo = parse_activity_file("activities/15342430162.tcx.gz")
        if trackpoints_bmo:
            # Create DataFrame for st.map
            df_bmo = pd.DataFrame(
                [(lat, lon) for lat, lon, _, _ in trackpoints_bmo],
                columns=['lat', 'lon']
            )

            # Display the map with green color
            st.map(df_bmo, color='#51cf66', size=20, zoom=11, use_container_width=True)
        else:
            st.error("Could not load BMO 2025 route")
    except Exception as e:
        st.error(f"Error loading BMO 2025 route: {e}")

    st.markdown("<br>", unsafe_allow_html=True)

    # RVM 2025 Map
    st.markdown("### Royal Victoria Marathon")

    try:
        trackpoints_rvm = parse_activity_file("activities/17205422180.fit.gz")
        if trackpoints_rvm:
            # Create DataFrame for st.map
            df_rvm = pd.DataFrame(
                [(lat, lon) for lat, lon, _, _ in trackpoints_rvm],
                columns=['lat', 'lon']
            )

            # Display the map with electric cyan color
            st.map(df_rvm, color='#00d9ff', size=20, zoom=13, use_container_width=True)
        else:
            st.error("Could not load RVM 2025 route")
    except Exception as e:
        st.error(f"Error loading RVM 2025 route: {e}")


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
