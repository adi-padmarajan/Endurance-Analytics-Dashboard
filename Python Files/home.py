import streamlit as st
import plotly.graph_objects as go


def render(colors):
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
