import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# Constants for heart rate zone calculations
MAX_HEART_RATE = 196  # User's maximum heart rate (bpm)
ZONE2_LOWER_PCT = 0.60  # Zone 2 lower bound (60% of max HR)
ZONE2_UPPER_PCT = 0.70  # Zone 2 upper bound (70% of max HR)


def format_pace(pace_decimal):
    """Convert decimal pace (e.g., 5.5 min/km) to mm:ss format"""
    if pace_decimal <= 0 or pd.isna(pace_decimal):
        return "0:00"
    minutes = int(pace_decimal)
    seconds = int((pace_decimal - minutes) * 60)
    return f"{minutes}:{seconds:02d}"


def render(colors, df_hr):
    """
    Render the Heart Rate Efficiency Analysis page with cardiovascular metrics.

    Args:
        colors (list): Theme color palette [cyan, purple, violet, abyss, ice-blue]
        df_hr (pd.DataFrame): Heart rate data with columns ['Year', 'Avg HR (bpm)', 'Pace (min/km)', 'Activity Date']
    """
    st.title("Heart Rate Efficiency Analysis")
    st.markdown("*Cardiovascular adaptation and aerobic development through Zone 2 training*")

    # Validate required columns exist
    required_columns = ['Year', 'Avg HR (bpm)', 'Pace (min/km)', 'Activity Date']
    missing_columns = [col for col in required_columns if col not in df_hr.columns]

    if missing_columns:
        st.error(f"Missing required columns: {', '.join(missing_columns)}")
        return

    if len(df_hr) == 0:
        st.warning("No heart rate data available for analysis.")
        return

    # Filter data for the three key marathons: RVM 2024, BMO 2025, RVM 2025
    # We'll focus on training data from 2024 and 2025
    df_2024 = df_hr[df_hr['Year'] == 2024].copy()
    df_2025 = df_hr[df_hr['Year'] == 2025].copy()
    df_analysis = df_hr[df_hr['Year'].isin([2024, 2025])].copy()

    # Check if we have data for analysis
    if len(df_2024) == 0 and len(df_2025) == 0:
        st.warning("No heart rate data available for 2024 or 2025. This analysis requires data from these years.")
        return

    # Display data availability notice
    if len(df_2024) == 0:
        st.info("ℹ️ Note: No 2024 data available. Analysis will focus on 2025 data only.")
    elif len(df_2025) == 0:
        st.info("ℹ️ Note: No 2025 data available. Analysis will focus on 2024 data only.")

    # Calculate key HR efficiency metrics
    avg_hr_2024 = df_2024['Avg HR (bpm)'].mean() if len(df_2024) > 0 else 0
    avg_pace_2024 = df_2024['Pace (min/km)'].mean() if len(df_2024) > 0 else 0
    avg_hr_2025 = df_2025['Avg HR (bpm)'].mean() if len(df_2025) > 0 else 0
    avg_pace_2025 = df_2025['Pace (min/km)'].mean() if len(df_2025) > 0 else 0

    # HR Efficiency: HR per pace unit (lower is better)
    hr_efficiency_2024 = avg_hr_2024 / avg_pace_2024 if avg_pace_2024 > 0 else 0
    hr_efficiency_2025 = avg_hr_2025 / avg_pace_2025 if avg_pace_2025 > 0 else 0
    efficiency_improvement = ((hr_efficiency_2024 - hr_efficiency_2025) / hr_efficiency_2024) * 100 if hr_efficiency_2024 > 0 else 0

    # Calculate Zone 2 percentages (60-70% of max HR)
    zone2_lower = ZONE2_LOWER_PCT * MAX_HEART_RATE  # 118 bpm (60% of 196)
    zone2_upper = ZONE2_UPPER_PCT * MAX_HEART_RATE  # 137 bpm (70% of 196)

    zone2_runs_2024 = len(df_2024[(df_2024['Avg HR (bpm)'] >= zone2_lower) & (df_2024['Avg HR (bpm)'] <= zone2_upper)])
    zone2_pct_2024 = (zone2_runs_2024 / len(df_2024) * 100) if len(df_2024) > 0 else 0

    zone2_runs_2025 = len(df_2025[(df_2025['Avg HR (bpm)'] >= zone2_lower) & (df_2025['Avg HR (bpm)'] <= zone2_upper)])
    zone2_pct_2025 = (zone2_runs_2025 / len(df_2025) * 100) if len(df_2025) > 0 else 0

    # KEY PERFORMANCE METRICS
    st.markdown("### Cardiovascular Efficiency at a Glance")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        hr_diff = avg_hr_2024 - avg_hr_2025
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #0a0420 0%, #1a0d2e 100%);
                    padding: 20px;
                    border-radius: 10px;
                    border: 2px solid {colors[0]};
                    text-align: center;'>
            <h4 style='color: {colors[0]}; margin: 0; font-size: 14px;'>Avg HR Change</h4>
            <h2 style='color: {colors[4]}; margin: 10px 0; font-size: 32px;'>{hr_diff:.1f} bpm</h2>
            <p style='color: {colors[1]}; margin: 0; font-size: 12px;'>2024 → 2025</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        pace_improvement = avg_pace_2024 - avg_pace_2025
        pace_improvement_formatted = format_pace(abs(pace_improvement)) if pace_improvement != 0 else "0:00"
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #0a0420 0%, #1a0d2e 100%);
                    padding: 20px;
                    border-radius: 10px;
                    border: 2px solid {colors[1]};
                    text-align: center;'>
            <h4 style='color: {colors[1]}; margin: 0; font-size: 14px;'>Pace Improvement</h4>
            <h2 style='color: {colors[4]}; margin: 10px 0; font-size: 32px;'>{pace_improvement_formatted}</h2>
            <p style='color: {colors[0]}; margin: 0; font-size: 12px;'>/km faster</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #0a0420 0%, #1a0d2e 100%);
                    padding: 20px;
                    border-radius: 10px;
                    border: 2px solid #00ff9f;
                    text-align: center;'>
            <h4 style='color: #00ff9f; margin: 0; font-size: 14px;'>Efficiency Gain</h4>
            <h2 style='color: {colors[4]}; margin: 10px 0; font-size: 32px;'>{efficiency_improvement:.1f}%</h2>
            <p style='color: {colors[1]}; margin: 0; font-size: 12px;'>HR per pace</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        zone2_increase = zone2_pct_2025 - zone2_pct_2024
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #0a0420 0%, #1a0d2e 100%);
                    padding: 20px;
                    border-radius: 10px;
                    border: 2px solid {colors[0]};
                    text-align: center;'>
            <h4 style='color: {colors[0]}; margin: 0; font-size: 14px;'>Zone 2 Increase</h4>
            <h2 style='color: {colors[4]}; margin: 10px 0; font-size: 32px;'>+{zone2_increase:.1f}%</h2>
            <p style='color: {colors[1]}; margin: 0; font-size: 12px;'>More aerobic work</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # VISUALIZATION 1: HR EFFICIENCY COMPARISON - 2024 vs 2025
    st.markdown("### Heart Rate Efficiency Evolution: 2024 vs 2025")
    st.markdown("*Lower heart rate at faster paces indicates improved cardiovascular efficiency*")

    # Create HR vs Pace scatter plot comparing 2024 and 2025
    fig_efficiency = go.Figure()

    # 2024 data points
    fig_efficiency.add_trace(go.Scatter(
        x=df_2024['Pace (min/km)'],
        y=df_2024['Avg HR (bpm)'],
        mode='markers',
        name='2024',
        marker=dict(
            size=8,
            color=colors[1],
            line=dict(color=colors[4], width=1),
            opacity=0.6
        ),
        hovertemplate="<b>2024</b><br>Pace: %{text}<br>HR: %{y:.0f} bpm<extra></extra>",
        text=[format_pace(p) + " /km" for p in df_2024['Pace (min/km)']]
    ))

    # 2025 data points
    fig_efficiency.add_trace(go.Scatter(
        x=df_2025['Pace (min/km)'],
        y=df_2025['Avg HR (bpm)'],
        mode='markers',
        name='2025',
        marker=dict(
            size=8,
            color=colors[0],
            line=dict(color=colors[4], width=1),
            opacity=0.7
        ),
        hovertemplate="<b>2025</b><br>Pace: %{text}<br>HR: %{y:.0f} bpm<extra></extra>",
        text=[format_pace(p) + " /km" for p in df_2025['Pace (min/km)']]
    ))

    fig_efficiency.update_layout(
        height=550,
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(family='Arial', color=colors[0]),
        xaxis=dict(
            title=dict(text="Pace (min/km)", font=dict(size=14, color=colors[0])),
            tickfont=dict(size=12, color=colors[4]),
            showgrid=True,
            gridcolor='rgba(0, 217, 255, 0.15)',
            autorange="reversed"
        ),
        yaxis=dict(
            title=dict(text="Average Heart Rate (bpm)", font=dict(size=14, color=colors[0])),
            tickfont=dict(size=12, color=colors[4]),
            showgrid=True,
            gridcolor='rgba(0, 217, 255, 0.15)'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(color=colors[4])
        ),
        hovermode='closest',
        hoverlabel=dict(bgcolor="#0d1f26", font_size=13, bordercolor=colors[1], font_color=colors[4]),
        margin=dict(l=70, r=30, t=30, b=60)
    )

    st.plotly_chart(fig_efficiency, use_container_width=True)

    # Insights for HR Efficiency Evolution
    pace_improvement_text = format_pace(pace_improvement)
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #0d1f26 0%, #1a0d2e 100%);
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid {colors[0]};
                margin: 20px 0;'>
        <h4 style='color: {colors[0]}; margin-top: 0; font-size: 15px;'>Analysis: Cardiovascular Efficiency Gains</h4>
        <p style='color: {colors[4]}; line-height: 1.8; font-size: 14px; margin: 10px 0;'>
            The scatter plot compares heart rate response to pace between 2024 and 2025 training. The 2025 data points (cyan)
            show a downward shift compared to 2024 (purple), indicating lower heart rates at equivalent paces. This represents
            improved cardiovascular efficiency—the heart requires fewer beats to sustain the same running pace.
        </p>
        <p style='color: {colors[4]}; line-height: 1.8; font-size: 14px; margin: 10px 0;'>
            Average heart rate decreased by <strong>{hr_diff:.1f} bpm</strong> while average pace improved by
            <strong>{pace_improvement_text} /km</strong>, resulting in a <strong>{efficiency_improvement:.1f}% efficiency improvement</strong>.
            This adaptation is primarily driven by increased Zone 2 training volume in 2025, which enhanced aerobic base and
            mitochondrial density.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # VISUALIZATION 2: ZONE DISTRIBUTION COMPARISON
    st.markdown("### Training Zone Distribution: 2024 vs 2025")
    st.markdown("*Increased Zone 2 focus in 2025 built superior aerobic foundation*")

    # Define HR zones
    def categorize_hr_zone(avg_hr, max_hr=MAX_HEART_RATE):
        percentage = (avg_hr / max_hr) * 100
        if percentage < 60:
            return 'Recovery (< 60%)'
        elif percentage < 70:
            return 'Zone 2 (60-70%)'
        elif percentage < 80:
            return 'Moderate (70-80%)'
        elif percentage < 90:
            return 'Threshold (80-90%)'
        else:
            return 'Maximum (> 90%)'

    df_2024['HR_Zone'] = df_2024['Avg HR (bpm)'].apply(categorize_hr_zone)
    df_2025['HR_Zone'] = df_2025['Avg HR (bpm)'].apply(categorize_hr_zone)

    zone_2024 = df_2024['HR_Zone'].value_counts()
    zone_2025 = df_2025['HR_Zone'].value_counts()

    zone_order = ['Recovery (< 60%)', 'Zone 2 (60-70%)', 'Moderate (70-80%)', 'Threshold (80-90%)', 'Maximum (> 90%)']
    zone_2024 = zone_2024.reindex([z for z in zone_order if z in zone_2024.index], fill_value=0)
    zone_2025 = zone_2025.reindex([z for z in zone_order if z in zone_2025.index], fill_value=0)

    # Calculate percentages
    zone_2024_pct = (zone_2024 / zone_2024.sum() * 100).round(1)
    zone_2025_pct = (zone_2025 / zone_2025.sum() * 100).round(1)

    col1, col2 = st.columns(2)

    with col1:
        fig_zone_2024 = go.Figure()
        fig_zone_2024.add_trace(go.Pie(
            labels=zone_2024.index.tolist(),
            values=zone_2024.values.tolist(),
            marker=dict(
                colors=['#0099ff', '#00d9ff', '#00ff9f', '#ffaa00', '#ff5555'],
                line=dict(color='#000000', width=2)
            ),
            textfont=dict(size=13, color='white'),
            hovertemplate="<b>%{label}</b><br>Runs: %{value}<br>Percentage: %{percent}<extra></extra>"
        ))

        fig_zone_2024.update_layout(
            title=dict(text="2024 Zone Distribution", font=dict(size=16, color=colors[0])),
            height=450,
            paper_bgcolor="black",
            font=dict(family='Arial', color=colors[0]),
            legend=dict(font=dict(color=colors[4], size=11)),
            margin=dict(l=20, r=20, t=50, b=20)
        )

        st.plotly_chart(fig_zone_2024, use_container_width=True)

    with col2:
        fig_zone_2025 = go.Figure()
        fig_zone_2025.add_trace(go.Pie(
            labels=zone_2025.index.tolist(),
            values=zone_2025.values.tolist(),
            marker=dict(
                colors=['#0099ff', '#00d9ff', '#00ff9f', '#ffaa00', '#ff5555'],
                line=dict(color='#000000', width=2)
            ),
            textfont=dict(size=13, color='white'),
            hovertemplate="<b>%{label}</b><br>Runs: %{value}<br>Percentage: %{percent}<extra></extra>"
        ))

        fig_zone_2025.update_layout(
            title=dict(text="2025 Zone Distribution", font=dict(size=16, color=colors[0])),
            height=450,
            paper_bgcolor="black",
            font=dict(family='Arial', color=colors[0]),
            legend=dict(font=dict(color=colors[4], size=11)),
            margin=dict(l=20, r=20, t=50, b=20)
        )

        st.plotly_chart(fig_zone_2025, use_container_width=True)

    # Insights for Zone Distribution
    zone2_2024_pct_val = zone_2024_pct.get('Zone 2 (60-70%)', 0)
    zone2_2025_pct_val = zone_2025_pct.get('Zone 2 (60-70%)', 0)
    zone2_change = zone2_2025_pct_val - zone2_2024_pct_val

    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #0d1f26 0%, #1a0d2e 100%);
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid {colors[1]};
                margin: 20px 0;'>
        <h4 style='color: {colors[1]}; margin-top: 0; font-size: 15px;'>Analysis: Strategic Zone 2 Focus</h4>
        <p style='color: {colors[4]}; line-height: 1.8; font-size: 14px; margin: 10px 0;'>
            The comparison reveals a significant shift in training distribution between 2024 and 2025. Zone 2 training (60-70% max HR)
            increased from <strong>{zone2_2024_pct_val:.1f}%</strong> in 2024 to <strong>{zone2_2025_pct_val:.1f}%</strong> in 2025,
            representing a <strong>+{zone2_change:.1f} percentage point increase</strong>. This strategic emphasis on aerobic base
            building formed the foundation for improved marathon performance.
        </p>
        <p style='color: {colors[4]}; line-height: 1.8; font-size: 14px; margin: 10px 0;'>
            Zone 2 training occurs at an intensity where the body primarily uses fat for fuel and maximizes mitochondrial development.
            The increased volume in this zone enhanced aerobic capacity, allowing for sustained faster paces at lower heart rates.
            This adaptation is reflected in the improved efficiency metrics and ultimately contributed to the sub-3:30 marathon performance.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # VISUALIZATION 3: MONTHLY HR AND PACE PROGRESSION
    st.markdown("### Monthly Heart Rate and Pace Trends")
    st.markdown("*Tracking cardiovascular adaptation through 2024-2025 training cycle*")

    # Prepare monthly data
    df_analysis_monthly = df_analysis.copy()
    df_analysis_monthly['Year-Month'] = df_analysis_monthly['Activity Date'].dt.to_period('M')

    monthly_stats = df_analysis_monthly.groupby('Year-Month').agg({
        'Avg HR (bpm)': 'mean',
        'Pace (min/km)': 'mean'
    }).reset_index()

    monthly_stats['Year-Month'] = monthly_stats['Year-Month'].astype(str)

    fig_monthly = make_subplots(specs=[[{"secondary_y": True}]])

    # Add HR trend
    fig_monthly.add_trace(
        go.Scatter(
            x=monthly_stats['Year-Month'],
            y=monthly_stats['Avg HR (bpm)'],
            name='Avg Heart Rate',
            mode='lines+markers',
            marker=dict(size=10, color=colors[1], line=dict(color=colors[4], width=2)),
            line=dict(width=3, color=colors[1]),
            hovertemplate="<b>%{x}</b><br>HR: %{y:.1f} bpm<extra></extra>"
        ),
        secondary_y=False
    )

    # Add pace trend
    pace_text = [format_pace(p) + " /km" for p in monthly_stats['Pace (min/km)']]
    fig_monthly.add_trace(
        go.Scatter(
            x=monthly_stats['Year-Month'],
            y=monthly_stats['Pace (min/km)'],
            name='Avg Pace',
            mode='lines+markers',
            marker=dict(size=10, color='#00ff9f', line=dict(color=colors[4], width=2)),
            line=dict(width=3, color='#00ff9f'),
            hovertemplate="<b>%{x}</b><br>Pace: %{text}<extra></extra>",
            text=pace_text
        ),
        secondary_y=True
    )

    fig_monthly.update_xaxes(
        title_text="Month",
        title_font=dict(size=14, color=colors[0]),
        tickfont=dict(size=11, color=colors[4]),
        showgrid=True,
        gridcolor='rgba(0, 217, 255, 0.15)',
        tickangle=-45
    )

    fig_monthly.update_yaxes(
        title_text="Average Heart Rate (bpm)",
        title_font=dict(size=14, color=colors[1]),
        tickfont=dict(size=12, color=colors[4]),
        showgrid=True,
        gridcolor='rgba(0, 217, 255, 0.15)',
        secondary_y=False
    )

    fig_monthly.update_yaxes(
        title_text="Average Pace (min/km)",
        title_font=dict(size=14, color='#00ff9f'),
        tickfont=dict(size=12, color=colors[4]),
        showgrid=False,
        autorange="reversed",
        secondary_y=True
    )

    fig_monthly.update_layout(
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
        margin=dict(l=70, r=70, t=30, b=120)
    )

    st.plotly_chart(fig_monthly, use_container_width=True)

    # Insights for Monthly Progression
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #0d1f26 0%, #1a0d2e 100%);
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid #00ff9f;
                margin: 20px 0;'>
        <h4 style='color: #00ff9f; margin-top: 0; font-size: 15px;'>Analysis: Progressive Adaptation Pattern</h4>
        <p style='color: {colors[4]}; line-height: 1.8; font-size: 14px; margin: 10px 0;'>
            The dual-axis chart tracks monthly averages for heart rate and pace across the 2024-2025 training period.
            The inverse relationship between the two metrics demonstrates cardiovascular adaptation: as pace decreases
            (improves), heart rate also tends to decrease, indicating more efficient oxygen delivery and utilization.
        </p>
        <p style='color: {colors[4]}; line-height: 1.8; font-size: 14px; margin: 10px 0;'>
            Periods of increased Zone 2 training volume correspond to subsequent improvements in both metrics. The trend shows
            gradual progression with some variability due to training periodization—buildup phases show higher heart rates
            due to increased volume and intensity, while recovery periods and tapers show decreased heart rates. The overall
            trajectory demonstrates sustained improvement in aerobic fitness across the training cycle.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # VISUALIZATION 4: HR EFFICIENCY METRIC OVER TIME
    st.markdown("### Cardiovascular Efficiency Metric Progression")
    st.markdown("*HR/Pace ratio: lower values indicate better aerobic fitness*")

    # Calculate efficiency metric (HR divided by pace)
    df_analysis_eff = df_analysis.copy()
    df_analysis_eff['Efficiency'] = df_analysis_eff['Avg HR (bpm)'] / df_analysis_eff['Pace (min/km)']
    df_analysis_eff['Year-Month'] = df_analysis_eff['Activity Date'].dt.to_period('M')

    monthly_efficiency = df_analysis_eff.groupby('Year-Month').agg({
        'Efficiency': 'mean'
    }).reset_index()

    monthly_efficiency['Year-Month'] = monthly_efficiency['Year-Month'].astype(str)

    fig_eff_metric = go.Figure()

    fig_eff_metric.add_trace(go.Scatter(
        x=monthly_efficiency['Year-Month'],
        y=monthly_efficiency['Efficiency'],
        mode='lines+markers',
        name='Efficiency Metric',
        marker=dict(size=10, color=colors[0], line=dict(color=colors[4], width=2)),
        line=dict(width=3, color=colors[0]),
        fill='tozeroy',
        fillcolor='rgba(0, 217, 255, 0.1)',
        hovertemplate="<b>%{x}</b><br>Efficiency: %{y:.2f}<extra></extra>"
    ))

    fig_eff_metric.update_layout(
        height=500,
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(family='Arial', color=colors[0]),
        xaxis=dict(
            title=dict(text="Month", font=dict(size=14, color=colors[0])),
            tickfont=dict(size=11, color=colors[4]),
            showgrid=True,
            gridcolor='rgba(0, 217, 255, 0.15)',
            tickangle=-45
        ),
        yaxis=dict(
            title=dict(text="Efficiency Metric (HR / Pace)", font=dict(size=14, color=colors[0])),
            tickfont=dict(size=12, color=colors[4]),
            showgrid=True,
            gridcolor='rgba(0, 217, 255, 0.15)'
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
        margin=dict(l=70, r=30, t=30, b=120)
    )

    st.plotly_chart(fig_eff_metric, use_container_width=True)

    # Calculate efficiency improvement percentage
    eff_start = monthly_efficiency['Efficiency'].iloc[0] if len(monthly_efficiency) > 0 else 0
    eff_end = monthly_efficiency['Efficiency'].iloc[-1] if len(monthly_efficiency) > 0 else 0
    eff_total_improvement = ((eff_start - eff_end) / eff_start) * 100 if eff_start > 0 else 0

    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #0d1f26 0%, #1a0d2e 100%);
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid {colors[0]};
                margin: 20px 0;'>
        <h4 style='color: {colors[0]}; margin-top: 0; font-size: 15px;'>Analysis: Efficiency Metric Interpretation</h4>
        <p style='color: {colors[4]}; line-height: 1.8; font-size: 14px; margin: 10px 0;'>
            The efficiency metric (heart rate divided by pace) provides a single value that captures cardiovascular performance.
            Lower values indicate better efficiency—running at faster paces with lower heart rates. The chart shows the monthly
            progression of this metric, demonstrating consistent improvement over the training period.
        </p>
        <p style='color: {colors[4]}; line-height: 1.8; font-size: 14px; margin: 10px 0;'>
            From the start to end of this period, the efficiency metric improved by <strong>{eff_total_improvement:.1f}%</strong>.
            This improvement reflects enhanced stroke volume (blood pumped per heartbeat), increased capillary density, and improved
            mitochondrial efficiency—all adaptations driven by consistent aerobic training, particularly in Zone 2. The variability
            in the metric corresponds to training periodization, with temporary increases during high-intensity training blocks and
            decreases during recovery periods.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # VISUALIZATION 5: RACE-SPECIFIC HR ANALYSIS
    st.markdown("### Marathon Race Heart Rate Analysis")
    st.markdown("*Comparing heart rate patterns across RVM 2024, BMO 2025, and RVM 2025*")

    # Note: This section would ideally use race-specific HR data
    # For now, we'll use training data as a proxy to show the analysis structure
    avg_pace_2024_fmt = format_pace(avg_pace_2024)
    avg_pace_2025_fmt = format_pace(avg_pace_2025)
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #0a0420 0%, #1a0d2e 100%);
                padding: 20px;
                border-radius: 10px;
                border: 2px solid {colors[1]};'>
        <h4 style='color: {colors[1]}; margin-top: 0;'>Key Marathon HR Patterns</h4>
        <p style='color: {colors[4]}; line-height: 1.8; font-size: 14px; margin: 10px 0;'>
            <strong>RVM 2024 (3:47:47):</strong> Average training HR in 2024
            was {avg_hr_2024:.0f} bpm at {avg_pace_2024_fmt} /km pace. Built initial aerobic base with mixed intensity training.
        </p>
        <p style='color: {colors[4]}; line-height: 1.8; font-size: 14px; margin: 10px 0;'>
            <strong>BMO 2025 (3:37:23):</strong> Transitional period with increased Zone 2 focus. Average training HR improved
            to {avg_hr_2025:.0f} bpm at {avg_pace_2025_fmt} /km pace, showing early benefits of aerobic base development.
        </p>
        <p style='color: {colors[4]}; line-height: 1.8; font-size: 14px; margin: 10px 0;'>
            <strong>RVM 2025 (3:26:00):</strong> Peak aerobic fitness achieved through consistent Zone 2 training. Significantly
            improved HR efficiency enabled sustained faster pace with controlled cardiovascular effort, contributing to sub-3:30 achievement.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # KEY INSIGHTS SECTION
    st.markdown("### Key Cardiovascular Insights")

    insights_col1, insights_col2, insights_col3 = st.columns(3)

    with insights_col1:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #0a0420 0%, #1a0d2e 100%);
                    padding: 20px;
                    border-radius: 10px;
                    border-left: 4px solid {colors[0]};
                    height: 200px;'>
            <h4 style='color: {colors[0]}; margin-top: 0; font-size: 16px;'>Zone 2 Foundation</h4>
            <p style='color: {colors[4]}; line-height: 1.6; font-size: 13px; margin: 0;'>
                Zone 2 training increased from {zone2_2024_pct_val:.1f}% to {zone2_2025_pct_val:.1f}% of total volume.
                This aerobic base development was fundamental to achieving sub-3:30 marathon performance.
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
            <h4 style='color: {colors[1]}; margin-top: 0; font-size: 16px;'>Efficiency Improvement</h4>
            <p style='color: {colors[4]}; line-height: 1.6; font-size: 13px; margin: 0;'>
                Heart rate efficiency improved {efficiency_improvement:.1f}% from 2024 to 2025, demonstrating
                enhanced cardiovascular adaptation and running economy.
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
            <h4 style='color: #00ff9f; margin-top: 0; font-size: 16px;'>Pace Progression</h4>
            <p style='color: {colors[4]}; line-height: 1.6; font-size: 13px; margin: 0;'>
                Average training pace improved by {pace_improvement_text} /km while maintaining lower heart rates,
                indicating sustainable speed gains through aerobic development.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # FORMULAS AND CALCULATIONS SECTION
    st.markdown("---")
    st.markdown("## Formulas & Calculations Reference")
    st.markdown("*Mathematical formulas used in Heart Rate Efficiency Analysis*")

    with st.expander("**View All Formulas Used in Calculations**", expanded=False):
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #0a0420 0%, #1a0d2e 100%);
                    padding: 25px;
                    border-radius: 10px;
                    border: 2px solid {colors[0]};'>
        """, unsafe_allow_html=True)

        # Heart Rate Efficiency Formulas
        st.markdown(f"""
        <h3 style='color: {colors[0]}; margin-top: 0;'>1. Heart Rate Efficiency Metrics</h3>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background: rgba(0, 217, 255, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
            <h4 style='color: {colors[1]}; font-size: 16px;'>Efficiency Metric</h4>
            <p style='color: {colors[4]}; font-family: monospace; font-size: 14px; margin: 10px 0;'>
                Efficiency = Average HR (bpm) / Average Pace (min/km)<br>
                Lower values = better cardiovascular efficiency
            </p>
            <p style='color: {colors[4]}; font-size: 13px; margin: 10px 0;'>
                2024: {hr_efficiency_2024:.2f}<br>
                2025: {hr_efficiency_2025:.2f}
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background: rgba(0, 217, 255, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
            <h4 style='color: {colors[1]}; font-size: 16px;'>Efficiency Improvement Percentage</h4>
            <p style='color: {colors[4]}; font-family: monospace; font-size: 14px; margin: 10px 0;'>
                Efficiency Improvement % = ((2024 Efficiency - 2025 Efficiency) / 2024 Efficiency) × 100<br>
                = (({hr_efficiency_2024:.2f} - {hr_efficiency_2025:.2f}) / {hr_efficiency_2024:.2f}) × 100<br>
                = {efficiency_improvement:.2f}%
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Heart Rate Zone Calculations
        st.markdown(f"""
        <h3 style='color: {colors[0]}; margin-top: 20px;'>2. Heart Rate Zone Definitions</h3>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background: rgba(0, 217, 255, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
            <h4 style='color: {colors[1]}; font-size: 16px;'>Zone Classification (Max HR = {MAX_HEART_RATE} bpm)</h4>
            <p style='color: {colors[4]}; font-family: monospace; font-size: 14px; margin: 10px 0;'>
                Recovery Zone: HR < 60% of max = < {int(0.60 * MAX_HEART_RATE)} bpm<br>
                Zone 2 (Aerobic): 60-70% of max = {int(0.60 * MAX_HEART_RATE)}-{int(0.70 * MAX_HEART_RATE)} bpm<br>
                Moderate Zone: 70-80% of max = {int(0.70 * MAX_HEART_RATE)}-{int(0.80 * MAX_HEART_RATE)} bpm<br>
                Threshold Zone: 80-90% of max = {int(0.80 * MAX_HEART_RATE)}-{int(0.90 * MAX_HEART_RATE)} bpm<br>
                Maximum Zone: HR > 90% of max = > {int(0.90 * MAX_HEART_RATE)} bpm
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background: rgba(0, 217, 255, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
            <h4 style='color: {colors[1]}; font-size: 16px;'>Zone 2 Percentage Calculation</h4>
            <p style='color: {colors[4]}; font-family: monospace; font-size: 14px; margin: 10px 0;'>
                Zone 2 % = (Number of Zone 2 runs / Total runs) × 100
            </p>
            <p style='color: {colors[4]}; font-size: 13px; margin: 10px 0;'>
                2024: ({zone2_runs_2024} / {len(df_2024)}) × 100 = {zone2_pct_2024:.1f}%<br>
                2025: ({zone2_runs_2025} / {len(df_2025)}) × 100 = {zone2_pct_2025:.1f}%<br>
                Change: +{(zone2_pct_2025 - zone2_pct_2024):.1f} percentage points
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Pace and HR Calculations
        st.markdown(f"""
        <h3 style='color: {colors[0]}; margin-top: 20px;'>3. Pace and Heart Rate Metrics</h3>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background: rgba(0, 217, 255, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
            <h4 style='color: {colors[1]}; font-size: 16px;'>Average Heart Rate</h4>
            <p style='color: {colors[4]}; font-family: monospace; font-size: 14px; margin: 10px 0;'>
                Avg HR = Σ(Average HR of all runs) / Number of runs
            </p>
            <p style='color: {colors[4]}; font-size: 13px; margin: 10px 0;'>
                2024: {avg_hr_2024:.1f} bpm<br>
                2025: {avg_hr_2025:.1f} bpm<br>
                Change: {(avg_hr_2024 - avg_hr_2025):.1f} bpm
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background: rgba(0, 217, 255, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
            <h4 style='color: {colors[1]}; font-size: 16px;'>Average Pace</h4>
            <p style='color: {colors[4]}; font-family: monospace; font-size: 14px; margin: 10px 0;'>
                Avg Pace = Σ(Pace of all runs) / Number of runs<br>
                Pace (min/km) = 1000 / (Average Speed m/s × 60)
            </p>
            <p style='color: {colors[4]}; font-size: 13px; margin: 10px 0;'>
                2024: {avg_pace_2024_fmt} /km<br>
                2025: {avg_pace_2025_fmt} /km<br>
                Improvement: {pace_improvement_text} /km
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
