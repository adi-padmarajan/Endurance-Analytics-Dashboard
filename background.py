import streamlit as st


def render(colors):
    """
    Render the Project Background page with methodology and training philosophy.

    Args:
        colors (list): Theme color palette [cyan, purple, violet, abyss, ice-blue]
    """
    # PAGE HEADER
    st.markdown(
        f"""
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
            Project Background
        </h1>

        <h3 style="
            color: #cbd5e1;
            font-weight: 300;
            letter-spacing: 1.2px;
            margin: 0;
            font-size: 1.4rem;
            line-height: 1.6;
        ">
            The Story Behind the Data
        </h3>

        <p style="
            color: #94a3b8;
            font-weight: 400;
            margin: 20px 0 0 0;
            font-size: 1rem;
            letter-spacing: 0.5px;
        ">
            By Aditya Padmarajan
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # SECTION SPACING
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # PROJECT GENESIS
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
            Project Genesis
        </h2>
    </div>
    """, unsafe_allow_html=True)

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
    <p style="
        color: #cbd5e1;
        font-size: 17px;
        line-height: 1.9;
        margin: 0 0 20px 0;
        text-align: justify;
    ">
        In October 2022, I completed my first marathon at the <span style='color: #38bdf8; font-weight: 600;'>Royal Victoria Marathon</span>
        with a time of <span style='color: #00ff9f; font-weight: 600;'>4:46:07</span>. As a recreational runner with limited endurance training,
        crossing the finish line was an achievement in itself. However, the experience sparked a question: <em>How much can human performance
        improve through systematic training and data-driven optimization?</em>
    </p>

    <p style="
        color: #cbd5e1;
        font-size: 17px;
        line-height: 1.9;
        margin: 0;
        text-align: justify;
    ">
        This project documents the journey from that first marathon to achieving a <span style='color: #00ff9f; font-weight: 600;'>3:26:00</span>
        finish at the 2025 Royal Victoria Marathon—an <span style='color: #b957ff; font-weight: 600;'>80-minute improvement</span> representing
        a complete transformation in endurance capacity, physiological efficiency, and competitive performance.
    </p>
    </div>
    """, unsafe_allow_html=True)

    # SECTION SPACING
    st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)

    # METHODOLOGY & DATA COLLECTION
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
            Methodology & Data Collection
        </h2>
    </div>
    """, unsafe_allow_html=True)

    # Two column layout for methodology
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div style="
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.88), rgba(2, 6, 23, 0.92));
            border-radius: 16px;
            padding: 32px;
            border-left: 5px solid #38bdf8;
            box-shadow: 0 6px 25px rgba(56, 189, 248, 0.2);
            min-height: 630px;
            max-height: 630px;
        ">
            <h3 style='
                color: #38bdf8;
                margin: 0 0 20px 0;
                font-size: 1.5rem;
                font-weight: 600;
                letter-spacing: 0.5px;
            '>Data Acquisition</h3>
            <p style='
                color: #cbd5e1;
                line-height: 1.9;
                font-size: 16px;
                margin: 0 0 16px 0;
            '>
                All training data was captured using GPS-enabled sports watches and uploaded to
                <strong style='color: #00ff9f;'>Strava</strong>, providing comprehensive activity tracking including:
            </p>
            <ul style='
                color: #cbd5e1;
                line-height: 1.9;
                font-size: 15.5px;
                margin: 0;
                padding-left: 20px;
            '>
                <li style='margin-bottom: 10px;'><b style='color: #e0f2fe;'>GPS Coordinates:</b> Latitude/longitude tracks for route visualization</li>
                <li style='margin-bottom: 10px;'><b style='color: #e0f2fe;'>Performance Metrics:</b> Distance, pace, speed, elevation gain</li>
                <li style='margin-bottom: 10px;'><b style='color: #e0f2fe;'>Physiological Data:</b> Heart rate, estimated VO₂ Max</li>
                <li style='margin-bottom: 10px;'><b style='color: #e0f2fe;'>Temporal Data:</b> Activity timestamps, duration</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.88), rgba(2, 6, 23, 0.92));
            border-radius: 16px;
            padding: 32px;
            border-left: 5px solid #b957ff;
            box-shadow: 0 6px 25px rgba(185, 87, 255, 0.2);
            min-height: 610px;
            max-height: 610px;
        ">
            <h3 style='
                color: #b957ff;
                margin: 0 0 20px 0;
                font-size: 1.5rem;
                font-weight: 600;
                letter-spacing: 0.5px;
            '>Analysis Framework</h3>
            <p style='
                color: #cbd5e1;
                line-height: 1.9;
                font-size: 16px;
                margin: 0 0 16px 0;
            '>
                The analysis leverages <strong style='color: #00ff9f;'>Python-based data science tools</strong>
                to extract insights from the raw activity data:
            </p>
            <ul style='
                color: #cbd5e1;
                line-height: 1.9;
                font-size: 15.5px;
                margin: 0;
                padding-left: 20px;
            '>
                <li style='margin-bottom: 10px;'><b style='color: #e0f2fe;'>Data Processing:</b> Pandas for data aggregation and transformation</li>
                <li style='margin-bottom: 10px;'><b style='color: #e0f2fe;'>Visualization:</b> Plotly for interactive charts and graphs</li>
                <li style='margin-bottom: 10px;'><b style='color: #e0f2fe;'>Geospatial Mapping:</b> GPX/TCX/FIT file parsing for route visualization</li>
                <li style='margin-bottom: 10px;'><b style='color: #e0f2fe;'>Metrics Calculation:</b> Aggregations, averages, and year-over-year comparisons</li>
                <li style='margin-bottom: 0;'><b style='color: #e0f2fe;'>Dashboard:</b> Streamlit for interactive web-based presentation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # SECTION SPACING
    st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)

    # KEY TRAINING PRINCIPLES
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
            Training Philosophy
        </h2>
    </div>
    """, unsafe_allow_html=True)

    # Three column layout for training principles
    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown("""
        <div style="
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.88), rgba(2, 6, 23, 0.92));
            border-radius: 16px;
            padding: 28px;
            border-left: 5px solid #00ff9f;
            box-shadow: 0 6px 25px rgba(0, 255, 159, 0.2);
            min-height: 420px;
        ">
            <h3 style='
                color: #00ff9f;
                margin: 0 0 18px 0;
                font-size: 1.4rem;
                font-weight: 600;
                letter-spacing: 0.5px;
            '>Progressive Overload</h3>
            <p style='
                color: #cbd5e1;
                line-height: 1.9;
                font-size: 15.5px;
                margin: 0;
            '>
                Training volume increased gradually from a modest base of <strong style='color: #00ff9f;'>246 km in 2022</strong> to a peak of
                <strong style='color: #00ff9f;'>1,712 km in 2025</strong>. This systematic progression allowed for physiological adaptations
                while minimizing injury risk through proper periodization and recovery protocols.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.88), rgba(2, 6, 23, 0.92));
            border-radius: 16px;
            padding: 28px;
            border-left: 5px solid #38bdf8;
            box-shadow: 0 6px 25px rgba(56, 189, 248, 0.2);
            min-height: 420px;
        ">
            <h3 style='
                color: #38bdf8;
                margin: 0 0 18px 0;
                font-size: 1.4rem;
                font-weight: 600;
                letter-spacing: 0.5px;
            '>Aerobic Foundation</h3>
            <p style='
                color: #cbd5e1;
                line-height: 1.9;
                font-size: 15.5px;
                margin: 0;
            '>
                Majority of training conducted at <strong style='color: #38bdf8;'>low-to-moderate intensity</strong> to build aerobic capacity.
                Heart rate analysis demonstrates improved efficiency—maintaining faster paces at lower heart rates as cardiovascular
                adaptations accumulated over successive training cycles.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.88), rgba(2, 6, 23, 0.92));
            border-radius: 16px;
            padding: 28px;
            border-left: 5px solid #51cf66;
            box-shadow: 0 6px 25px rgba(81, 207, 102, 0.2);
            min-height: 420px;
        ">
            <h3 style='
                color: #51cf66;
                margin: 0 0 18px 0;
                font-size: 1.4rem;
                font-weight: 600;
                letter-spacing: 0.5px;
            '>Data-Driven Decisions</h3>
            <p style='
                color: #cbd5e1;
                line-height: 1.9;
                font-size: 15.5px;
                margin: 0;
            '>
                Every training run was logged and analyzed to identify trends, optimize recovery, and adjust training intensity.
                <strong style='color: #51cf66;'>GPS tracking and heart rate monitoring</strong> provided objective feedback,
                enabling evidence-based adjustments to training strategy.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # SECTION SPACING
    st.markdown("<div style='height: 48px;'></div>", unsafe_allow_html=True)
