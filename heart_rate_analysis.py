import streamlit as st
import plotly.graph_objects as go


def render(colors, df_hr):
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
