import streamlit as st
import plotly.graph_objects as go


def render(colors, vo2max_df):
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

    # VO₂ Max Progression (2025 Data)
    st.markdown("#### VO₂ Max Progression")
    st.markdown("*Aerobic capacity improvements throughout 2025*")

    # Prepare VO₂ Max data
    months = vo2max_df['Month'].tolist()
    vo2_values = vo2max_df['VO2 Max'].tolist()

    # Create Plotly figure for VO₂ Max
    fig_vo2 = go.Figure()

    # Add line trace with markers
    fig_vo2.add_trace(go.Scatter(
        x=months,
        y=vo2_values,
        mode='lines+markers',
        marker=dict(
            size=12,
            color='#00ff9f',  # Cyan-green color
            line=dict(color=colors[0], width=2)
        ),
        line=dict(width=3, color='#00ff9f', shape='spline'),
        fill='tozeroy',
        fillcolor='rgba(0, 255, 159, 0.1)',
        hovertemplate="<b>%{x}</b><br>VO₂ Max: %{y:.1f} ml/kg/min<extra></extra>"
    ))

    # Update layout
    fig_vo2.update_layout(
        xaxis=dict(
            title=dict(text="Month", font=dict(size=14, color=colors[0], family='Arial')),
            tickfont=dict(size=12, color=colors[4]),
            showgrid=True,
            gridcolor=f'rgba(0, 217, 255, 0.15)',
            showline=True,
            linecolor=colors[1],
            linewidth=1
        ),
        yaxis=dict(
            title=dict(text="VO₂ Max (ml/kg/min)", font=dict(size=14, color=colors[0], family='Arial')),
            tickfont=dict(size=12, color=colors[4]),
            showgrid=True,
            gridcolor=f'rgba(0, 217, 255, 0.15)',
            showline=True,
            linecolor=colors[1],
            linewidth=1,
            range=[50, 66]
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

    st.plotly_chart(fig_vo2, use_container_width=True)
