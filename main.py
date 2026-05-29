import pandas as pd
import folium
from folium.plugins import HeatMap
import os
import time
import requests

def ensure_data_file(file_path):
    """Downloads the file if it doesn't exist locally or is older than 1 week."""
    url = "https://raw.githubusercontent.com/Ringmast4r/Global-Data-Center-Map/main/datacenters.xlsx"
    one_week_seconds = 7 * 24 * 60 * 60
    
    should_download = False
    if not os.path.exists(file_path):
        should_download = True
    else:
        file_age = time.time() - os.path.getmtime(file_path)
        if file_age > one_week_seconds:
            should_download = True
            
    if should_download:
        print(f"Downloading {file_path} from GitHub...")
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(file_path, 'wb') as f:
                f.write(response.content)
        except Exception as e:
            print(f"Failed to download file: {e}")

def generate_datacenter_heatmap(file_path):
    # Ensure the data file is present and up to date
    ensure_data_file(file_path)

    # Load the Excel file
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Data Cleaning: Convert Latitude and Longitude to floats
    # This handles cases where coordinates are strings with commas
    def clean_coordinate(value):
        if isinstance(value, str):
            return float(value.replace(',', '.'))
        return float(value)

    df['Latitude'] = df['Latitude'].apply(clean_coordinate)
    df['Longitude'] = df['Longitude'].apply(clean_coordinate)

    # Drop rows with missing coordinates
    df = df.dropna(subset=['Latitude', 'Longitude'])

    # Initialize a map centered at the average location
    avg_lat = df['Latitude'].mean()
    avg_lon = df['Longitude'].mean()
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=3, tiles='CartoDB positron')

    # Prepare data for HeatMap: a list of [lat, lon]
    heat_data = [[row['Latitude'], row['Longitude']] for index, row in df.iterrows()]

    # Add the heatmap layer
    HeatMap(heat_data, radius=15, blur=10, max_zoom=1).add_to(m)

    # Optional: Add markers for each datacenter with a popup
    for index, row in df.iterrows():
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=2,
            popup=f"{row['Name']} ({row['Company']})",
            color='blue',
            fill=True
        ).add_to(m)

    # Save the map to an HTML file
    output_file = 'datacenter_heatmap.html'
    m.save(output_file)
    print(f"Heatmap successfully generated: {output_file}")

if __name__ == "__main__":
    generate_datacenter_heatmap('datacenters.xlsx')
