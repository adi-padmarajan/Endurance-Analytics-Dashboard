import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


def render(colors, activities_df):
    st.title("Training Metrics Analysis")
    st.markdown("*Building the foundation through consistent volume and smart progression*")

    # Prepare data
    yearly_data = activities_df[activities_df['Activity Type'] == 'Run'].copy()
    yearly_data['Activity Date'] = pd.to_datetime(yearly_data['Activity Date'], format="%b %d, %Y, %I:%M:%S %p")
    yearly_data['Year'] = yearly_data['Activity Date'].dt.year
    yearly_data['Month'] = yearly_data['Activity Date'].dt.to_period('M')
    yearly_data['Week'] = yearly_data['Activity Date'].dt.to_period('W')

    # Calculate overall metrics
    total_distance = yearly_data['Distance'].sum()
    total_runs = len(yearly_data)
    avg_distance_per_run = yearly_data['Distance'].mean()
    total_time_hours = yearly_data['Elapsed Time'].sum() / 3600

    # Calculate consistency metrics
    weeks_with_runs = yearly_data['Week'].nunique()
    total_weeks = (yearly_data['Activity Date'].max() - yearly_data['Activity Date'].min()).days / 7
    consistency_pct = (weeks_with_runs / total_weeks * 100) if total_weeks > 0 else 0

    # Calculate yearly totals
    yearly_summary = yearly_data.groupby('Year').agg({
        'Distance': 'sum',
        'Activity ID': 'count'
    }).reset_index()
    yearly_summary.columns = ['Year', 'Total Distance (km)', 'Number of Runs']

    years = yearly_summary['Year'].astype(int).tolist()
    distances = yearly_summary['Total Distance (km)'].tolist()
    run_counts = yearly_summary['Number of Runs'].tolist()

    # Calculate year-over-year growth
    if len(distances) > 1:
        yoy_growth = ((distances[-1] - distances[0]) / distances[0] * 100)
        avg_annual_growth = yoy_growth / (len(distances) - 1)
    else:
        yoy_growth = 0
        avg_annual_growth = 0

    # KEY PERFORMANCE METRICS - Compact Cards
    st.markdown("### Training at a Glance")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #0a0420 0%, #1a0d2e 100%);
                    padding: 20px;
                    border-radius: 10px;
                    border: 2px solid {colors[0]};
                    text-align: center;'>
            <h4 style='color: {colors[0]}; margin: 0; font-size: 14px;'>Total Distance</h4>
            <h2 style='color: {colors[4]}; margin: 10px 0; font-size: 32px;'>{total_distance:,.0f} km</h2>
            <p style='color: {colors[1]}; margin: 0; font-size: 12px;'>{total_runs:,} runs</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #0a0420 0%, #1a0d2e 100%);
                    padding: 20px;
                    border-radius: 10px;
                    border: 2px solid {colors[1]};
                    text-align: center;'>
            <h4 style='color: {colors[1]}; margin: 0; font-size: 14px;'>Consistency</h4>
            <h2 style='color: {colors[4]}; margin: 10px 0; font-size: 32px;'>{consistency_pct:.1f}%</h2>
            <p style='color: {colors[0]}; margin: 0; font-size: 12px;'>{weeks_with_runs} active weeks</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #0a0420 0%, #1a0d2e 100%);
                    padding: 20px;
                    border-radius: 10px;
                    border: 2px solid #00ff9f;
                    text-align: center;'>
            <h4 style='color: #00ff9f; margin: 0; font-size: 14px;'>Avg Run</h4>
            <h2 style='color: {colors[4]}; margin: 10px 0; font-size: 32px;'>{avg_distance_per_run:.1f} km</h2>
            <p style='color: {colors[1]}; margin: 0; font-size: 12px;'>Per activity</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #0a0420 0%, #1a0d2e 100%);
                    padding: 20px;
                    border-radius: 10px;
                    border: 2px solid {colors[0]};
                    text-align: center;'>
            <h4 style='color: {colors[0]}; margin: 0; font-size: 14px;'>YoY Growth</h4>
            <h2 style='color: {colors[4]}; margin: 10px 0; font-size: 32px;'>+{avg_annual_growth:.1f}%</h2>
            <p style='color: {colors[1]}; margin: 0; font-size: 12px;'>Annual avg increase</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # VISUALIZATION 1: ANNUAL VOLUME WITH DUAL AXIS
    st.markdown("### Annual Training Volume Evolution")

    # Color gradient
    bar_colors = ['#8b3fff', '#b957ff', '#00a8ff', '#00d9ff']

    fig_annual = make_subplots(specs=[[{"secondary_y": True}]])

    # Add distance bars
    fig_annual.add_trace(
        go.Bar(
            x=years,
            y=distances,
            name='Distance (km)',
            marker=dict(color=bar_colors),
            text=[f"{dist:.0f} km" for dist in distances],
            textposition='inside',
            textfont=dict(size=11, color="#000000", weight='bold'),
            hovertemplate="<b>%{x}</b><br>Distance: %{y:.0f} km<extra></extra>"
        ),
        secondary_y=False
    )

    # Add run count line
    fig_annual.add_trace(
        go.Scatter(
            x=years,
            y=run_counts,
            name='Number of Runs',
            mode='lines+markers',
            marker=dict(size=12, color='#00ff9f', line=dict(color=colors[4], width=2)),
            line=dict(width=3, color='#00ff9f'),
            hovertemplate="<b>%{x}</b><br>Runs: %{y}<extra></extra>"
        ),
        secondary_y=True
    )

    fig_annual.update_xaxes(
        title_text="Year",
        title_font=dict(size=14, color=colors[0]),
        tickfont=dict(size=12, color=colors[4]),
        showgrid=False
    )

    fig_annual.update_yaxes(
        title_text="Distance (km)",
        title_font=dict(size=14, color=colors[0]),
        tickfont=dict(size=12, color=colors[4]),
        showgrid=True,
        gridcolor='rgba(0, 217, 255, 0.15)',
        secondary_y=False
    )

    fig_annual.update_yaxes(
        title_text="Number of Runs",
        title_font=dict(size=14, color='#00ff9f'),
        tickfont=dict(size=12, color=colors[4]),
        showgrid=False,
        secondary_y=True
    )

    fig_annual.update_layout(
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

    st.plotly_chart(fig_annual, use_container_width=True)

    # Insights for Annual Volume Evolution
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #0d1f26 0%, #1a0d2e 100%);
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid {colors[0]};
                margin: 20px 0;'>
        <h4 style='color: {colors[0]}; margin-top: 0; font-size: 15px;'>Analysis: Progressive Volume Growth Pattern</h4>
        <p style='color: {colors[4]}; line-height: 1.8; font-size: 14px; margin: 10px 0;'>
            The dual-axis chart shows a consistent upward trend in both total distance and number of runs across the years,
            with an average annual growth rate of <strong>{avg_annual_growth:.1f}%</strong>. The number of runs (green line) increases
            proportionally with total distance, indicating that volume growth comes from both increased running frequency and longer individual runs.
        </p>
        <p style='color: {colors[4]}; line-height: 1.8; font-size: 14px; margin: 10px 0;'>
            The progression shows no dramatic year-over-year spikes, suggesting a measured approach to volume accumulation.
            Each year builds upon the previous baseline with gradual increases in both metrics.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # VISUALIZATION 2: CUMULATIVE DISTANCE OVER TIME
    st.markdown("### Cumulative Training Progress")
    st.markdown("*Total distance accumulation over time*")

    # Calculate cumulative distance
    yearly_data_sorted = yearly_data.sort_values('Activity Date')
    yearly_data_sorted['Cumulative Distance'] = yearly_data_sorted['Distance'].cumsum()

    # Calculate weekly and monthly summaries (needed for later visualizations)
    weekly_summary = yearly_data.groupby('Week').agg({
        'Distance': 'sum',
        'Activity ID': 'count'
    }).reset_index()
    weekly_summary.columns = ['Week', 'Weekly Distance', 'Number of Runs']

    monthly_summary = yearly_data.groupby('Month').agg({
        'Distance': 'sum',
        'Activity ID': 'count'
    }).reset_index()
    monthly_summary.columns = ['Month', 'Total Distance (km)', 'Number of Runs']

    fig_cumulative = go.Figure()

    fig_cumulative.add_trace(go.Scatter(
        x=yearly_data_sorted['Activity Date'],
        y=yearly_data_sorted['Cumulative Distance'],
        mode='lines',
        fill='tozeroy',
        line=dict(width=3, color=colors[0]),
        fillcolor='rgba(0, 217, 255, 0.1)',
        hovertemplate="<b>%{x|%b %d, %Y}</b><br>Cumulative: %{y:.0f} km<extra></extra>"
    ))

    fig_cumulative.update_layout(
        height=500,
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(family='Arial', color=colors[4]),
        xaxis=dict(
            title="Date",
            tickfont=dict(size=12, color=colors[4]),
            showgrid=True,
            gridcolor='rgba(0, 217, 255, 0.15)',
            title_font=dict(size=14, color=colors[0])
        ),
        yaxis=dict(
            title="Cumulative Distance (km)",
            tickfont=dict(size=12, color=colors[4]),
            showgrid=True,
            gridcolor='rgba(0, 217, 255, 0.15)',
            title_font=dict(size=14, color=colors[0])
        ),
        margin=dict(l=70, r=30, t=30, b=60)
    )

    st.plotly_chart(fig_cumulative, use_container_width=True)

    # Insights for Cumulative Distance
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #0d1f26 0%, #1a0d2e 100%);
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid {colors[1]};
                margin: 20px 0;'>
        <h4 style='color: {colors[1]}; margin-top: 0; font-size: 15px;'>Analysis: Cumulative Distance Progression</h4>
        <p style='color: {colors[4]}; line-height: 1.8; font-size: 14px; margin: 10px 0;'>
            The cumulative distance curve shows {total_distance:,.0f} km accumulated over {total_runs:,} runs. The curve's steepness
            at different points indicates varying training intensity, with steeper sections corresponding to high-volume training blocks
            such as marathon preparation phases.
        </p>
        <p style='color: {colors[4]}; line-height: 1.8; font-size: 14px; margin: 10px 0;'>
            The consistent upward trajectory with minimal flat periods indicates regular training activity throughout the time period.
            Brief plateau regions visible in the chart correspond to recovery weeks or reduced training periods. The curve shows an
            increasing slope in more recent periods, reflecting higher training volume tolerance.
        </p>
    </div>
    """, unsafe_allow_html=True)


    # VISUALIZATION 5: RUN DISTANCE DISTRIBUTION
    st.markdown("### Run Distance Categories")
    st.markdown("*Distribution of training across different run types*")

    # Categorize runs
    def categorize_distance(dist):
        if dist < 5:
            return 'Recovery (< 5km)'
        elif dist < 10:
            return 'Short (5-10km)'
        elif dist < 15:
            return 'Medium (10-15km)'
        elif dist < 25:
            return 'Long (15-25km)'
        else:
            return 'Ultra Long (> 25km)'

    yearly_data['Distance_Category'] = yearly_data['Distance'].apply(categorize_distance)
    dist_category_counts = yearly_data['Distance_Category'].value_counts()

    # Define order
    category_order = ['Recovery (< 5km)', 'Short (5-10km)', 'Medium (10-15km)', 'Long (15-25km)', 'Ultra Long (> 25km)']
    dist_category_counts = dist_category_counts.reindex([c for c in category_order if c in dist_category_counts.index])

    col1, col2 = st.columns([1, 1])

    with col1:
        # Pie chart
        fig_dist_cat = go.Figure()

        fig_dist_cat.add_trace(go.Pie(
            labels=dist_category_counts.index.tolist(),
            values=dist_category_counts.values.tolist(),
            marker=dict(
                colors=[colors[1], colors[0], '#00ff9f', '#ffaa00', '#ff5555'],
                line=dict(color='#000000', width=2)
            ),
            textfont=dict(size=13, color='white'),
            hovertemplate="<b>%{label}</b><br>Runs: %{value}<br>Percentage: %{percent}<extra></extra>"
        ))

        fig_dist_cat.update_layout(
            height=500,
            paper_bgcolor="black",
            font=dict(family='Arial', color=colors[0]),
            legend=dict(font=dict(color=colors[4], size=11)),
            margin=dict(l=20, r=20, t=20, b=20)
        )

        st.plotly_chart(fig_dist_cat, use_container_width=True)

    with col2:
        # Bar chart alternative
        fig_dist_bar = go.Figure()

        fig_dist_bar.add_trace(go.Bar(
            y=dist_category_counts.index.tolist(),
            x=dist_category_counts.values.tolist(),
            orientation='h',
            marker=dict(
                color=[colors[1], colors[0], '#00ff9f', '#ffaa00', '#ff5555'],
                line=dict(color=colors[4], width=1)
            ),
            text=dist_category_counts.values.tolist(),
            textposition='outside',
            textfont=dict(size=12, color=colors[4]),
            hovertemplate="<b>%{y}</b><br>Runs: %{x}<extra></extra>"
        ))

        fig_dist_bar.update_layout(
            height=500,
            plot_bgcolor="black",
            paper_bgcolor="black",
            font=dict(family='Arial', color=colors[4]),
            xaxis=dict(
                title="Number of Runs",
                tickfont=dict(size=11, color=colors[4]),
                showgrid=True,
                gridcolor='rgba(0, 217, 255, 0.15)',
                title_font=dict(size=12, color=colors[0])
            ),
            yaxis=dict(
                tickfont=dict(size=11, color=colors[4]),
                showgrid=False
            ),
            margin=dict(l=150, r=20, t=20, b=60)
        )

        st.plotly_chart(fig_dist_bar, use_container_width=True)

    # Insights for Run Distance Distribution
    recovery_pct = (dist_category_counts.get('Recovery (< 5km)', 0) / total_runs * 100) if total_runs > 0 else 0
    long_runs = dist_category_counts.get('Long (15-25km)', 0) + dist_category_counts.get('Ultra Long (> 25km)', 0)
    long_run_pct = (long_runs / total_runs * 100) if total_runs > 0 else 0

    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #0d1f26 0%, #1a0d2e 100%);
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid #00ff9f;
                margin: 20px 0;'>
        <h4 style='color: #00ff9f; margin-top: 0; font-size: 15px;'>Analysis: Training Distribution by Distance Category</h4>
        <p style='color: {colors[4]}; line-height: 1.8; font-size: 14px; margin: 10px 0;'>
            The distribution shows a pyramid structure with recovery runs (< 5km) comprising {recovery_pct:.1f}% of total runs,
            while long runs (15-25km) and ultra-long runs (> 25km) together account for {long_run_pct:.1f}%. The majority of runs
            fall in the moderate distance ranges (5-15km), with progressively fewer runs at longer distances.
        </p>
        <p style='color: {colors[4]}; line-height: 1.8; font-size: 14px; margin: 10px 0;'>
            The pie chart shows percentage distribution by count, while the bar chart displays absolute numbers for easier comparison
            across categories. The medium distance category (10-15km) represents a balance between endurance development and
            recovery time, suitable for regular training frequency.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # RVM 2025 MARATHON PREP ANALYSIS
 
    st.markdown("---")
    st.markdown("## Royal Victoria Marathon 2025 - Sub 3:30 PR Prep Analysis")
    st.markdown("*16-Week Training Block: A Deep Dive into Race Preparation*")
    st.markdown("<br>", unsafe_allow_html=True)

    # Filter RVM 2025 prep data (16 weeks before race day: Oct 12, 2025)
    rvm_2025_end = pd.to_datetime('2025-10-12')  # Race day
    rvm_2025_start = rvm_2025_end - pd.Timedelta(weeks=16)  # 16 weeks back
    rvm_2025_data = yearly_data[(yearly_data['Activity Date'] >= rvm_2025_start) &
                                 (yearly_data['Activity Date'] <= rvm_2025_end)].copy()

    if len(rvm_2025_data) > 0:
        # Calculate RVM 2025 metrics
        rvm_2025_total_distance = rvm_2025_data['Distance'].sum()
        rvm_2025_total_runs = len(rvm_2025_data)
        rvm_2025_avg_distance = rvm_2025_data['Distance'].mean()
        rvm_2025_longest_run = rvm_2025_data['Distance'].max()
        rvm_2025_weeks = 16  # Exactly 16 weeks
        rvm_2025_avg_weekly = rvm_2025_total_distance / rvm_2025_weeks

        # Categorize workouts based on activity names and descriptions
        def categorize_workout(row):
            name = str(row['Activity Name']).lower()
            desc = str(row['Activity Description']).lower() if pd.notna(row['Activity Description']) else ''

            if 'zone 2' in name or 'z2' in desc:
                if 'long' in name:
                    return 'Long Run (Zone 2)'
                return 'Easy/Zone 2'
            elif 'tempo' in name or 'tempo' in desc:
                return 'Tempo'
            elif 'track' in name or 'repeats' in name or '800m' in desc or '400m' in desc or '200m' in desc:
                return 'Track/Intervals'
            elif 'marathon pace' in name or 'marathon pace' in desc:
                return 'Marathon Pace'
            elif 'speedwork' in name or 'hill' in name:
                return 'Speedwork/Hills'
            elif 'shakeout' in name:
                return 'Shakeout'
            elif row['Distance'] >= 18:
                return 'Long Run'
            else:
                return 'Easy Run'

        rvm_2025_data['Workout_Type'] = rvm_2025_data.apply(categorize_workout, axis=1)

        # RVM 2025 Summary Cards
        st.markdown("### Training Block Summary")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #0a0420 0%, #1a0d2e 100%);
                        padding: 20px;
                        border-radius: 10px;
                        border: 2px solid {colors[0]};
                        text-align: center;'>
                <h4 style='color: {colors[0]}; margin: 0; font-size: 14px;'>Total Distance</h4>
                <h2 style='color: {colors[4]}; margin: 10px 0; font-size: 32px;'>{rvm_2025_total_distance:.0f} km</h2>
                <p style='color: {colors[1]}; margin: 0; font-size: 12px;'>{rvm_2025_total_runs} runs</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #0a0420 0%, #1a0d2e 100%);
                        padding: 20px;
                        border-radius: 10px;
                        border: 2px solid {colors[1]};
                        text-align: center;'>
                <h4 style='color: {colors[1]}; margin: 0; font-size: 14px;'>Avg Weekly</h4>
                <h2 style='color: {colors[4]}; margin: 10px 0; font-size: 32px;'>{rvm_2025_avg_weekly:.0f} km</h2>
                <p style='color: {colors[0]}; margin: 0; font-size: 12px;'>Over {rvm_2025_weeks:.0f} weeks</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #0a0420 0%, #1a0d2e 100%);
                        padding: 20px;
                        border-radius: 10px;
                        border: 2px solid #00ff9f;
                        text-align: center;'>
                <h4 style='color: #00ff9f; margin: 0; font-size: 14px;'>Longest Run</h4>
                <h2 style='color: {colors[4]}; margin: 10px 0; font-size: 32px;'>{rvm_2025_longest_run:.1f} km</h2>
                <p style='color: {colors[1]}; margin: 0; font-size: 12px;'>Peak distance</p>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #0a0420 0%, #1a0d2e 100%);
                        padding: 20px;
                        border-radius: 10px;
                        border: 2px solid {colors[0]};
                        text-align: center;'>
                <h4 style='color: {colors[0]}; margin: 0; font-size: 14px;'>Avg Run</h4>
                <h2 style='color: {colors[4]}; margin: 10px 0; font-size: 32px;'>{rvm_2025_avg_distance:.1f} km</h2>
                <p style='color: {colors[1]}; margin: 0; font-size: 12px;'>Per activity</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # WORKOUT TYPE DISTRIBUTION
        st.markdown("### Workout Type Distribution")
        st.markdown("*How training was structured across different workout types*")

        workout_type_counts = rvm_2025_data['Workout_Type'].value_counts()
        workout_type_distance = rvm_2025_data.groupby('Workout_Type')['Distance'].sum()

        col1, col2 = st.columns([1, 1])

        with col1:
            # Pie chart by count
            fig_workout_pie = go.Figure()
            fig_workout_pie.add_trace(go.Pie(
                labels=workout_type_counts.index.tolist(),
                values=workout_type_counts.values.tolist(),
                marker=dict(
                    colors=[colors[1], colors[0], '#00ff9f', '#ffaa00', '#ff5555', '#00d9ff', '#b957ff', '#8b3fff'],
                    line=dict(color='#000000', width=2)
                ),
                textfont=dict(size=12, color='white'),
                hovertemplate="<b>%{label}</b><br>Runs: %{value}<br>Percentage: %{percent}<extra></extra>"
            ))

            fig_workout_pie.update_layout(
                title=dict(text="By Number of Runs", font=dict(size=14, color=colors[0])),
                height=400,
                paper_bgcolor="black",
                font=dict(family='Arial', color=colors[0]),
                legend=dict(font=dict(color=colors[4], size=10)),
                margin=dict(l=20, r=20, t=50, b=20)
            )

            st.plotly_chart(fig_workout_pie, use_container_width=True)

        with col2:
            # Pie chart by distance
            fig_workout_dist_pie = go.Figure()
            fig_workout_dist_pie.add_trace(go.Pie(
                labels=workout_type_distance.index.tolist(),
                values=workout_type_distance.values.tolist(),
                marker=dict(
                    colors=[colors[1], colors[0], '#00ff9f', '#ffaa00', '#ff5555', '#00d9ff', '#b957ff', '#8b3fff'],
                    line=dict(color='#000000', width=2)
                ),
                textfont=dict(size=12, color='white'),
                hovertemplate="<b>%{label}</b><br>Distance: %{value:.1f} km<br>Percentage: %{percent}<extra></extra>"
            ))

            fig_workout_dist_pie.update_layout(
                title=dict(text="By Total Distance", font=dict(size=14, color=colors[0])),
                height=400,
                paper_bgcolor="black",
                font=dict(family='Arial', color=colors[0]),
                legend=dict(font=dict(color=colors[4], size=10)),
                margin=dict(l=20, r=20, t=50, b=20)
            )

            st.plotly_chart(fig_workout_dist_pie, use_container_width=True)

        # Insights for Workout Type Distribution
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #0d1f26 0%, #1a0d2e 100%);
                    padding: 20px;
                    border-radius: 10px;
                    border-left: 4px solid {colors[1]};
                    margin: 20px 0;'>
            <h4 style='color: {colors[1]}; margin-top: 0; font-size: 15px;'>Analysis: Workout Type Distribution</h4>
            <p style='color: {colors[4]}; line-height: 1.8; font-size: 14px; margin: 10px 0;'>
                The left chart shows workout frequency by type, while the right chart shows total distance contribution. Long runs
                appear less frequently but contribute disproportionately to total distance, which is typical for marathon-specific training.
            </p>
            <p style='color: {colors[4]}; line-height: 1.8; font-size: 14px; margin: 10px 0;'>
                Zone 2 runs comprise the largest portion of workouts, with additional sessions including tempo runs, track intervals,
                and marathon pace work. This distribution reflects a polarized training approach where most volume occurs at low intensity,
                supplemented by targeted high-intensity sessions. Each workout type serves a distinct physiological purpose: long runs
                for endurance, tempo runs for lactate threshold, track sessions for speed development, and Zone 2 work for aerobic base.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # WEEKLY PROGRESSION FOR RVM 2025
        st.markdown("### Weekly Training Progression")
        st.markdown("*Volume and consistency throughout the prep cycle*")

        rvm_2025_data['Week_Start'] = rvm_2025_data['Activity Date'].dt.to_period('W').apply(lambda r: r.start_time)
        weekly_rvm = rvm_2025_data.groupby('Week_Start').agg({
            'Distance': 'sum',
            'Activity ID': 'count'
        }).reset_index()
        weekly_rvm.columns = ['Week', 'Distance', 'Runs']

        fig_weekly = make_subplots(specs=[[{"secondary_y": True}]])

        # Distance bars
        fig_weekly.add_trace(
            go.Bar(
                x=weekly_rvm['Week'],
                y=weekly_rvm['Distance'],
                name='Weekly Distance',
                marker=dict(
                    color=weekly_rvm['Distance'],
                    colorscale=[[0, colors[1]], [0.5, colors[0]], [1, '#00ff9f']],
                    line=dict(color=colors[4], width=1)
                ),
                text=[f"{dist:.0f}" for dist in weekly_rvm['Distance']],
                textposition='inside',
                textfont=dict(size=10, color='#000000', weight='bold'),
                hovertemplate="<b>Week of %{x|%b %d}</b><br>Distance: %{y:.0f} km<extra></extra>"
            ),
            secondary_y=False
        )

        # Runs line
        fig_weekly.add_trace(
            go.Scatter(
                x=weekly_rvm['Week'],
                y=weekly_rvm['Runs'],
                name='Number of Runs',
                mode='lines+markers',
                marker=dict(size=10, color='#00ff9f', line=dict(color=colors[4], width=2)),
                line=dict(width=3, color='#00ff9f'),
                hovertemplate="<b>Week of %{x|%b %d}</b><br>Runs: %{y}<extra></extra>"
            ),
            secondary_y=True
        )

        fig_weekly.update_xaxes(
            title_text="Week",
            title_font=dict(size=14, color=colors[0]),
            tickfont=dict(size=11, color=colors[4]),
            showgrid=False
        )

        fig_weekly.update_yaxes(
            title_text="Distance (km)",
            title_font=dict(size=14, color=colors[0]),
            tickfont=dict(size=12, color=colors[4]),
            showgrid=True,
            gridcolor='rgba(0, 217, 255, 0.15)',
            secondary_y=False
        )

        fig_weekly.update_yaxes(
            title_text="Number of Runs",
            title_font=dict(size=14, color='#00ff9f'),
            tickfont=dict(size=12, color=colors[4]),
            showgrid=False,
            secondary_y=True
        )

        fig_weekly.update_layout(
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

        st.plotly_chart(fig_weekly, use_container_width=True)

        # Insights for Weekly Progression
        peak_week_distance = weekly_rvm['Distance'].max()
        taper_week_distance = weekly_rvm['Distance'].iloc[-2] if len(weekly_rvm) > 1 else 0
        avg_weekly_rvm = weekly_rvm['Distance'].mean()

        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #0d1f26 0%, #1a0d2e 100%);
                    padding: 20px;
                    border-radius: 10px;
                    border-left: 4px solid #00ff9f;
                    margin: 20px 0;'>
            <h4 style='color: #00ff9f; margin-top: 0; font-size: 15px;'>Analysis: Weekly Training Progression</h4>
            <p style='color: {colors[4]}; line-height: 1.8; font-size: 14px; margin: 10px 0;'>
                The chart shows a classic marathon training pattern: gradual build, peak, and taper. Peak week reached {peak_week_distance:.0f} km,
                representing the highest volume week in the training cycle. The average weekly distance across the preparation period
                was {avg_weekly_rvm:.0f} km.
            </p>
            <p style='color: {colors[4]}; line-height: 1.8; font-size: 14px; margin: 10px 0;'>
                The green line shows number of runs per week, typically maintaining 4-6 runs regardless of total volume. This indicates
                volume distribution across multiple sessions rather than concentrated in fewer, longer runs. In the final 2-3 weeks before
                the race, volume decreases to {taper_week_distance:.0f} km while run frequency remains relatively stable, consistent with
                standard taper protocols that reduce volume while maintaining workout frequency.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Display message when no RVM 2025 data exists
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #0d1f26 0%, #1a0d2e 100%);
                    padding: 30px;
                    border-radius: 10px;
                    border-left: 4px solid {colors[1]};
                    margin: 20px 0;
                    text-align: center;'>
            <h4 style='color: {colors[1]}; margin-top: 0; font-size: 16px;'>No Training Data Available</h4>
            <p style='color: {colors[4]}; line-height: 1.8; font-size: 14px; margin: 10px 0;'>
                No running data found for the RVM 2025 prep period ({rvm_2025_start.strftime('%b %d, %Y')} - {rvm_2025_end.strftime('%b %d, %Y')}).
                This section will populate once training activities are logged for this time period.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # FORMULAS AND CALCULATIONS SECTION
    st.markdown("---")
    st.markdown("## Formulas & Calculations Reference")
    st.markdown("*Mathematical formulas used in Training Metrics Analysis*")

    with st.expander("**View All Formulas Used in Calculations**", expanded=False):

        # Core Training Metrics
        st.markdown(f"""
        <h3 style='color: {colors[0]}; margin-top: 0;'>1. Core Training Metrics</h3>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background: rgba(0, 217, 255, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
            <h4 style='color: {colors[1]}; font-size: 16px;'>Total Distance</h4>
            <p style='color: {colors[4]}; font-family: monospace; font-size: 14px; margin: 10px 0;'>
                Total Distance = Σ(Distance of all runs)<br>
                = Sum of all individual run distances
            </p>
            <p style='color: {colors[4]}; font-size: 13px; margin: 10px 0;'>
                Current Total: {total_distance:,.0f} km across {total_runs:,} runs
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background: rgba(0, 217, 255, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
            <h4 style='color: {colors[1]}; font-size: 16px;'>Average Distance Per Run</h4>
            <p style='color: {colors[4]}; font-family: monospace; font-size: 14px; margin: 10px 0;'>
                Average Distance = Total Distance / Total Number of Runs<br>
                = {total_distance:,.0f} / {total_runs:,}<br>
                = {avg_distance_per_run:.2f} km per run
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background: rgba(0, 217, 255, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
            <h4 style='color: {colors[1]}; font-size: 16px;'>Total Training Time</h4>
            <p style='color: {colors[4]}; font-family: monospace; font-size: 14px; margin: 10px 0;'>
                Total Time (hours) = Σ(Elapsed Time in seconds) / 3600<br>
                = {yearly_data['Elapsed Time'].sum():.0f} seconds / 3600<br>
                = {total_time_hours:.2f} hours
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Consistency Metrics
        st.markdown(f"""
        <h3 style='color: {colors[0]}; margin-top: 20px;'>2. Consistency Metrics</h3>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background: rgba(0, 217, 255, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
            <h4 style='color: {colors[1]}; font-size: 16px;'>Weekly Consistency Percentage</h4>
            <p style='color: {colors[4]}; font-family: monospace; font-size: 14px; margin: 10px 0;'>
                Total Weeks = (Latest Activity Date - Earliest Activity Date) / 7<br>
                Weeks with Runs = Number of unique weeks containing at least one run<br>
                Consistency % = (Weeks with Runs / Total Weeks) × 100
            </p>
            <p style='color: {colors[4]}; font-size: 13px; margin: 10px 0;'>
                Current Consistency: {consistency_pct:.1f}%<br>
                ({weeks_with_runs} active weeks out of {total_weeks:.0f} total weeks)
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Growth Metrics
        st.markdown(f"""
        <h3 style='color: {colors[0]}; margin-top: 20px;'>3. Year-over-Year Growth</h3>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background: rgba(0, 217, 255, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
            <h4 style='color: {colors[1]}; font-size: 16px;'>Total Growth Percentage</h4>
            <p style='color: {colors[4]}; font-family: monospace; font-size: 14px; margin: 10px 0;'>
                YoY Growth % = ((Latest Year Distance - First Year Distance) / First Year Distance) × 100
            </p>
            <p style='color: {colors[4]}; font-size: 13px; margin: 10px 0;'>
                Example calculation:<br>
                <span style='font-family: monospace;'>
                = ((Latest Year km - First Year km) / First Year km) × 100
                </span>
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background: rgba(0, 217, 255, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
            <h4 style='color: {colors[1]}; font-size: 16px;'>Average Annual Growth Rate</h4>
            <p style='color: {colors[4]}; font-family: monospace; font-size: 14px; margin: 10px 0;'>
                Avg Annual Growth = Total YoY Growth % / Number of Years<br>
                = {yoy_growth:.2f}% / {len(distances) - 1 if len(distances) > 1 else 1}<br>
                = {avg_annual_growth:.2f}% per year
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Cumulative Metrics
        st.markdown(f"""
        <h3 style='color: {colors[0]}; margin-top: 20px;'>4. Cumulative Distance Calculation</h3>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background: rgba(0, 217, 255, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
            <h4 style='color: {colors[1]}; font-size: 16px;'>Running Cumulative Sum</h4>
            <p style='color: {colors[4]}; font-family: monospace; font-size: 14px; margin: 10px 0;'>
                Cumulative Distance[i] = Σ(Distance[0] to Distance[i])<br>
                For each activity, sum all previous distances
            </p>
            <p style='color: {colors[4]}; font-size: 13px; margin: 10px 0;'>
                This creates the ascending line in the cumulative distance chart
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Distance Categorization
        st.markdown(f"""
        <h3 style='color: {colors[0]}; margin-top: 20px;'>5. Run Distance Categorization</h3>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background: rgba(0, 217, 255, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
            <h4 style='color: {colors[1]}; font-size: 16px;'>Distance Categories</h4>
            <p style='color: {colors[4]}; font-family: monospace; font-size: 14px; margin: 10px 0;'>
                Runs are categorized based on distance:
            </p>
            <p style='color: {colors[4]}; font-size: 13px; margin: 10px 0;'>
                • Recovery: Distance < 5 km<br>
                • Short: 5 km ≤ Distance < 10 km<br>
                • Medium: 10 km ≤ Distance < 15 km<br>
                • Long: 15 km ≤ Distance < 25 km<br>
                • Ultra Long: Distance ≥ 25 km
            </p>
        </div>
        """, unsafe_allow_html=True)

        # RVM 2025 Prep Specific Metrics
        if len(rvm_2025_data) > 0:
            st.markdown(f"""
            <h3 style='color: {colors[0]}; margin-top: 20px;'>6. RVM 2025 Marathon Prep Metrics</h3>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div style='background: rgba(0, 217, 255, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
                <h4 style='color: {colors[1]}; font-size: 16px;'>Average Weekly Distance</h4>
                <p style='color: {colors[4]}; font-family: monospace; font-size: 14px; margin: 10px 0;'>
                    Prep Duration = 16 weeks (calculated as 16 weeks before race day)<br>
                    Start Date = Oct 12, 2025 - 16 weeks = {rvm_2025_start.strftime('%b %d, %Y')}<br>
                    End Date = {rvm_2025_end.strftime('%b %d, %Y')} (Race Day)
                </p>
                <p style='color: {colors[4]}; font-family: monospace; font-size: 14px; margin: 10px 0;'>
                    Avg Weekly = Total Distance / Duration in Weeks<br>
                    = {rvm_2025_total_distance:.0f} km / {rvm_2025_weeks}<br>
                    = {rvm_2025_avg_weekly:.2f} km/week
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div style='background: rgba(0, 217, 255, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
                <h4 style='color: {colors[1]}; font-size: 16px;'>Workout Type Categorization</h4>
                <p style='color: {colors[4]}; font-family: monospace; font-size: 14px; margin: 10px 0;'>
                    Classification based on activity names and descriptions:
                </p>
                <p style='color: {colors[4]}; font-size: 13px; margin: 10px 0;'>
                    • Zone 2 / Easy: Activities with "zone 2" or "z2" in name/description<br>
                    • Long Run: Zone 2 runs with "long" in name OR distance ≥ 18 km<br>
                    • Tempo: Activities with "tempo" keyword<br>
                    • Track/Intervals: Activities with "track", "repeats", "800m", "400m", "200m"<br>
                    • Marathon Pace: Activities with "marathon pace" keyword<br>
                    • Speedwork/Hills: Activities with "speedwork" or "hill" keyword<br>
                    • Shakeout: Activities with "shakeout" keyword<br>
                    • Easy Run: All other runs
                </p>
            </div>
            """, unsafe_allow_html=True)

        # Aggregation Formulas
        st.markdown(f"""
        <h3 style='color: {colors[0]}; margin-top: 20px;'>7. Data Aggregation Methods</h3>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background: rgba(0, 217, 255, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
            <h4 style='color: {colors[1]}; font-size: 16px;'>Yearly Aggregation</h4>
            <p style='color: {colors[4]}; font-family: monospace; font-size: 14px; margin: 10px 0;'>
                For each year:<br>
                • Total Distance = Σ(Distance) grouped by Year<br>
                • Number of Runs = count(Activity ID) grouped by Year
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background: rgba(0, 217, 255, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
            <h4 style='color: {colors[1]}; font-size: 16px;'>Monthly Aggregation</h4>
            <p style='color: {colors[4]}; font-family: monospace; font-size: 14px; margin: 10px 0;'>
                For each month:<br>
                • Total Distance = Σ(Distance) grouped by Year-Month<br>
                • Number of Runs = count(Activity ID) grouped by Year-Month
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='background: rgba(0, 217, 255, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
            <h4 style='color: {colors[1]}; font-size: 16px;'>Weekly Aggregation</h4>
            <p style='color: {colors[4]}; font-family: monospace; font-size: 14px; margin: 10px 0;'>
                For each week (ISO week format):<br>
                • Weekly Distance = Σ(Distance) grouped by ISO Week<br>
                • Number of Runs = count(Activity ID) grouped by ISO Week
            </p>
            <p style='color: {colors[4]}; font-size: 13px; margin: 10px 0;'>
                ISO week starts on Monday and ends on Sunday
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
