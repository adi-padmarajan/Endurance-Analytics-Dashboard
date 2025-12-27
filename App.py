import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Page configuration for a wide layout
st.set_page_config(
    page_title="The Sub-3:30 Protocol",  # Browser tab title
    page_icon="⭐",                       # Browser tab icon
    layout="wide"                         # Use full width of the page
)

st.title("The Sub-3:30 Protocol: A 6-Race Journey from Sub-5")
st.subheader("A Data-Driven Analysis of Marathon Progression (2022 – 2025)")

st.markdown("<hr>", unsafe_allow_html=True)

# Load datasets
activities_df = pd.read_csv("activities_dataset.csv")
challenges_df = pd.read_csv("global_challenges.csv")

with st.expander("### Project Overview", expanded = False):
	st.markdown(
	"""
	This dashboard analyzes **347 running activities over 3.5 years**, documenting the progression from a first-time marathoner (4:46:07 at Royal Victoria Marathon 2022) to a sub-3:30 finisher (3:26:00 at Royal Victoria Marathon 2025) — an improvement of **80 minutes** across 6 marathon races.
	The analysis explores how training patterns, physiological adaptations, and race execution evolved to produce consistent performance gains at two recurring races: the **Royal Victoria Marathon** (4 finishes) and **BMO Vancouver Marathon** (2 finishes).
	"""
	)

with st.expander("### Datasets", expanded = False):
	st.markdown(
	"""
	The dataset is sourced from a complete Strava activity export containing 449 total activities. For this analysis, we filter exclusively to **running activities (347 runs)** spanning February 2022 to October 2025.

	**Key columns extracted:**
	- **Activity metadata:** ID, Date, Name, Type
	- **Performance metrics:** Distance, Speed, Pace, Moving Time
	- **Physiological data:** Heart Rate (average/max)
	- **Terrain data:** Elevation Gain/Loss, High/Low points
	- **Effort indicators:** Calories, Relative Effort

	*Note: Heart rate data is unavailable for the first 20 runs (Feb–Jun 2022) due to the absence of a heart rate monitor during that period.*
	""")

with st.expander("### Marathons Race Summary and Official Times", expanded = False):
	st.markdown(
	"""
	| Race | Date | Finish Time | Pace |
	|------|------|-------------|------|
	| Royal Victoria Marathon 2022 | Oct 9, 2022 | 4:46:07 | 6:30/km |
	| BMO Vancouver Marathon 2023 | May 7, 2023 | 4:25:48 | 6:13/km |
	| Royal Victoria Marathon 2023 | Oct 8, 2023 | 4:16:58 | 6:04/km |
	| Royal Victoria Marathon 2024 | Oct 13, 2024 | 3:47:47 | 5:22/km |
	| BMO Vancouver Marathon 2025 | May 4, 2025 | 3:37:23 | 5:07/km |
	| Royal Victoria Marathon 2025 | Oct 12, 2025 | 3:26:00 | 4:50/km |

	"""
)

with st.expander("### Link to Github Repository and Jupyter Notebook", expanded = False):
	st.markdown(
	"""
	- **GitHub Repository:** https://github.com/adi-padmarajan/Endurance-Analytics-Dashboard
	- **Jupyter Notebook:** https://github.com/adi-padmarajan/Endurance-Analytics-Dashboard/blob/main/endurance_analytics.ipynb
	"""
	)

st.markdown("<hr>", unsafe_allow_html=True)

# Define the data for the chart
races = ["RVM 2022", "BMO 2023", "RVM 2023", "RVM 2024", "BMO 2025", "RVM 2025"]
times_minutes = [286.12, 265.80, 256.97, 227.78, 217.38, 206.00]  # Finish times in minutes
times_labels = ["4:46:07", "4:25:48", "4:16:58", "3:47:47", "3:37:23", "3:26:00"]  # H:M:S format labels

st.markdown("## Marathon Performance Metrics")

col1, col2, col3 = st.columns(3)

# Marathon Progression Timeline

with col1:
    st.markdown("#### Marathon Progression Timeline")
    st.markdown("*Finish time improvements across all 6 marathon races*")

    # Define the data for the chart
    races = ["RVM 2022", "BMO 2023", "RVM 2023", "RVM 2024", "BMO 2025", "RVM 2025"]
    times_minutes = [286.12, 265.80, 256.97, 227.78, 217.38, 206.00]
    times_labels = ["4:46:07", "4:25:48", "4:16:58", "3:47:47", "3:37:23", "3:26:00"]

    # Create Plotly figure
    fig1 = go.Figure()

    # Add line trace with markers (Blue color)
    fig1.add_trace(go.Scatter(
        x=races,
        y=times_minutes,
        mode='lines+markers',
        marker=dict(size=10, color='#3B82F6'),  
        line=dict(width=2.5, color='#3B82F6'),
        hovertemplate="<b>%{x}</b><br>Time: %{customdata}<extra></extra>",
        customdata=times_labels
    ))

    # Update layout with inverted y-axis and H:M:S tick labels
    fig1.update_layout(
        xaxis=dict(
            title=dict(text="Race", font=dict(size=14, color='#334155', family='Arial')),
            tickfont=dict(size=12, color='#475569'),
            showgrid=True,
            gridcolor='rgba(148, 163, 184, 0.15)',
            showline=True,
            linecolor='rgba(148, 163, 184, 0.3)',
            linewidth=1
        ),
        yaxis=dict(
            title=dict(text="Finish Time (H:M:S)", font=dict(size=14, color='#334155', family='Arial')),
            tickvals=times_minutes,
            ticktext=times_labels,
            autorange="reversed",
            tickfont=dict(size=12, color='#475569'),
            showgrid=True,
            gridcolor='rgba(148, 163, 184, 0.15)',
            showline=True,
            linecolor='rgba(148, 163, 184, 0.3)',
            linewidth=1
        ),
        height=400,
        margin=dict(l=70, r=30, t=30, b=60),
        hovermode='x unified',
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(family='Arial', color='#334155'),
        hoverlabel=dict(
            bgcolor='white',
            font_size=13,
            font_family='Arial',
            bordercolor='#3B82F6',
			font_color = 'black'
        )
    )

    st.plotly_chart(fig1, use_container_width=True)

# Pace Evolution Curve (NEW - Green color, right column)

with col2:
    st.markdown("#### Pace Evolution Curve")
    st.markdown("*Average pace progression from 6:30/km to 4:50/km*")

    # Define pace data for the chart
    races = ["RVM 2022", "BMO 2023", "RVM 2023", "RVM 2024", "BMO 2025", "RVM 2025"]
    pace_decimal = [6.50, 6.22, 6.07, 5.37, 5.12, 4.83]  # Pace in decimal minutes (e.g., 6:30 = 6.5)
    pace_labels = ["6:30", "6:13", "6:04", "5:22", "5:07", "4:50"]  # M:SS format labels

    # Create Plotly figure for pace chart
    fig2 = go.Figure()

    # Add line trace with markers (Green color)
    fig2.add_trace(go.Scatter(
        x=races,
        y=pace_decimal,
        mode='lines+markers',
        marker=dict(size=10, color='#10B981'),  # Green markers
        line=dict(width=2.5, color='#10B981'),  # Green line
        hovertemplate="<span style = \"color: black\"><b>%{x}</b><br>Pace: %{customdata}/km</span> <extra></extra>",
        customdata=pace_labels
    ))

    # Update layout with inverted y-axis and pace labels
    fig2.update_layout(
        xaxis=dict(
            title=dict(text="Race", font=dict(size=14, color='#334155', family='Arial')),
            tickfont=dict(size=12, color='#475569'),
            showgrid=True,
            gridcolor='rgba(148, 163, 184, 0.15)',
            showline=True,
            linecolor='rgba(148, 163, 184, 0.3)',
            linewidth=1
        ),
        yaxis=dict(
            title=dict(text="Pace (min/km)", font=dict(size=14, color='#334155', family='Arial')),
            tickvals=pace_decimal,      # Tick positions
            ticktext=pace_labels,       # Display M:SS labels
            autorange="reversed",       # INVERTED: Faster pace (lower number) at top
            tickfont=dict(size=12, color='#475569'),
            showgrid=True,
            gridcolor='rgba(148, 163, 184, 0.15)',
            showline=True,
            linecolor='rgba(148, 163, 184, 0.3)',
            linewidth=1
        ),
        height=400,
        margin=dict(l=70, r=30, t=30, b=60),
        hovermode='x unified',
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(family='Arial', color='#334155'),
        hoverlabel=dict(
            bgcolor='white',
            font_size=13,
            font_family='Arial',
            bordercolor='#10B981',
			font_color = 'black'
        )
    )

    # Display the pace chart
    st.plotly_chart(fig2, use_container_width=True)

with col3:
    # Building the Base
    st.markdown("#### Building the Base")
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

    # Color Gradient (Purple)
    colors = ['#d896ff', '#be29ec', '#800080', '#660066']

    # Create Plotly figure
    fig3 = go.Figure()

    # Add bar trace
    fig3.add_trace(go.Bar(
        x=years,
        y=distances,
        marker=dict(
            color=colors,
            line=dict(color = "white", width=0.5)
        ),
        text=[f"{dist:.0f} km" for dist, runs in zip(distances, run_counts)],
        textposition='inside',
        insidetextanchor="middle", # Vertical Centering
        textfont=dict(size=11, color='white', family='Arial'),
        hovertemplate="<span style = \"color: black\"><b>%{x}</b><br>Distance: %{y:.0f} km</span> <br> <span style = \"color: black\"> Runs: %{customdata}</span> <extra></extra>",
        customdata=run_counts
    ))

    # Update layout
    fig3.update_layout(
        xaxis=dict(
            title=dict(text="Year", font=dict(size=14, color='#334155', family='Arial')),
            tickfont=dict(size=12, color='#475569'),
            showgrid=False,
            showline=True,
            linecolor='rgba(148, 163, 184, 0.3)',
            linewidth=1
        ),
        yaxis=dict(
            title=dict(text="Total Distance (km)", font=dict(size=14, color='#334155', family='Arial')),
            tickfont=dict(size=12, color='#475569'),
            showgrid=True,
            gridcolor='rgba(148, 163, 184, 0.15)',
            showline=True,
            linecolor='rgba(148, 163, 184, 0.3)',
            linewidth=1
        ),
        height=400,
        margin=dict(l=70, r=30, t=30, b=60),
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(family='Arial', color='#334155'),
        hoverlabel=dict(
            bgcolor='white',
            font_size=13,
            font_family='Arial',
            bordercolor='#2E7D32'
        ),
        showlegend=False
    )

    st.plotly_chart(fig3, use_container_width=True)



# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align: center; color: #64748b; font-size: 0.85rem;'>
        Built by <strong>Aditya Padmarajan</strong> • Data from Strava • 2022-2025
    </div>
    """, 
    unsafe_allow_html=True
)
