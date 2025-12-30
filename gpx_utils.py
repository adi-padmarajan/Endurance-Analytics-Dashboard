"""
GPX/TCX/FIT Parsing Utilities for Route Visualization
"""

import gzip
import gpxpy
import xml.etree.ElementTree as ET
from typing import List, Tuple, Optional
import numpy as np
from fitparse import FitFile
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_gpx_file(filepath: str) -> List[Tuple[float, float, Optional[float], Optional[int]]]:
    """
    Parse a GPX file (compressed or uncompressed) and extract trackpoints.

    Returns:
        List of tuples (latitude, longitude, elevation, heart_rate)
    """
    try:
        # Handle .gz compressed files
        if filepath.endswith('.gz'):
            with gzip.open(filepath, 'rt', encoding='utf-8') as f:
                gpx = gpxpy.parse(f)
        else:
            with open(filepath, 'r', encoding='utf-8') as f:
                gpx = gpxpy.parse(f)

        trackpoints = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    # GPX doesn't have HR by default, set to None
                    trackpoints.append((
                        point.latitude,
                        point.longitude,
                        point.elevation,
                        None  # Heart rate not in standard GPX
                    ))

        return trackpoints
    except Exception as e:
        logger.error(f"Error parsing GPX file {filepath}: {e}")
        return []


def parse_tcx_file(filepath: str) -> List[Tuple[float, float, Optional[float], Optional[int]]]:
    """
    Parse a TCX file (compressed or uncompressed) and extract trackpoints.

    Returns:
        List of tuples (latitude, longitude, elevation, heart_rate)
    """
    try:
        # Handle .gz compressed files
        if filepath.endswith('.gz'):
            with gzip.open(filepath, 'rt', encoding='utf-8') as f:
                tree = ET.parse(f)
        else:
            with open(filepath, 'r', encoding='utf-8') as f:
                tree = ET.parse(f)

        root = tree.getroot()

        # TCX namespace
        ns = {'ns': 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2'}

        trackpoints = []
        for trackpoint in root.findall('.//ns:Trackpoint', ns):
            position = trackpoint.find('ns:Position', ns)
            if position is not None:
                lat_elem = position.find('ns:LatitudeDegrees', ns)
                lon_elem = position.find('ns:LongitudeDegrees', ns)

                if lat_elem is not None and lon_elem is not None:
                    lat = float(lat_elem.text)
                    lon = float(lon_elem.text)

                    # Get elevation if available
                    alt_elem = trackpoint.find('ns:AltitudeMeters', ns)
                    elevation = float(alt_elem.text) if alt_elem is not None else None

                    # Get heart rate if available
                    hr_elem = trackpoint.find('.//ns:HeartRateBpm/ns:Value', ns)
                    heart_rate = int(hr_elem.text) if hr_elem is not None else None

                    trackpoints.append((lat, lon, elevation, heart_rate))

        return trackpoints
    except Exception as e:
        logger.error(f"Error parsing TCX file {filepath}: {e}")
        return []


def parse_fit_file(filepath: str) -> List[Tuple[float, float, Optional[float], Optional[int]]]:
    """
    Parse a FIT file (compressed or uncompressed) and extract trackpoints.

    Returns:
        List of tuples (latitude, longitude, elevation, heart_rate)
    """
    try:
        # Handle .gz compressed files - decompress first
        if filepath.endswith('.gz'):
            import tempfile
            import os

            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.fit') as tmp_file:
                tmp_path = tmp_file.name

            # Decompress to temporary file
            with gzip.open(filepath, 'rb') as f_in:
                with open(tmp_path, 'wb') as f_out:
                    f_out.write(f_in.read())

            # Parse the decompressed file
            fitfile = FitFile(tmp_path)

            # Clean up
            os.unlink(tmp_path)
        else:
            fitfile = FitFile(filepath)

        trackpoints = []

        # Get all records from the FIT file
        for record in fitfile.get_messages('record'):
            lat = None
            lon = None
            elevation = None
            heart_rate = None

            for record_data in record:
                if record_data.name == 'position_lat':
                    lat = record_data.value * (180.0 / 2**31) if record_data.value else None
                elif record_data.name == 'position_long':
                    lon = record_data.value * (180.0 / 2**31) if record_data.value else None
                elif record_data.name == 'altitude':
                    elevation = record_data.value
                elif record_data.name == 'heart_rate':
                    heart_rate = record_data.value

            # Only add if we have valid coordinates
            if lat is not None and lon is not None:
                trackpoints.append((lat, lon, elevation, heart_rate))

        return trackpoints
    except Exception as e:
        logger.error(f"Error parsing FIT file {filepath}: {e}")
        return []


def parse_activity_file(filepath: str) -> List[Tuple[float, float, Optional[float], Optional[int]]]:
    """
    Auto-detect file type and parse accordingly.

    Returns:
        List of tuples (latitude, longitude, elevation, heart_rate)
    """
    if 'gpx' in filepath.lower():
        return parse_gpx_file(filepath)
    elif 'tcx' in filepath.lower():
        return parse_tcx_file(filepath)
    elif 'fit' in filepath.lower():
        return parse_fit_file(filepath)
    else:
        logger.warning(f"Unknown file format: {filepath}")
        return []


def calculate_pace_segments(trackpoints: List[Tuple], segment_distance_km: float = 1.0) -> List[dict]:
    """
    Calculate pace for segments of the route (e.g., every 1km).

    Args:
        trackpoints: List of (lat, lon, elevation, hr) tuples
        segment_distance_km: Distance for each segment in kilometers

    Returns:
        List of segment data with avg pace, location, etc.
    """
    from math import radians, sin, cos, sqrt, atan2

    def haversine(lat1, lon1, lat2, lon2):
        """Calculate distance between two points in km"""
        R = 6371  # Earth radius in km

        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))

        return R * c

    if not trackpoints:
        return []

    segments = []
    segment_start_idx = 0
    cumulative_distance = 0
    segment_num = 0

    for i in range(1, len(trackpoints)):
        lat1, lon1, _, _ = trackpoints[i-1]
        lat2, lon2, _, _ = trackpoints[i]

        distance = haversine(lat1, lon1, lat2, lon2)
        cumulative_distance += distance

        if cumulative_distance >= segment_distance_km:
            # Calculate segment stats
            segment_points = trackpoints[segment_start_idx:i+1]

            # Center point of segment
            center_lat = np.mean([p[0] for p in segment_points])
            center_lon = np.mean([p[1] for p in segment_points])

            # Average elevation and HR if available
            elevations = [p[2] for p in segment_points if p[2] is not None]
            heart_rates = [p[3] for p in segment_points if p[3] is not None]

            avg_elevation = np.mean(elevations) if elevations else None
            avg_hr = np.mean(heart_rates) if heart_rates else None

            segments.append({
                'segment_num': segment_num,
                'distance_km': segment_num * segment_distance_km,
                'center_lat': center_lat,
                'center_lon': center_lon,
                'avg_elevation': avg_elevation,
                'avg_hr': avg_hr
            })

            segment_num += 1
            segment_start_idx = i
            cumulative_distance = 0

    return segments


def get_route_bounds(trackpoints: List[Tuple]) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """
    Get the bounding box of the route.

    Returns:
        ((min_lat, min_lon), (max_lat, max_lon))
    """
    if not trackpoints:
        return ((0, 0), (0, 0))

    lats = [p[0] for p in trackpoints]
    lons = [p[1] for p in trackpoints]

    return ((min(lats), min(lons)), (max(lats), max(lons)))


def get_center_point(trackpoints: List[Tuple]) -> Tuple[float, float]:
    """
    Get the center point of the route.

    Returns:
        (center_lat, center_lon)
    """
    if not trackpoints:
        return (0, 0)

    lats = [p[0] for p in trackpoints]
    lons = [p[1] for p in trackpoints]

    return (np.mean(lats), np.mean(lons))
