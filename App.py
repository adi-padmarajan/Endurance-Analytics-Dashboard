import streamlit as st
import pandas as pd

# Import page modules
import home
import marathon_performance
import training_metrics
import heart_rate_analysis
import route_visualization

# Page configuration for a wide layout
st.set_page_config(
    page_title="The Sub-3:30 Protocol",  # Browser tab title
    page_icon="⭐",                       # Browser tab icon
    layout="wide"                         # Use full width of the page
)

colors = ["#00d9ff", "#b957ff", "#1a0d2e", "#0a0420", "#e0f4ff"]

# Load external CSS file and add enhancements
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css("styles.css")

# Additional CSS enhancements for 10/10 polish
st.markdown("""
<style>
    /* Smooth scrolling */
    html {
        scroll-behavior: smooth;
    }

    /* Enhanced card animations on hover */
    [data-testid="stMetric"] {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0, 217, 255, 0.2);
    }

    /* Improve expander styling */
    .streamlit-expanderHeader {
        font-weight: 600;
        font-size: 16px;
        border-radius: 8px;
        transition: background-color 0.3s ease;
    }

    .streamlit-expanderHeader:hover {
        background-color: rgba(0, 217, 255, 0.05);
    }

    /* Smooth transition for plotly charts */
    .js-plotly-plot {
        transition: opacity 0.3s ease-in;
    }

    /* Better link styling */
    a {
        color: #00d9ff;
        text-decoration: none;
        transition: color 0.3s ease;
    }

    a:hover {
        color: #00ff9f;
        text-decoration: underline;
    }

    /* Table styling improvements */
    table.training-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }

    table.training-table th {
        background: linear-gradient(135deg, #00d9ff 0%, #00ff9f 100%);
        color: #0a0420;
        font-weight: 700;
        padding: 15px;
        text-align: left;
        font-size: 14px;
        letter-spacing: 0.5px;
    }

    table.training-table td {
        background: #0a0420;
        color: #e0e0e0;
        padding: 12px 15px;
        border-bottom: 1px solid rgba(0, 217, 255, 0.1);
        font-size: 13px;
    }

    table.training-table tr:last-child td {
        border-bottom: none;
    }

    table.training-table tr:hover td {
        background: rgba(0, 217, 255, 0.05);
        transition: background 0.3s ease;
    }

    /* Enhanced scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: #0a0420;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #00d9ff 0%, #00ff9f 100%);
        border-radius: 5px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #00ff9f 0%, #00d9ff 100%);
    }

    /* Loading animation */
    .stSpinner > div {
        border-top-color: #00d9ff !important;
    }

    /* Improve markdown heading spacing */
    h1, h2, h3, h4 {
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }

    /* Add subtle fade-in animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .element-container {
        animation: fadeIn 0.5s ease-out;
    }

    /* Enhance sidebar navigation */
    .stRadio > div {
        gap: 0.5rem;
    }

    .stRadio > div > label {
        background: linear-gradient(135deg, rgba(0, 217, 255, 0.05) 0%, rgba(185, 87, 255, 0.05) 100%);
        padding: 12px 16px;
        border-radius: 8px;
        border-left: 3px solid transparent;
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .stRadio > div > label:hover {
        background: linear-gradient(135deg, rgba(0, 217, 255, 0.15) 0%, rgba(185, 87, 255, 0.15) 100%);
        border-left-color: #00d9ff;
        transform: translateX(5px);
    }

    .stRadio > div > label[data-baseweb="radio"] > div:first-child {
        background-color: #00d9ff;
    }

    /* Improve hr styling */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #00d9ff 50%, transparent 100%);
        margin: 2rem 0;
    }

    /* Add glow effect to key metrics */
    [data-testid="stMetricValue"] {
        text-shadow: 0 0 20px rgba(0, 217, 255, 0.3);
    }

    /* Enhance footer */
    footer {
        visibility: hidden;
    }

    /* Better focus states for accessibility */
    button:focus, a:focus {
        outline: 2px solid #00d9ff;
        outline-offset: 2px;
    }
</style>
""", unsafe_allow_html=True)


# Sidebar Navigation
with st.sidebar:
    st.title("The Sub-3:30 Protocol")
    st.markdown("<hr>", unsafe_allow_html=True)

    # Navigation Menu
    page = st.radio(
        "Navigation",
        ["Home", "Marathon Performance Metrics", "Training Metrics", "Heart Rate Analysis","Route Visualization"],
        label_visibility="collapsed"
    )

    st.markdown("<hr>", unsafe_allow_html=True)

# Load datasets
activities_df = pd.read_csv("datasets/activities_dataset.csv")
challenges_df = pd.read_csv("datasets/global_challenges.csv")
vo2max_df = pd.read_csv("datasets/VO₂ Max.csv", skiprows=1, names=['Month', 'Activity Type', 'VO2 Max'])

# Prepare Heart Rate Data
# Filter out race distances (marathons > 40km) and ensure HR data exists
df_hr = activities_df[
    (activities_df['Activity Type'] == 'Run') &
    (activities_df['Average Heart Rate'].notna()) &
    (activities_df['Distance'] <= 40)
].copy()

# Parse dates and add Year column
df_hr['Activity Date'] = pd.to_datetime(df_hr['Activity Date'], format="%b %d, %Y, %I:%M:%S %p")
df_hr['Year'] = df_hr['Activity Date'].dt.year

# Calculate pace
df_hr['Pace (min/km)'] = 1000 / (df_hr['Average Speed'] * 60)
df_hr = df_hr.rename(columns={'Average Heart Rate': 'Avg HR (bpm)'})

# PAGE ROUTING 
if page == "Home":
    home.render(colors)

elif page == "Marathon Performance Metrics":
    marathon_performance.render(colors, vo2max_df)

elif page == "Training Metrics":
    training_metrics.render(colors, activities_df)

elif page == "Heart Rate Analysis":
    heart_rate_analysis.render(colors, df_hr)

elif page == "Route Visualization":
    route_visualization.render(colors)



# Footer (displayed on all pages)
st.markdown("<hr>", unsafe_allow_html=True)

# Enhanced footer with social links and attribution
st.markdown(
    f"""
    <div style='text-align: center; padding: 2rem 0 1rem 0;'>
        <div style='color: {colors[4]}; font-size: 0.9rem; line-height: 1.8; text-shadow: 0 0 8px {colors[4]}30;'>
            <p style='margin: 0.5rem 0;'>
                Built with passion by <strong style='color: {colors[0]}; text-shadow: 0 0 10px rgba(0, 217, 255, 0.3);'>Aditya Padmarajan</strong>
            </p>
            <p style='margin: 0.5rem 0; font-size: 0.8rem; opacity: 0.8;'>
                Data sourced from Strava • 2022-2025
            </p>
            <p style='margin: 1rem 0 0 0; font-size: 0.75rem; opacity: 0.6;'>
                "The difference between the impossible and the possible lies in a person's determination." — Tommy Lasorda
            </p>
        </div>
    </div>

    <!-- Back to Top Button -->
    <div id="backToTop" style='
        position: fixed;
        bottom: 30px;
        right: 30px;
        background: linear-gradient(135deg, {colors[0]} 0%, {colors[1]} 100%);
        color: {colors[3]};
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0, 217, 255, 0.4);
        transition: all 0.3s ease;
        z-index: 1000;
        font-size: 20px;
        font-weight: bold;
    ' onclick='window.scrollTo({{top: 0, behavior: "smooth"}})'
       onmouseover='this.style.transform="scale(1.1)"; this.style.boxShadow="0 6px 20px rgba(0, 217, 255, 0.6)"'
       onmouseout='this.style.transform="scale(1)"; this.style.boxShadow="0 4px 12px rgba(0, 217, 255, 0.4)"'>
        ↑
    </div>

    <script>
    // Show/hide back to top button based on scroll position
    window.onscroll = function() {{
        var backToTop = document.getElementById("backToTop");
        if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {{
            backToTop.style.opacity = "1";
            backToTop.style.pointerEvents = "auto";
        }} else {{
            backToTop.style.opacity = "0";
            backToTop.style.pointerEvents = "none";
        }}
    }};

    // Initial state
    document.getElementById("backToTop").style.opacity = "0";
    document.getElementById("backToTop").style.pointerEvents = "none";
    </script>
    """,
    unsafe_allow_html=True
)
