# GemeindeAtlas-BL

## Overview

GemeindeAtlas-BL is a data visualization app focused on the municipality key figures (Gemeindekennzahlen) of the Canton of Basel-Landschaft. The data is sourced from [data.bl.ch](https://data.bl.ch/explore/dataset/10650/table/). This app is designed to offer an interactive, easy-to-use dashboard for comparing key metrics across different municipalities.

Live Demo: [GemeindeAtlas-BL App](https://gemeinde-atlas-bl.streamlit.app/)

## Technologies Used

- **Programming Language**: Python
- **Web Framework**: Streamlit
- **Data Visualization Libraries**: 
  - Folium for geospatial visualizations
  - Altair for statistical visualizations
  - Plotly for interactive charts

## Features

- **Compare Municipalities**: Easily compare key figures for different municipalities in Basel-Landschaft.
- **Interactive Dashboards**: Utilize interactive features for in-depth analysis.
- **Various Metrics**: View metrics related to population density, economic data, age distribution, and more.

## Installation & Running Locally

If you would like to run this app locally, please follow these steps:

```bash
# Clone the repository
git clone https://github.com/lcalmbach/gemeinde-atlas-bl.git

# Navigate to the project directory
cd gemeinde-atlas-bl

# Create a virtual environment
py -m venv env

# Activate the virtual environment
env\scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```