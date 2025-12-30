import streamlit as st
import pandas as pd
from gpx_utils import parse_activity_file


def render(colors):
    st.title("Marathon Route Visualization")
    st.markdown("*Marathon Routes*")

    st.markdown("<hr>", unsafe_allow_html=True)

    # Running Routes Collage - 20 Routes Combined
    st.markdown("### Training Routes Collage")
    st.markdown("*20 Running Routes Combined - Victoria & Vancouver, BC*")

    try:
        trackpoints_collage = parse_activity_file("GOTOES_2880330584911107.gpx")
        if trackpoints_collage:
            # Create DataFrame for st.map
            df_collage = pd.DataFrame(
                [(lat, lon) for lat, lon, _, _ in trackpoints_collage],
                columns=['lat', 'lon']
            )

            # Display the map with purple/magenta color to match the theme
            st.map(df_collage, color='#b957ff', size=20, zoom=11, use_container_width=True)
        else:
            st.error("Could not load running routes collage")
    except Exception as e:
        st.error(f"Error loading running routes collage: {e}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    # BMO 2025 Map
    st.markdown("### BMO Vancouver Marathon")

    try:
        trackpoints_bmo = parse_activity_file("activities/15342430162.tcx.gz")
        if trackpoints_bmo:
            # Create DataFrame for st.map
            df_bmo = pd.DataFrame(
                [(lat, lon) for lat, lon, _, _ in trackpoints_bmo],
                columns=['lat', 'lon']
            )

            # Display the map with green color
            st.map(df_bmo, color='#51cf66', size=20, zoom=11, use_container_width=True)
        else:
            st.error("Could not load BMO 2025 route")
    except Exception as e:
        st.error(f"Error loading BMO 2025 route: {e}")

    st.markdown("<br>", unsafe_allow_html=True)

    # RVM 2025 Map
    st.markdown("### Royal Victoria Marathon")

    try:
        trackpoints_rvm = parse_activity_file("activities/17205422180.fit.gz")
        if trackpoints_rvm:
            # Create DataFrame for st.map
            df_rvm = pd.DataFrame(
                [(lat, lon) for lat, lon, _, _ in trackpoints_rvm],
                columns=['lat', 'lon']
            )

            # Display the map with electric cyan color
            st.map(df_rvm, color='#00d9ff', size=20, zoom=13, use_container_width=True)
        else:
            st.error("Could not load RVM 2025 route")
    except Exception as e:
        st.error(f"Error loading RVM 2025 route: {e}")
