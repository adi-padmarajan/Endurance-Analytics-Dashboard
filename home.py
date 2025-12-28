import streamlit as st
import plotly.graph_objects as go


def render(colors):
    # HERO HEADER - ENHANCED CINEMATIC DESIGN
    st.markdown(
    """
    <div style="
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.95), rgba(2, 6, 23, 0.98));
        border-radius: 24px;
        padding: 48px 40px;
        width: 100%;
        margin: 0 0 48px 0;
        box-shadow:
            0 8px 40px rgba(56, 189, 248, 0.25),
            0 0 100px rgba(56, 189, 248, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(56, 189, 248, 0.35);
        backdrop-filter: blur(12px);
        text-align: center;
    ">
    <h1 style="
        color: #38bdf8;
        margin: 0 0 16px 0;
        font-size: 3.2rem;
        font-weight: 700;
        text-shadow: 0 0 35px rgba(56, 189, 248, 0.8);
        letter-spacing: 1.5px;
    ">
        The Sub-3:30 Protocol
    </h1>

    <h3 style="
        color: #cbd5e1;
        font-weight: 300;
        letter-spacing: 1.2px;
        margin: 0;
        font-size: 1.4rem;
        line-height: 1.6;
    ">
        A Data-Driven Journey from a Sub 5:00 to a Sub 3:30 Marathon
    </h3>
    </div>
    """,
    unsafe_allow_html=True
    )

    # EXECUTIVE SUMMARY SECTION
    st.markdown("""
    <div style='margin-bottom: 32px;'>
        <h2 style='
            color: #38bdf8;
            margin: 0 0 28px 0;
            font-size: 2rem;
            font-weight: 600;
            text-align: center;
            letter-spacing: 0.8px;
            text-shadow: 0 0 20px rgba(56, 189, 248, 0.5);
        '>
            Executive Summary
        </h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4, gap="medium")

    # Metric Card 1 - Minutes Improved
    with col1:
        st.markdown("""
        <div style='
            text-align: center;
            padding: 2.2rem 1.5rem;
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.9), rgba(10, 4, 32, 0.95));
            border: 2px solid rgba(56, 189, 248, 0.45);
            border-radius: 18px;
            box-shadow:
                0 10px 35px rgba(56, 189, 248, 0.25),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            transition: transform 0.3s ease;
            height: 250px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        '>
            <h2 style='
                color: #38bdf8;
                margin: 0;
                font-size: 3.2rem;
                font-weight: 700;
                line-height: 1;
                text-shadow: 0 0 25px rgba(56, 189, 248, 0.7);
            '>80</h2>
            <p style='
                color: #94a3b8;
                margin: 12px 0 0 0;
                font-size: 1rem;
                font-weight: 500;
                letter-spacing: 0.8px;
            '>Minutes Improved</p>
        </div>
        """, unsafe_allow_html=True)

    # Metric Card 2 - Training Runs
    with col2:
        st.markdown("""
        <div style='
            text-align: center;
            padding: 2.2rem 1.5rem;
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.9), rgba(10, 4, 32, 0.95));
            border: 2px solid rgba(185, 87, 255, 0.45);
            border-radius: 18px;
            box-shadow:
                0 10px 35px rgba(185, 87, 255, 0.25),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            transition: transform 0.3s ease;
            height: 250px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        '>
            <h2 style='
                color: #b957ff;
                margin: 0;
                font-size: 3.2rem;
                font-weight: 700;
                line-height: 1;
                text-shadow: 0 0 25px rgba(185, 87, 255, 0.7);
            '>347</h2>
            <p style='
                color: #94a3b8;
                margin: 12px 0 0 0;
                font-size: 1rem;
                font-weight: 500;
                letter-spacing: 0.8px;
            '>Training Runs</p>
        </div>
        """, unsafe_allow_html=True)

    # Metric Card 3 - Kilometers Logged
    with col3:
        st.markdown("""
        <div style='
            text-align: center;
            padding: 2.2rem 1.5rem;
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.9), rgba(10, 4, 32, 0.95));
            border: 2px solid rgba(0, 255, 159, 0.45);
            border-radius: 18px;
            box-shadow:
                0 10px 35px rgba(0, 255, 159, 0.25),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            transition: transform 0.3s ease;
            height: 250px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        '>
            <h2 style='
                color: #00ff9f;
                margin: 0;
                font-size: 3.2rem;
                font-weight: 700;
                line-height: 1;
                text-shadow: 0 0 25px rgba(0, 255, 159, 0.7);
            '>3400 +</h2>
            <p style='
                color: #94a3b8;
                margin: 12px 0 0 0;
                font-size: 1rem;
                font-weight: 500;
                letter-spacing: 0.8px;
            '>Kilometers Logged</p>
        </div>
        """, unsafe_allow_html=True)

    # Metric Card 4 - Years of Training
    with col4:
        st.markdown("""
        <div style='
            text-align: center;
            padding: 2.2rem 1.5rem;
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.9), rgba(10, 4, 32, 0.95));
            border: 2px solid rgba(81, 207, 102, 0.45);
            border-radius: 18px;
            box-shadow:
                0 10px 35px rgba(81, 207, 102, 0.25),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            transition: transform 0.3s ease;
            height: 250px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        '>
            <h2 style='
                color: #51cf66;
                margin: 0;
                font-size: 3.2rem;
                font-weight: 700;
                line-height: 1;
                text-shadow: 0 0 25px rgba(81, 207, 102, 0.7);
            '>3.5</h2>
            <p style='
                color: #94a3b8;
                margin: 12px 0 0 0;
                font-size: 1rem;
                font-weight: 500;
                letter-spacing: 0.8px;
            '>Years of Training</p>
        </div>
        """, unsafe_allow_html=True)

    # SECTION SPACING
    st.markdown("<div style='height: 56px;'></div>", unsafe_allow_html=True)

    # PROJECT OVERVIEW CARD
    st.markdown("""
    <div style="
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.9), rgba(2, 6, 23, 0.95));
        border-radius: 20px;
        padding: 40px 44px;
        width: 100%;
        margin: 0 0 48px 0;
        border: 1px solid rgba(56, 189, 248, 0.35);
        box-shadow:
            0 10px 40px rgba(56, 189, 248, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    ">
    <h2 style="
        color: #38bdf8;
        margin: 0 0 24px 0;
        text-align: center;
        letter-spacing: 1px;
        font-size: 1.8rem;
        font-weight: 600;
        text-shadow: 0 0 20px rgba(56, 189, 248, 0.5);
    ">
        Project Overview
    </h2>

    <p style="
        color: #cbd5e1;
        font-size: 17px;
        line-height: 1.9;
        margin: 0 0 20px 0;
        text-align: justify;
    ">
        This comprehensive data analytics project chronicles a remarkable transformation in marathon
        performance, combining <span style='color: #38bdf8; font-weight: 600;'>endurance sports science</span>,
        <span style='color: #b957ff; font-weight: 600;'>data visualization</span>, and
        <span style='color: #00ff9f; font-weight: 600;'>performance analytics</span> to document the journey
        from a recreational runner to a competitive marathoner.
    </p>

    <p style="
        color: #cbd5e1;
        font-size: 17px;
        line-height: 1.9;
        margin: 0;
        text-align: justify;
    ">
        The analysis leverages <span style='color: #38bdf8; font-weight: 600;'>347 GPS-tracked running activities</span>
        spanning 3.5 years (2022–2025), examining the physiological, training, and performance adaptations that enabled an
        <span style='color: #00ff9f; font-weight: 600;'>80-minute improvement</span> across
        <span style='color: #b957ff; font-weight: 600;'>6 marathon races</span>.
    </p>
    </div>
    """,
    unsafe_allow_html=True
)

    # RESEARCH METHODOLOGY & PERFORMANCE TIMELINE SECTION
    st.markdown("""
    <div style='margin-bottom: 32px;'>
    <h2 style='
        color: #38bdf8;
        margin: 0 0 32px 0;
        font-size: 2rem;
        font-weight: 600;
        text-align: center;
        letter-spacing: 0.8px;
        text-shadow: 0 0 20px rgba(56, 189, 248, 0.5);
    '>
        Research Methodology
    </h2>
    </div>
    """, unsafe_allow_html=True)

    # Three column layout for methodology cards
    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        # Data Sources Card
        st.markdown("""
        <div style="
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.88), rgba(2, 6, 23, 0.92));
            border-radius: 16px;
            padding: 28px;
            border-left: 5px solid #38bdf8;
            box-shadow: 0 6px 25px rgba(56, 189, 248, 0.2);
            min-height: 450px;
            max-height: 450px;
            overflow: hidden;
        ">
            <h3 style='
                color: #38bdf8;
                margin: 0 0 20px 0;
                font-size: 1.4rem;
                font-weight: 600;
                letter-spacing: 0.5px;
            '>Data Sources</h3>
            <ul style='
                color: #cbd5e1;
                line-height: 1.9;
                font-size: 15.5px;
                margin: 0;
                padding-left: 20px;
            '>
                <li style='margin-bottom: 10px;'><b style='color: #e0f2fe;'>Primary Dataset:</b> Strava activity exports</li>
                <li style='margin-bottom: 10px;'><b style='color: #e0f2fe;'>Activity Count:</b> 347 running sessions</li>
                <li style='margin-bottom: 10px;'><b style='color: #e0f2fe;'>Temporal Range:</b> 2022 - 2025</li>
                <li style='margin-bottom: 0;'><b style='color: #e0f2fe;'>Geographic Scope:</b> Victoria & Vancouver, BC</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Analytical Approach Card
        st.markdown("""
        <div style="
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.88), rgba(2, 6, 23, 0.92));
            border-radius: 16px;
            padding: 28px;
            border-left: 5px solid #b957ff;
            box-shadow: 0 6px 25px rgba(185, 87, 255, 0.2);
            min-height: 450px;
            max-height: 450px;
            overflow: hidden;
        ">
            <h3 style='
                color: #b957ff;
                margin: 0 0 20px 0;
                font-size: 1.4rem;
                font-weight: 600;
                letter-spacing: 0.5px;
            '>Analytical Approach</h3>
            <ul style='
                color: #cbd5e1;
                line-height: 1.9;
                font-size: 15.5px;
                margin: 0;
                padding-left: 20px;
            '>
                <li style='margin-bottom: 10px;'><b style='color: #e0f2fe;'>Performance Metrics:</b> Race time, pace evolution</li>
                <li style='margin-bottom: 10px;'><b style='color: #e0f2fe;'>Training Volume:</b> Annual distance, frequency</li>
                <li style='margin-bottom: 10px;'><b style='color: #e0f2fe;'>Physiological Data:</b> Heart rate efficiency</li>
                <li style='margin-bottom: 0;'><b style='color: #e0f2fe;'>Geospatial Analysis:</b> Route visualization</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        # Key Race Events Card
        st.markdown("""
        <div style="
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.88), rgba(2, 6, 23, 0.92));
            border-radius: 16px;
            padding: 28px;
            border-left: 5px solid #00ff9f;
            box-shadow: 0 6px 25px rgba(0, 255, 159, 0.2);
            min-height: 450px;
            max-height: 450px;
            overflow: hidden;
        ">
            <h3 style='
                color: #00ff9f;
                margin: 0 0 20px 0;
                font-size: 1.4rem;
                font-weight: 600;
                letter-spacing: 0.5px;
            '>Key Race Events</h3>
            <ul style='
                color: #cbd5e1;
                line-height: 1.9;
                font-size: 15.5px;
                margin: 0;
                padding-left: 20px;
            '>
                <li style='margin-bottom: 10px;'><b style='color: #e0f2fe;'>Royal Victoria Marathon:</b> 4 finishes (2022, 2023, 2024, 2025)</li>
                <li style='margin-bottom: 0;'><b style='color: #e0f2fe;'>BMO Vancouver Marathon:</b> 2 finishes (2023, 2025)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # SECTION SPACING
    st.markdown("<div style='height: 56px;'></div>", unsafe_allow_html=True)

    # PERFORMANCE TIMELINE
    st.markdown("""
    <div style='margin-bottom: 32px;'>
    <h2 style='
        color: #38bdf8;
        margin: 0 0 32px 0;
        font-size: 2rem;
        font-weight: 600;
        text-align: center;
        letter-spacing: 0.8px;
        text-shadow: 0 0 20px rgba(56, 189, 248, 0.5);
    '>
        Performance Timeline
    </h2>
    </div>
    """, unsafe_allow_html=True)

    # Performance Timeline Chart
    races_mini = ["RVM 2022", "BMO 2023", "RVM 2023", "RVM 2024", "BMO 2025", "RVM 2025"]
    times_mini = [286.12, 265.80, 256.97, 227.78, 217.38, 206.00]
    times_labels_mini = ["4:46:07", "4:25:48", "4:16:58", "3:47:47", "3:37:23", "3:26:00"]

    fig_mini = go.Figure()

    fig_mini.add_trace(go.Scatter(
        x=races_mini,
        y=times_mini,
        mode='lines+markers',
        marker=dict(size=14, color='#38bdf8', line=dict(color='#b957ff', width=3)),
        line=dict(width=4, color='#38bdf8', shape='spline'),
        hovertemplate="<b>%{x}</b><br>Time: %{customdata}<extra></extra>",
        customdata=times_labels_mini
    ))

    fig_mini.update_layout(
        xaxis=dict(
            tickfont=dict(size=13, color='#cbd5e1', family='Arial'),
            showgrid=True,
            gridcolor='rgba(56, 189, 248, 0.12)',
        ),
        yaxis=dict(
            tickvals=times_mini,
            ticktext=times_labels_mini,
            autorange="reversed",
            tickfont=dict(size=13, color='#cbd5e1', family='Arial'),
            showgrid=True,
            gridcolor='rgba(56, 189, 248, 0.12)',
        ),
        height=460,
        margin=dict(l=80, r=40, t=20, b=70),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family='Arial', color='#38bdf8'),
        showlegend=False
    )

    st.plotly_chart(fig_mini, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # SECTION SPACING
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # KEY FINDINGS SECTION
    st.markdown("""
    <div style='margin-bottom: 32px;'>
    <h2 style='
        color: #38bdf8;
        margin: 0 0 28px 0;
        font-size: 2rem;
        font-weight: 600;
        text-align: center;
        letter-spacing: 0.8px;
        text-shadow: 0 0 20px rgba(56, 189, 248, 0.5);
    '>
        Key Research Findings
    </h2>
    </div>
    """, unsafe_allow_html=True)

    # Performance Adaptations Expander
    with st.expander("Performance Adaptations - Marathon Time, Pace Evolution & Training Volume", expanded=False):
        st.markdown("""
        <div style="
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.7), rgba(2, 6, 23, 0.8));
            border-radius: 14px;
            padding: 24px;
            border-left: 4px solid #38bdf8;
        ">
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            **Marathon Time Improvement**
            - **First marathon (RVM 2022):** 4:46:07
              *(6:47/km pace)*
            - **Latest marathon (RVM 2025):** 3:26:00
              *(4:52/km pace)*
            - **Total improvement:** 80 minutes
              *(27.9% faster)*
            """)

        with col2:
            st.markdown("""
            **Pace Evolution**
            - Average pace improved from **6:30/km to 4:50/km**
            - Consistent **sub-5:00/km** pacing achieved by 2024
            - **Negative splits** mastered in final races
            """)

        with col3:
            st.markdown("""
            **Training Volume Progression**
            - **2022:** Lower baseline volume (building phase)
            - **2023:** Volume increase with consistency focus
            - **2024-2025:** Peak training years with **1000+ km annually**
            """)

        st.markdown("</div>", unsafe_allow_html=True)

    # Physiological Adaptations Expander
    with st.expander("Physiological Adaptations - Aerobic Efficiency, Consistency & Race Preparation", expanded=False):
        st.markdown("""
        <div style="
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.7), rgba(2, 6, 23, 0.8));
            border-radius: 14px;
            padding: 24px;
            border-left: 4px solid #b957ff;
        ">
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            **Aerobic Efficiency Gains**
            - Heart rate efficiency **improved year-over-year**
            - Same pace achieved at **lower heart rates** over time
            - Enhanced **lactate threshold and VO2max** indicators
            """)

        with col2:
            st.markdown("""
            **Training Consistency**
            - **347 runs** completed over 3.5 years
            - Average of **99 runs per year**
            - Maintained **injury-free progression** through smart periodization
            """)

        with col3:
            st.markdown("""
            **Race-Specific Preparation**
            - **Course familiarity** advantage at RVM (4 races)
            - Consistent improvement at same venue demonstrates **adaptation**
            - **Strategic race selection** for optimal progression
            """)

        st.markdown("</div>", unsafe_allow_html=True)

    # SCIENTIFIC CONTEXT EXPANDER
    with st.expander("Scientific Context & Training Principles - Exercise Physiology Fundamentals", expanded=False):
        st.markdown("""
        <div style="
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.7), rgba(2, 6, 23, 0.8));
            border-radius: 14px;
            padding: 28px;
            border-left: 4px solid #00ff9f;
        ">
        <p style='color: #cbd5e1; font-size: 15.5px; line-height: 1.9; margin-bottom: 24px;'>
        This project demonstrates several well-established principles from exercise physiology and endurance training:
        </p>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            **Aerobic Base Development**

            The foundation of marathon performance lies in building aerobic capacity through consistent, moderate-intensity training.
            The heart rate analysis reveals progressive improvements in aerobic efficiency—maintaining faster paces at lower heart rates
            over successive years.

            **Progressive Overload**

            Annual training volume increased systematically, allowing for physiological adaptations while minimizing injury risk.
            The progression from recreational to competitive performance exemplifies proper application of progressive overload principles.
            """)

        with col2:
            st.markdown("""
            **Specificity & Course Familiarity**

            Multiple races on the same course (Royal Victoria Marathon) provided controlled conditions to measure true performance gains,
            eliminating course difficulty as a confounding variable.

            **Data-Driven Training**

            Leveraging GPS tracking, heart rate monitoring, and performance analytics enabled evidence-based training decisions,
            optimizing the progression toward the sub-3:30 goal.
            """)

        st.markdown("</div>", unsafe_allow_html=True)

    # SECTION SPACING
    st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)

    # DASHBOARD NAVIGATION SECTION
    st.markdown("""
    <div style='margin-bottom: 32px;'>
    <h2 style='
        color: #38bdf8;
        margin: 0 0 32px 0;
        font-size: 2rem;
        font-weight: 600;
        text-align: center;
        letter-spacing: 0.8px;
        text-shadow: 0 0 20px rgba(56, 189, 248, 0.5);
    '>
        Dashboard Navigation
    </h2>
    </div>
    """, unsafe_allow_html=True)

    nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4, gap="medium")

    with nav_col1:
        st.markdown("""
        <div style='
            padding: 2rem 1.6rem;
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.88), rgba(2, 6, 23, 0.92));
            border-left: 5px solid #38bdf8;
            border-radius: 16px;
            box-shadow: 0 6px 25px rgba(56, 189, 248, 0.25);
            min-height: 275px;
            max-height: 275px;
            overflow: hidden;
            transition: transform 0.3s ease;
        '>
        <h3 style='
            color: #38bdf8;
            margin: 0 0 14px 0;
            font-size: 1.3rem;
            font-weight: 600;
            letter-spacing: 0.5px;
        '>Marathon Performance</h3>
        <p style='
            color: #94a3b8;
            font-size: 0.95rem;
            line-height: 1.7;
            margin: 0;
        '>
        Track race-by-race improvements, pace evolution curves, and competitive performance metrics across all 6 marathons.
        </p>
        </div>
        """, unsafe_allow_html=True)

    with nav_col2:
        st.markdown("""
        <div style='
            padding: 2rem 1.6rem;
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.88), rgba(2, 6, 23, 0.92));
            border-left: 5px solid #b957ff;
            border-radius: 16px;
            box-shadow: 0 6px 25px rgba(185, 87, 255, 0.25);
            min-height: 275px;
            max-height: 275px;
            overflow: hidden;
        '>
        <h3 style='
            color: #b957ff;
            margin: 0 0 14px 0;
            font-size: 1.3rem;
            font-weight: 600;
            letter-spacing: 0.5px;
        '>Training Metrics</h3>
        <p style='
            color: #94a3b8;
            font-size: 0.95rem;
            line-height: 1.7;
            margin: 0;
        '>
        Explore annual training volume, consistency patterns, and how progressive overload was applied year-over-year.
        </p>
        </div>
        """, unsafe_allow_html=True)

    with nav_col3:
        st.markdown("""
        <div style='
            padding: 2rem 1.6rem;
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.88), rgba(2, 6, 23, 0.92));
            border-left: 5px solid #00ff9f;
            border-radius: 16px;
            box-shadow: 0 6px 25px rgba(0, 255, 159, 0.25);
            min-height: 275px;
            max-height: 275px;
            overflow: hidden;
        '>
        <h3 style='
            color: #00ff9f;
            margin: 0 0 14px 0;
            font-size: 1.3rem;
            font-weight: 600;
            letter-spacing: 0.5px;
        '>Heart Rate Analysis</h3>
        <p style='
            color: #94a3b8;
            font-size: 0.95rem;
            line-height: 1.7;
            margin: 0;
        '>
        Analyze aerobic efficiency improvements through pace-HR relationships and cardiovascular adaptations over time.
        </p>
        </div>
        """, unsafe_allow_html=True)

    with nav_col4:
        st.markdown("""
        <div style='
            padding: 2rem 1.6rem;
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.88), rgba(2, 6, 23, 0.92));
            border-left: 5px solid #51cf66;
            border-radius: 16px;
            box-shadow: 0 6px 25px rgba(81, 207, 102, 0.25);
            min-height: 275px;
            max-height: 275px;
            overflow: hidden;
        '>
        <h3 style='
            color: #51cf66;
            margin: 0 0 14px 0;
            font-size: 1.3rem;
            font-weight: 600;
            letter-spacing: 0.5px;
        '>Route Visualization</h3>
        <p style='
            color: #94a3b8;
            font-size: 0.95rem;
            line-height: 1.7;
            margin: 0;
        '>
        Interactive GPS route maps of marathon courses, showcasing the terrain and race-day execution.
        </p>
        </div>
        """, unsafe_allow_html=True)

    # SECTION SPACING
    st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)

    # CALL TO ACTION 
    st.markdown("""
    <div style='
        text-align: center;
        padding: 3rem 2.5rem;
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(2, 6, 23, 0.98));
        border: 2px solid rgba(56, 189, 248, 0.5);
        border-radius: 20px;
        box-shadow:
            0 10px 40px rgba(56, 189, 248, 0.35),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        width: 100%;
        margin: 0;
    '>
        <h2 style='
            color: #38bdf8;
            margin: 0 0 20px 0;
            font-size: 2.2rem;
            font-weight: 600;
            text-shadow: 0 0 30px rgba(56, 189, 248, 0.7);
            letter-spacing: 1px;
        '>
        Explore the Data
        </h2>
        <p style='
            color: #cbd5e1;
            font-size: 1.15rem;
            line-height: 1.8;
            margin: 0;
            max-width: 750px;
            margin: 0 auto;
        '>
        Use the navigation menu on the left to dive into detailed performance metrics, training analysis,
        heart rate efficiency trends, and interactive route visualizations.
        </p>
    </div>
    """, unsafe_allow_html=True)
