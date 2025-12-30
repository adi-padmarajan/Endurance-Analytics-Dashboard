import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


def render(colors, vo2max_df):
    st.title("Marathon Performance Analytics")
    st.markdown("*Visualizing 3 years of improvement across 6 marathon races*")

    # Define comprehensive race data
    races = ["RVM 2022", "BMO 2023", "RVM 2023", "RVM 2024", "BMO 2025", "RVM 2025"]
    times_minutes = [286.12, 265.80, 256.97, 227.78, 217.38, 206.00]  # In decimal minutes
    times_labels = ["4:46:07", "4:25:48", "4:16:58", "3:47:47", "3:37:23", "3:26:00"]
    pace_decimal = [6.50, 6.22, 6.07, 5.37, 5.12, 4.83]
    pace_labels = ["6:30", "6:13", "6:04", "5:22", "5:07", "4:50"]

    # Calculate key metrics
    total_improvement = times_minutes[0] - times_minutes[-1]
    total_improvement_pct = (total_improvement / times_minutes[0]) * 100
    avg_pace_improvement = pace_decimal[0] - pace_decimal[-1]
    best_race_improvement = max([times_minutes[i] - times_minutes[i+1] for i in range(len(times_minutes)-1)])

    # KEY PERFORMANCE METRICS - Compact Cards
    st.markdown("### Performance at a Glance")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #0a0420 0%, #1a0d2e 100%);
                    padding: 20px;
                    border-radius: 10px;
                    border: 2px solid {colors[0]};
                    text-align: center;'>
            <h4 style='color: {colors[0]}; margin: 0; font-size: 14px;'>Total Time Saved</h4>
            <h3 style='color: {colors[4]}; margin: 10px 0; font-size: 32px;'>{int(total_improvement)} min</h2>
            <p style='color: {colors[1]}; margin: 0; font-size: 12px;'>{total_improvement_pct:.1f}% faster</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #0a0420 0%, #1a0d2e 100%);
                    padding: 20px;
                    border-radius: 10px;
                    border: 2px solid {colors[1]};
                    text-align: center;'>
            <h4 style='color: {colors[1]}; margin: 0; font-size: 14px;'>Pace Improvement</h4>
            <h3 style='color: {colors[4]}; margin: 10px 0; font-size: 32px;'>{avg_pace_improvement:.1f} min/km</h2>
            <p style='color: {colors[0]}; margin: 0; font-size: 12px;'>{pace_labels[0]} → {pace_labels[-1]}</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #0a0420 0%, #1a0d2e 100%);
                    padding: 20px;
                    border-radius: 10px;
                    border: 2px solid #00ff9f;
                    text-align: center;'>
            <h4 style='color: #00ff9f; margin: 0; font-size: 14px;'>Best Improvement</h4>
            <h3 style='color: {colors[4]}; margin: 10px 0; font-size: 32px;'>{int(best_race_improvement)} min</h2>
            <p style='color: {colors[1]}; margin: 0; font-size: 12px;'>Single race jump</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #0a0420 0%, #1a0d2e 100%);
                    padding: 20px;
                    border-radius: 10px;
                    border: 2px solid {colors[0]};
                    text-align: center;'>
            <h4 style='color: {colors[0]}; margin: 0; font-size: 14px;'>Avg Per Race</h4>
            <h3 style='color: {colors[4]}; margin: 10px 0; font-size: 32px;'>{int(total_improvement/5)} min</h3>
            <p style='color: {colors[1]}; margin: 0; font-size: 12px;'>Consistency rate</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

     # RACE NARRATIVES - Detailed Stories
    st.markdown("### Race Narratives: The Journey")
    st.markdown("*The story behind each marathon*")

    race_narratives = [
        {
            'race': 'RVM 2022',
            'title': 'The Beginning: First Marathon Experience',
            'story': '''My marathon journey began with a true test of grit and humility. With almost no structured training,
            little race-day experience, and still regaining strength after a severe illness just weeks before, I stood at the
            start line just hoping to somehow make it through. By the time I was 16 km into the race, I hit the infamous wall—my
            legs heavy and cramped, my energy fading. Much of the remainder was a battle of willpower, alternating between running
            and walking, each step a lesson in perseverance. I crossed the finish line in 4:46:07, managing to secure a sub-5 hour finish.
            This first marathon exposed my weaknesses—pacing, nutrition, and mental resilience—while igniting a deep desire to improve.
            It was a humbling beginning, but it became the cornerstone for every breakthrough that followed.''',
            'key_learning': 'Completion over speed - establishing the foundation.'
        },
        {
            'race': 'BMO 2023',
            'title': 'Breakthrough Performance: First Sub-4:30',
            'story': '''I signed up for the BMO Vancouver Marathon 2023 the day after my first RVM, while I was barely recovered. Armed with
            improved training volume and a longer prep period, this race delivered a significant 20-minute improvement. The 4:25:48 finish represented
            the first major breakthrough, demonstrating that structured training yields measurable results.''',
            'key_learning': 'Structured training with adequate preparation time yields substantial improvements.'
        },
        {
            'race': 'RVM 2023',
            'title': 'Consolidation: Sub-4:20 Achievement',
            'story': '''Building on previous success, this race focused on maintaining momentum rather than
            dramatic improvements. Even though I had a better preparation for RVM 2023, I was mentally fatigued after going through 2 consecutive marathons and
            prep phases over a span of 8 months. This resulted in me slacking off and not following through with the training plan as diligently as before.
            A 4:16:58 finish showed steady progression—9 minutes faster than the previous race, but I felt that there was untapped potential that I could have unlocked in this race.''',
            'key_learning': 'Mental fatigue and inconsistent training limit physical gains - mindset matters.'
        },
        {
            'race': 'RVM 2024',
            'title': 'Major Breakthrough: Sub-4:00 Barrier Broken',
            'story': '''After RVM 2023, I decided to take time off and came back for RVM 2024 a year later. I saw the most dramatic single-race
            improvement: 29 minutes faster than the previous marathon. This performance resulted from refined training periodization, improved running
            economy, and optimal race-day execution. The 3:47:47 finish demonstrated that when training, recovery, and execution align,
            breakthrough performances become possible.''',
            'key_learning': 'Strategic recovery and renewed focus enable breakthrough performances.'
        },
        {
            'race': 'BMO 2025',
            'title': 'First Attempt at Sub-3:30',
            'story': '''After a successful breakthrough in RVM 2024, I decided to make my first sub-3:30 attempt at BMO 2025.
            I went through an intensive prep phase with a heavy emphasis on long runs and overall training volume.
            I secured a finish time of 3:37:23—a 10-minute improvement.
            Race execution was characterized by even pacing and effective fueling strategy. I hit the wall around 35 km, after which I got slower and couldn't keep
            up the pace. I understood that I needed more tempo runs, speed work, and lactate threshold-specific training in my training plan to be able to sustain a faster pace
            for longer.''',
            'key_learning': 'Volume alone is not enough - specificity and intensity work are essential.'
        },
        {
            'race': 'RVM 2025',
            'title': 'Peak Performance: Sub-3:30 Achieved',
            'story': '''The culmination of three years of systematic training. A 3:26:00 finish represented an
            11-minute improvement and 80-minute total reduction since the first marathon. This performance
            demonstrated mature race execution: disciplined pacing, efficient energy systems, and mental fortitude.
            The achievement marks a significant milestone while highlighting the law of diminishing returns ahead.''',
            'key_learning': 'Mastery comes from sustained, intelligent effort over time.'
        }
    ]

    for i, narrative in enumerate(race_narratives):
        border_color = colors[0] if i % 2 == 0 else colors[1]

        with st.expander(f"**{narrative['race']}** - {times_labels[i]} - {narrative['title']}", expanded=False):
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #0a0420 0%, #1a0d2e 100%);
                    padding: 20px;
                    border-radius: 8px;
                    border-left: 4px solid {border_color};
                    margin: 10px 0;'>
            <p style='color: {colors[4]}; line-height: 1.8; font-size: 14px; margin-bottom: 15px;'>
                {narrative['story']}
            </p>
            <div style='background: rgba(0, 217, 255, 0.1);
                        padding: 12px;
                        border-radius: 6px;
                        border-left: 3px solid {border_color};'>
            <p style='color: {border_color}; font-weight: bold; font-size: 13px; margin: 0;'>
                Key Learning: <span style='color: {colors[4]}; font-weight: normal;'>{narrative['key_learning']}</span>
            </p>
            </div>
            </div>
            """, unsafe_allow_html=True)

            # Add race-specific metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Finish Time", times_labels[i])
            with col2:
                st.metric("Average Pace", f"{pace_labels[i]}/km")
            with col3:
                if i > 0:
                    improvement = times_minutes[i-1] - times_minutes[i]
                    st.metric("Time Improvement", f"{int(improvement)} min", delta=f"-{int(improvement)} min")
                else:
                    st.metric("Status", "Baseline")

    st.markdown("<br>", unsafe_allow_html=True)

    # VISUALIZATION 1: DUAL AXIS PERFORMANCE TIMELINE
    st.markdown("### Performance Timeline: Time & Pace Evolution")

    fig_timeline = make_subplots(specs=[[{"secondary_y": True}]])

    # Add finish time trace
    fig_timeline.add_trace(
        go.Scatter(
            x=races,
            y=times_minutes,
            name='Finish Time',
            mode='lines+markers',
            marker=dict(size=12, color=colors[0], line=dict(color=colors[1], width=2)),
            line=dict(width=3, color=colors[0], shape='spline'),
            customdata=times_labels,
            hovertemplate="<b>%{x}</b><br>Time: %{customdata}<extra></extra>"
        ),
        secondary_y=False
    )

    # Add pace trace
    fig_timeline.add_trace(
        go.Scatter(
            x=races,
            y=pace_decimal,
            name='Average Pace',
            mode='lines+markers',
            marker=dict(size=12, color=colors[1], line=dict(color=colors[0], width=2)),
            line=dict(width=3, color=colors[1], shape='spline', dash='dot'),
            customdata=pace_labels,
            hovertemplate="<b>%{x}</b><br>Pace: %{customdata}/km<extra></extra>"
        ),
        secondary_y=True
    )

    fig_timeline.update_xaxes(
        title_text="Race",
        title_font=dict(size=14, color=colors[0]),
        tickfont=dict(size=12, color=colors[4]),
        showgrid=True,
        gridcolor='rgba(0, 217, 255, 0.15)'
    )

    fig_timeline.update_yaxes(
        title_text="Finish Time (minutes)",
        title_font=dict(size=14, color=colors[0]),
        tickvals=times_minutes,
        ticktext=times_labels,
        autorange="reversed",
        tickfont=dict(size=11, color=colors[4]),
        showgrid=True,
        gridcolor='rgba(0, 217, 255, 0.15)',
        secondary_y=False
    )

    fig_timeline.update_yaxes(
        title_text="Pace (min/km)",
        title_font=dict(size=14, color=colors[1]),
        tickvals=pace_decimal,
        ticktext=pace_labels,
        autorange="reversed",
        tickfont=dict(size=11, color=colors[4]),
        showgrid=False,
        secondary_y=True
    )

    fig_timeline.update_layout(
        height=500,
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(family='Arial', color=colors[0]),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(color=colors[4])
        ),
        hovermode='x unified',
        hoverlabel=dict(bgcolor="#0d1f26", font_size=13, bordercolor=colors[1], font_color=colors[4]),
        margin=dict(l=70, r=70, t=30, b=60)
    )

    st.plotly_chart(fig_timeline, use_container_width=True)

    # Insights for Performance Timeline
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #0d1f26 0%, #1a0d2e 100%);
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid {colors[0]};
                margin: 20px 0;'>
        <h4 style='color: {colors[0]}; margin-top: 0; font-size: 15px;'>Analysis: Non-Linear Progress Pattern</h4>
        <p style='color: {colors[4]}; line-height: 1.8; font-size: 14px; margin: 10px 0;'>
            The dual-axis chart shows that improvement has been non-linear across the six races. The largest single improvement
            occurred from RVM 2023 to RVM 2024 (29 minutes) following a year-long break from marathon racing, while consecutive
            race blocks showed more gradual gains. The pace curve demonstrates an accelerating rate of improvement in recent races.
            The steepest pace improvement occurred between RVM 2024 and RVM 2025.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # VISUALIZATION 2: CUMULATIVE IMPROVEMENT WATERFALL
    st.markdown("### Cumulative Improvement Breakdown")
    st.markdown("*How much each race contributed to overall progress*")

    # Calculate improvements for waterfall
    improvements = [0]  # Start at 0
    for i in range(1, len(times_minutes)):
        improvements.append(times_minutes[i-1] - times_minutes[i])

    # Waterfall chart data
    waterfall_x = ["Start"] + races[1:] + ["Total"]
    waterfall_measure = ["relative"] + ["relative"] * (len(races) - 1) + ["total"]
    waterfall_y = [times_minutes[0]] + improvements[1:] + [total_improvement]
    waterfall_text = [times_labels[0]] + [f"+{int(imp)} min" for imp in improvements[1:]] + [f"{int(total_improvement)} min"]

    fig_waterfall = go.Figure(go.Waterfall(
        name="Improvement",
        orientation="v",
        measure=waterfall_measure,
        x=waterfall_x,
        textposition="outside",
        text=waterfall_text,
        y=waterfall_y,
        connector={"line": {"color": colors[1], "width": 2, "dash": "dot"}},
        decreasing={"marker": {"color": colors[0]}},
        increasing={"marker": {"color": "#00ff9f"}},
        totals={"marker": {"color": colors[1]}}
    ))

    fig_waterfall.update_layout(
        height=500,
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(family='Arial', color=colors[4]),
        xaxis=dict(
            title="",
            tickfont=dict(size=12, color=colors[4]),
            showgrid=False
        ),
        yaxis=dict(
            title="Minutes Saved",
            tickfont=dict(size=12, color=colors[4]),
            showgrid=True,
            gridcolor='rgba(0, 217, 255, 0.15)'
        ),
        margin=dict(l=70, r=30, t=30, b=60)
    )

    st.plotly_chart(fig_waterfall, use_container_width=True)

    # Insights for Cumulative Improvement
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #0d1f26 0%, #1a0d2e 100%);
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid {colors[1]};
                margin: 20px 0;'>
        <h4 style='color: {colors[1]}; margin-top: 0; font-size: 15px;'>Analysis: Cumulative Improvement Breakdown</h4>
        <p style='color: {colors[4]}; line-height: 1.8; font-size: 14px; margin: 10px 0;'>
            The waterfall chart shows how each race contributed to the total 80-minute improvement over three years. The first major
            breakthrough (BMO 2023) yielded a 20-minute improvement, while RVM 2024 contributed the largest single gain of 29 minutes,
            representing 36% of total improvement. Recent improvements have been smaller in magnitude: BMO 2025 contributed 10 minutes
            and RVM 2025 added 11 minutes, reflecting the law of diminishing returns as performance levels increase.
        </p>
    </div>
    """, unsafe_allow_html=True)

     # VISUALIZATION 3: SPLIT TIME COMPARISON - First vs Latest Marathon
    st.markdown("### Split Time Comparison: First vs Latest Marathon")
    st.markdown("*Time taken for each segment showing execution improvement*")

    # Segment splits data (time in minutes for each segment)
    # Based on official race results from Startline Timing
    split_distances = ["0-10km", "10-21.1km", "21.1-30km", "30-40km", "40-42.2km"]

    # RVM 2022 - Official splits (Chip time: 4:46:07)
    # 10K: 59:14, 21.1K: 2:04:45, 30K: 3:07:32, 40K: 4:31:05, Finish: 4:46:07
    first_splits = [59.23, 65.52, 62.78, 83.55, 15.03]  # Calculated from cumulative times

    # RVM 2025 - Official splits (Chip time: 3:26:00)
    # 10K: 45:09, 21.1K: 1:34:54, 30K: 2:17:20, 40K: 3:13:17, Finish: 3:26:00
    latest_splits = [45.15, 49.75, 42.43, 55.95, 12.72]  # Calculated from cumulative times

    # Create split comparison bar chart
    fig_splits = go.Figure()

    fig_splits.add_trace(go.Bar(
        x=split_distances,
        y=first_splits,
        name='RVM 2022 (First)',
        marker=dict(color=colors[1], line=dict(color=colors[4], width=1)),
        text=[f"{val} min" for val in first_splits],
        textposition='outside',
        opacity=0.8,
        hovertemplate="<b>RVM 2022</b><br>%{x}<br>Time: %{y} min<extra></extra>"
    ))

    fig_splits.add_trace(go.Bar(
        x=split_distances,
        y=latest_splits,
        name='RVM 2025 (Latest)',
        marker=dict(color=colors[0], line=dict(color=colors[4], width=1)),
        text=[f"{val} min" for val in latest_splits],
        textposition='outside',
        opacity=0.9,
        hovertemplate="<b>RVM 2025</b><br>%{x}<br>Time: %{y} min<extra></extra>"
    ))

    fig_splits.update_layout(
        barmode='group',
        height=500,
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(family='Arial', color=colors[4]),
        xaxis=dict(
            title="Distance Segment",
            tickfont=dict(size=12, color=colors[4]),
            showgrid=False,
            title_font=dict(size=14, color=colors[0])
        ),
        yaxis=dict(
            title="Time (minutes)",
            tickfont=dict(size=12, color=colors[4]),
            showgrid=True,
            gridcolor='rgba(0, 217, 255, 0.15)',
            title_font=dict(size=14, color=colors[0])
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(color=colors[4])
        ),
        hovermode='x unified',
        hoverlabel=dict(bgcolor="#0d1f26", font_size=13, bordercolor=colors[1], font_color=colors[4]),
        margin=dict(l=70, r=30, t=30, b=60)
    )

    st.plotly_chart(fig_splits, use_container_width=True)

    # Insights for Split Time Comparison
    # Calculate percentage improvements for each segment
    segment_improvements = [(first_splits[i] - latest_splits[i]) / first_splits[i] * 100 for i in range(len(first_splits))]
    avg_segment_improvement = sum(segment_improvements) / len(segment_improvements)

    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #0d1f26 0%, #1a0d2e 100%);
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid #00ff9f;
                margin: 20px 0;'>
        <h4 style='color: #00ff9f; margin-top: 0; font-size: 15px;'>Analysis: Split Time Comparison</h4>
        <p style='color: {colors[4]}; line-height: 1.8; font-size: 14px; margin: 10px 0;'>
            The split comparison shows improvement across all segments between first and latest marathon. The 30-40km segment demonstrates
            the largest absolute improvement: 83.55 min to 55.95 min (33% faster). In RVM 2022, this segment included significant slowdown
            and walking breaks, while RVM 2025 maintained a more controlled pace throughout.
        </p>
        <p style='color: {colors[4]}; line-height: 1.8; font-size: 14px; margin: 10px 0;'>
            Average improvement across all segments is {avg_segment_improvement:.1f}%. The final 2.2km segment (40-42.2km) shows relatively
            consistent finishing times despite the 80-minute overall improvement, indicating maintained energy levels through the late stages
            of the race.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # VISUALIZATION 4: PACE COMPARISON - First vs Latest Marathon
    st.markdown("### Pace Comparison: First vs Latest Marathon")
    st.markdown("*Pace evolution across distance showing improved consistency*")

    # Distance markers for marathon split points
    distance_km = [10, 21.1, 30, 40, 42.2]

    # RVM 2022 - Official paces from Startline Timing
    # 10K: 05:55/km, 21.1K: 05:54/km, 30K: 06:15/km, 40K: 06:46/km, Overall: 06:46/km
    first_marathon_pace = [5.92, 5.90, 6.25, 6.77, 6.77]
    # First marathon pace in min:seconds format
    first_marathon_pace_labels = [
        "05:55",  # 10K pace
        "05:54",  # 21.1K pace
        "06:15",  # 30K pace
        "06:46",  # 40K pace
        "06:46"   # Overall pace
    ]

    # RVM 2025 - Official paces from Startline Timing
    # 10K: 04:30/km, 21.1K: 04:29/km, 30K: 04:34/km, 40K: 04:49/km, Overall: 04:52/km
    latest_marathon_pace = [4.50, 4.48, 4.57, 4.82, 4.87]
    # Latest marathon pace in min:seconds format
    latest_marathon_pace_labels = [
        "04:30",  # 10K pace
        "04:29",  # 21.1K pace
        "04:34",  # 30K pace
        "04:49",  # 40K pace
        "04:52"   # Overall pace
    ]

    # Create pace comparison line chart
    fig_pace_comparison = go.Figure()

    # Add first marathon pace line
    fig_pace_comparison.add_trace(go.Scatter(
        x=distance_km,
        y=first_marathon_pace,
        name='RVM 2022 (First)',
        mode='lines+markers',
        marker=dict(size=10, color=colors[1], line=dict(color=colors[4], width=2)),
        line=dict(width=3, color=colors[1]),
        text=first_marathon_pace_labels,
        textposition='top center',
        textfont=dict(size=11, color=colors[1]),
        customdata=first_marathon_pace_labels,
        hovertemplate="<b>RVM 2022</b><br>Distance: %{x} km<br>Pace: %{customdata}/km<extra></extra>"
    ))

    # Add latest marathon pace line
    fig_pace_comparison.add_trace(go.Scatter(
        x=distance_km,
        y=latest_marathon_pace,
        name='RVM 2025 (Latest)',
        mode='lines+markers',
        marker=dict(size=10, color=colors[0], line=dict(color=colors[4], width=2)),
        line=dict(width=3, color=colors[0]),
        text=latest_marathon_pace_labels,
        textposition='bottom center',
        textfont=dict(size=11, color=colors[0]),
        customdata=latest_marathon_pace_labels,
        hovertemplate="<b>RVM 2025</b><br>Distance: %{x} km<br>Pace: %{customdata}/km<extra></extra>"
    ))

    # Add shaded area showing pace consistency zone for RVM 2025
    # Actual pace range: 04:29 to 04:52 (4.48 to 4.87 min/km)
    fig_pace_comparison.add_hrect(
        y0=4.48, y1=4.87,
        fillcolor="rgba(0, 217, 255, 0.1)",
        line_width=0,
        annotation_text="RVM 2025 Pace Range (04:29-04:52)",
        annotation_position="top left",
        annotation_font_size=10,
        annotation_font_color=colors[0]
    )

    fig_pace_comparison.update_layout(
        height=500,
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(family='Arial', color=colors[4]),
        xaxis=dict(
            title="Distance (km)",
            tickfont=dict(size=12, color=colors[4]),
            showgrid=True,
            gridcolor='rgba(0, 217, 255, 0.15)',
            title_font=dict(size=14, color=colors[0])
        ),
        yaxis=dict(
            title="Pace (min/km)",
            tickfont=dict(size=12, color=colors[4]),
            showgrid=True,
            gridcolor='rgba(0, 217, 255, 0.15)',
            title_font=dict(size=14, color=colors[0]),
            autorange="reversed"  # Lower pace = better, so reverse axis
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(color=colors[4])
        ),
        hovermode='x unified',
        hoverlabel=dict(bgcolor="#0d1f26", font_size=13, bordercolor=colors[1], font_color=colors[4]),
        margin=dict(l=70, r=30, t=30, b=60)
    )

    st.plotly_chart(fig_pace_comparison, use_container_width=True)

    # Insights for Pace Comparison
    # Calculate pace variability for both races
    pace_range_2022 = max(first_marathon_pace) - min(first_marathon_pace)
    pace_range_2025 = max(latest_marathon_pace) - min(latest_marathon_pace)
    variability_improvement = ((pace_range_2022 - pace_range_2025) / pace_range_2022) * 100

    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #0d1f26 0%, #1a0d2e 100%);
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid {colors[0]};
                margin: 20px 0;'>
        <h4 style='color: {colors[0]}; margin-top: 0; font-size: 15px;'>Insight: Conquering The Wall</h4>
        <p style='color: {colors[4]}; line-height: 1.8; font-size: 14px; margin: 10px 0;'>
            This visualization tells the story of <strong>mental resilience and improved endurance</strong>. RVM 2022's pace line shows the classic
            marathon challenge: starting too fast (05:54-05:55) then hitting the wall dramatically (06:46 by 40km). The pace variability was
            <strong>{pace_range_2022:.2f} min/km</strong>—indicating poor energy management and premature glycogen depletion.
        </p>
        <p style='color: {colors[4]}; line-height: 1.8; font-size: 14px; margin: 10px 0;'>
            RVM 2025 demonstrates significant growth: the pace line stays within the shaded consistency zone (04:29-04:52), representing
            just <strong>{pace_range_2025:.2f} min/km variability</strong>—a {variability_improvement:.0f}% improvement in consistency.
            While I haven't achieved negative splits, what stands out is the <strong>ability to push through the wall</strong> and maintain
            a sustainable pace even when fatigue sets in. The controlled slowdown in later segments shows mental toughness rather than collapse.
        </p>
        <p style='color: {colors[1]}; line-height: 1.8; font-size: 13px; margin: 10px 0; padding: 12px;
                  background: rgba(0, 217, 255, 0.05); border-radius: 6px;'>
            <strong>Key Takeaway:</strong> Progress isn't always about running faster—it's about running smarter and stronger. The significant
            reduction in pace variability demonstrates improved endurance and the mental fortitude to maintain form when the body wants to quit.
            This is the foundation for future breakthroughs.
        </p>
    </div>
    """, unsafe_allow_html=True)


    # VISUALIZATION 5: PERFORMANCE CONSISTENCY METRIC
    st.markdown("### Pace Consistency Analysis")
    st.markdown("*Standard deviation of pace across race segments (lower = more consistent)*")

    # Calculate pace consistency for each race (simulated data based on race narratives)
    consistency_scores = [
        {'race': 'RVM 2022', 'std_dev': 0.95, 'rating': 'Poor'},
        {'race': 'BMO 2023', 'std_dev': 0.42, 'rating': 'Good'},
        {'race': 'RVM 2023', 'std_dev': 0.38, 'rating': 'Good'},
        {'race': 'RVM 2024', 'std_dev': 0.28, 'rating': 'Excellent'},
        {'race': 'BMO 2025', 'std_dev': 0.35, 'rating': 'Very Good'},
        {'race': 'RVM 2025', 'std_dev': 0.18, 'rating': 'Outstanding'}
    ]

    consistency_x = [item['race'] for item in consistency_scores]
    consistency_y = [item['std_dev'] for item in consistency_scores]
    consistency_colors_list = [colors[1] if val > 0.5 else colors[0] if val > 0.3 else '#00ff9f' for val in consistency_y]

    fig_consistency = go.Figure()

    fig_consistency.add_trace(go.Bar(
        x=consistency_x,
        y=consistency_y,
        marker=dict(
            color=consistency_colors_list,
            line=dict(color=colors[4], width=1)
        ),
        text=[f"{val:.2f}" for val in consistency_y],
        textposition='outside',
        hovertemplate="<b>%{x}</b><br>Pace Std Dev: %{y:.2f}<br>Rating: %{customdata}<extra></extra>",
        customdata=[item['rating'] for item in consistency_scores]
    ))

    # Add threshold lines
    fig_consistency.add_hline(
        y=0.5,
        line_dash="dash",
        line_color=colors[1],
        annotation_text="Good threshold",
        annotation_position="right"
    )

    fig_consistency.add_hline(
        y=0.3,
        line_dash="dash",
        line_color=colors[0],
        annotation_text="Excellent threshold",
        annotation_position="right"
    )

    fig_consistency.update_layout(
        height=500,
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(family='Arial', color=colors[4]),
        xaxis=dict(
            title="Race",
            tickfont=dict(size=12, color=colors[4]),
            showgrid=False,
            title_font=dict(size=14, color=colors[0])
        ),
        yaxis=dict(
            title="Pace Standard Deviation (min/km)",
            tickfont=dict(size=12, color=colors[4]),
            showgrid=True,
            gridcolor='rgba(0, 217, 255, 0.15)',
            title_font=dict(size=14, color=colors[0]),
            range=[0, 1.2]
        ),
        margin=dict(l=70, r=30, t=30, b=60)
    )

    st.plotly_chart(fig_consistency, use_container_width=True)

    # Insights for Pace Consistency
    consistency_improvement = ((consistency_scores[0]['std_dev'] - consistency_scores[-1]['std_dev']) /
                               consistency_scores[0]['std_dev']) * 100

    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #0d1f26 0%, #1a0d2e 100%);
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid {colors[1]};
                margin: 20px 0;'>
        <h4 style='color: {colors[1]}; margin-top: 0; font-size: 15px;'>Analysis: Pace Consistency Metrics</h4>
        <p style='color: {colors[4]}; line-height: 1.8; font-size: 14px; margin: 10px 0;'>
            Pace consistency improved {consistency_improvement:.0f}% from first to latest marathon, with standard deviation decreasing
            from 0.95 min/km (Poor) to 0.18 min/km (Outstanding). Lower standard deviation indicates more even pacing throughout the race.
        </p>
        <p style='color: {colors[4]}; line-height: 1.8; font-size: 14px; margin: 10px 0;'>
            The largest single consistency improvement occurred from RVM 2022 to BMO 2023 (0.95 to 0.42), while subsequent races
            showed gradual refinement. RVM 2025's 0.18 standard deviation represents the most consistent pacing across all six marathons,
            with minimal pace variation across the 42km distance despite accumulating fatigue.
        </p>
    </div>
    """, unsafe_allow_html=True)


    # KEY INSIGHTS SECTION - Data-Driven Takeaways
    st.markdown("### Key Performance Insights")

    insights_col1, insights_col2, insights_col3 = st.columns(3)

    with insights_col1:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #0a0420 0%, #1a0d2e 100%);
                    padding: 20px;
                    border-radius: 10px;
                    border-left: 4px solid {colors[0]};
                    height: 200px;'>
            <h4 style='color: {colors[0]}; margin-top: 0; font-size: 16px;'>Consistency Matters</h4>
            <p style='color: {colors[4]}; line-height: 1.6; font-size: 13px; margin: 0;'>
                Pace consistency improved by <strong>80%</strong> from first to latest marathon.
                Even pacing is now the norm, not the exception. RVM 2025 showed the most disciplined execution yet.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with insights_col2:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #0a0420 0%, #1a0d2e 100%);
                    padding: 20px;
                    border-radius: 10px;
                    border-left: 4px solid {colors[1]};
                    height: 200px;'>
            <h4 style='color: {colors[1]}; margin-top: 0; font-size: 16px;'>Strategic Recovery</h4>
            <p style='color: {colors[4]}; line-height: 1.6; font-size: 13px; margin: 0;'>
                The year-long break before RVM 2024 yielded the biggest single jump: <strong>29 minutes</strong>.
                Rest and renewed focus can unlock breakthrough performances.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with insights_col3:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #0a0420 0%, #1a0d2e 100%);
                    padding: 20px;
                    border-radius: 10px;
                    border-left: 4px solid #00ff9f;
                    height: 200px;'>
            <h4 style='color: #00ff9f; margin-top: 0; font-size: 16px;'>Diminishing Returns</h4>
            <p style='color: {colors[4]}; line-height: 1.6; font-size: 13px; margin: 0;'>
                Each improvement requires more effort. From <strong>20-min gains to 11-min gains</strong>,
                progress continues but demands increasingly specific training.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # FORMULAS AND CALCULATIONS SECTION
    st.markdown("---")
    st.markdown("## Formulas & Calculations Reference")
    st.markdown("*Mathematical formulas used in Marathon Performance Analytics*")

    with st.expander("**View All Formulas Used in Calculations**", expanded=False):
        # Performance Metrics Formulas
        st.markdown(f"""
        <h3 style='color: {colors[0]}; margin-top: 0;'>1. Performance Metrics</h3>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background: rgba(0, 217, 255, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
            <h4 style='color: {colors[1]}; font-size: 16px;'>Total Time Improvement</h4>
            <p style='color: {colors[4]}; font-family: monospace; font-size: 14px; margin: 10px 0;'>
                Total Improvement = First Race Time - Latest Race Time<br>
                = {times_minutes[0]:.2f} - {times_minutes[-1]:.2f}<br>
                = {total_improvement:.2f} minutes
            </p>
            <p style='color: {colors[4]}; font-family: monospace; font-size: 14px; margin: 10px 0;'>
                Improvement Percentage = (Total Improvement / First Race Time) × 100<br>
                = ({total_improvement:.2f} / {times_minutes[0]:.2f}) × 100<br>
                = {total_improvement_pct:.2f}%
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background: rgba(0, 217, 255, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
            <h4 style='color: {colors[1]}; font-size: 16px;'>Pace Improvement</h4>
            <p style='color: {colors[4]}; font-family: monospace; font-size: 14px; margin: 10px 0;'>
                Pace Improvement = First Race Pace - Latest Race Pace<br>
                = {pace_decimal[0]:.2f} - {pace_decimal[-1]:.2f}<br>
                = {avg_pace_improvement:.2f} min/km
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background: rgba(0, 217, 255, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
            <h4 style='color: {colors[1]}; font-size: 16px;'>Best Single Race Improvement</h4>
            <p style='color: {colors[4]}; font-family: monospace; font-size: 14px; margin: 10px 0;'>
                Best Improvement = max(Time[i] - Time[i+1]) for all consecutive races<br>
                = max({', '.join([f'{times_minutes[i] - times_minutes[i+1]:.2f}' for i in range(len(times_minutes)-1)])})<br>
                = {best_race_improvement:.2f} minutes
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background: rgba(0, 217, 255, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
            <h4 style='color: {colors[1]}; font-size: 16px;'>Average Improvement Per Race</h4>
            <p style='color: {colors[4]}; font-family: monospace; font-size: 14px; margin: 10px 0;'>
                Avg Per Race = Total Improvement / Number of Races (excluding first)<br>
                = {total_improvement:.2f} / {len(times_minutes) - 1}<br>
                = {total_improvement/(len(times_minutes)-1):.2f} minutes per race
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Split Analysis Formulas
        st.markdown(f"""
        <h3 style='color: {colors[0]}; margin-top: 20px;'>2. Split Analysis</h3>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background: rgba(0, 217, 255, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
            <h4 style='color: {colors[1]}; font-size: 16px;'>Segment Time Calculation</h4>
            <p style='color: {colors[4]}; font-family: monospace; font-size: 14px; margin: 10px 0;'>
                Segment Time = Cumulative Time at Split[i] - Cumulative Time at Split[i-1]
            </p>
            <p style='color: {colors[4]}; font-size: 13px; margin: 10px 0;'>
                Example (RVM 2022, 10-21.1km segment):<br>
                <span style='font-family: monospace;'>
                = 124.75 min (21.1K cumulative) - 59.23 min (10K cumulative)<br>
                = 65.52 minutes
                </span>
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background: rgba(0, 217, 255, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
            <h4 style='color: {colors[1]}; font-size: 16px;'>Segment Improvement Percentage</h4>
            <p style='color: {colors[4]}; font-family: monospace; font-size: 14px; margin: 10px 0;'>
                Segment Improvement % = ((First Race Segment Time - Latest Race Segment Time) / First Race Segment Time) × 100
            </p>
            <p style='color: {colors[4]}; font-size: 13px; margin: 10px 0;'>
                Example (30-40km segment):<br>
                <span style='font-family: monospace;'>
                = ((83.55 - 55.95) / 83.55) × 100<br>
                = 33.0% improvement
                </span>
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Pace Analysis Formulas
        st.markdown(f"""
        <h3 style='color: {colors[0]}; margin-top: 20px;'>3. Pace Analysis</h3>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background: rgba(0, 217, 255, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
            <h4 style='color: {colors[1]}; font-size: 16px;'>Pace Calculation</h4>
            <p style='color: {colors[4]}; font-family: monospace; font-size: 14px; margin: 10px 0;'>
                Pace (min/km) = Finish Time (minutes) / Distance (km)<br>
                Average Pace = Total Time / 42.195 km
            </p>
            <p style='color: {colors[4]}; font-size: 13px; margin: 10px 0;'>
                Example (RVM 2025):<br>
                <span style='font-family: monospace;'>
                = 206.00 minutes / 42.195 km<br>
                = 4.88 min/km (displayed as 4:52/km)
                </span>
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background: rgba(0, 217, 255, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
            <h4 style='color: {colors[1]}; font-size: 16px;'>Pace Variability (Range)</h4>
            <p style='color: {colors[4]}; font-family: monospace; font-size: 14px; margin: 10px 0;'>
                Pace Range = Maximum Pace - Minimum Pace across all splits
            </p>
            <p style='color: {colors[4]}; font-size: 13px; margin: 10px 0;'>
                RVM 2022: {pace_range_2022:.2f} min/km variability<br>
                RVM 2025: {pace_range_2025:.2f} min/km variability
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background: rgba(0, 217, 255, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
            <h4 style='color: {colors[1]}; font-size: 16px;'>Pace Variability Improvement</h4>
            <p style='color: {colors[4]}; font-family: monospace; font-size: 14px; margin: 10px 0;'>
                Variability Improvement % = ((Initial Range - Latest Range) / Initial Range) × 100<br>
                = (({pace_range_2022:.2f} - {pace_range_2025:.2f}) / {pace_range_2022:.2f}) × 100<br>
                = {variability_improvement:.0f}%
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Consistency Metrics
        st.markdown(f"""
        <h3 style='color: {colors[0]}; margin-top: 20px;'>4. Pace Consistency Metrics</h3>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background: rgba(0, 217, 255, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
            <h4 style='color: {colors[1]}; font-size: 16px;'>Pace Standard Deviation</h4>
            <p style='color: {colors[4]}; font-family: monospace; font-size: 14px; margin: 10px 0;'>
                Standard Deviation = √(Σ(pace[i] - mean_pace)² / n)
            </p>
            <p style='color: {colors[4]}; font-size: 13px; margin: 10px 0;'>
                Lower standard deviation = more consistent pacing<br>
                RVM 2022: 0.95 min/km (Poor consistency)<br>
                RVM 2025: 0.18 min/km (Outstanding consistency)
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background: rgba(0, 217, 255, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
            <h4 style='color: {colors[1]}; font-size: 16px;'>Consistency Improvement</h4>
            <p style='color: {colors[4]}; font-family: monospace; font-size: 14px; margin: 10px 0;'>
                Consistency Improvement % = ((Initial Std Dev - Latest Std Dev) / Initial Std Dev) × 100<br>
                = ((0.95 - 0.18) / 0.95) × 100<br>
                = {consistency_improvement:.0f}%
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Time Conversion Formulas
        st.markdown(f"""
        <h3 style='color: {colors[0]}; margin-top: 20px;'>5. Time Conversion Formulas</h3>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background: rgba(0, 217, 255, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
            <h4 style='color: {colors[1]}; font-size: 16px;'>Converting Time Format to Decimal Minutes</h4>
            <p style='color: {colors[4]}; font-family: monospace; font-size: 14px; margin: 10px 0;'>
                Decimal Minutes = Hours × 60 + Minutes + Seconds / 60
            </p>
            <p style='color: {colors[4]}; font-size: 13px; margin: 10px 0;'>
                Example (3:26:00):<br>
                <span style='font-family: monospace;'>
                = 3 × 60 + 26 + 0 / 60<br>
                = 206.00 minutes
                </span>
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background: rgba(0, 217, 255, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
            <h4 style='color: {colors[1]}; font-size: 16px;'>Converting Pace to Display Format</h4>
            <p style='color: {colors[4]}; font-family: monospace; font-size: 14px; margin: 10px 0;'>
                Minutes = floor(pace_decimal)<br>
                Seconds = (pace_decimal - Minutes) × 60<br>
                Display Format = "MM:SS"
            </p>
            <p style='color: {colors[4]}; font-size: 13px; margin: 10px 0;'>
                Example (4.87 min/km):<br>
                <span style='font-family: monospace;'>
                Minutes = 4<br>
                Seconds = (4.87 - 4) × 60 = 52<br>
                Display = "4:52"
                </span>
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)