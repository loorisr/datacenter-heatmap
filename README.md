# Datacenter Heatmap Generator

This project generates an interactive heatmap and marker map of global datacenters. It automatically fetches the latest data and produces a web-ready HTML visualization.

## Data Source

Datacenter information is sourced from the [Global-Data-Center-Map](https://github.com/Ringmast4r/Global-Data-Center-Map) repository.

## Features

- **Data Automation**: Automatically downloads and updates the datacenter database (Excel format) if the local copy is older than a week.
- **Interactive Visualization**: Uses Leaflet.js (via Folium) to show datacenter density and individual site details.
- **CI/CD Ready**: Includes GitHub Actions configuration for automated weekly updates and deployment to GitHub Pages.

## Getting Started

The generator uses `pandas` for data processing and `folium` for map generation.

1. Install dependencies:
   ```bash
   pip install pandas folium requests openpyxl
   ```
2. Run the generator:
   ```bash
   python main.py
   ```

## GitHub Pages Deployment

The project includes a `deploy.yml` workflow. When placed in `.github/workflows/`, it will:
1. Run every Monday at midnight to refresh the data.
2. Generate the map and deploy it to your GitHub Pages site automatically.