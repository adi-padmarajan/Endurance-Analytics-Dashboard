import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def render(colors, activities_df):
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
