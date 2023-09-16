import os
import streamlit as st
from streamlit_folium import st_folium
import folium
import geojson
import json
import pandas as pd
import requests
import altair as alt
from plots import chloropleth_chart, barchart

__version__ = "0.0.2"
__author__ = "Lukas Calmbach"
__author_email__ = "lcalmbach@gmail.com"
VERSION_DATE = "2023-09-16"
APP_NAME = "GemeindeAtlas-BL"
GIT_REPO = "https://github.com/lcalmbach/gemeinde-atlas-bl"

gemeinden_json = "./gemeinden.json"


def init():
    st.set_page_config(
        page_title=APP_NAME,
        page_icon="🏠",
        layout="wide",
    )


def get_app_info():
    """
    Returns a string containing information about the application.
    Returns:
    - info (str): A formatted string containing details about the application.
    """

    info = f"""<div style="background-color:powderblue; padding: 10px;border-radius: 15px;">
    <small>Erstellt von <a href="mailto:{__author_email__}">{__author__}</a><br>
    Version: {__version__} ({VERSION_DATE})<br>
    Datenquelle: <a href="https://data.bl.ch>OGD Basel-Landschaft</a><br>
    Powered by:<a href="https://streamlit.io/">Streamlit</a>, <a href="https://github.com/python-visualization/folium">folium</a><br>
    <a href="{GIT_REPO}">git-repo</a><br>
    """
    return info


def get_feature(row):
    coordinates = json.loads(row["Geometrie"])["coordinates"][0]
    return geojson.Feature(
        geometry=geojson.Polygon(coordinates),
        properties={"Gemeinde": row["Gemeinde"], "BFS_Nummer": row["BFS_Nummer"]},
        id=row["BFS_Nummer"],
    )


def get_options(df):
    my_list = list(df.columns)
    # remove text columns
    indices_to_remove = {0, 1, 2, 3, 4, 29, 30, 31}
    for index in sorted(indices_to_remove, reverse=True):
        del my_list[index]
    return my_list


def main():
    init()
    cols = st.columns([1, 20])
    with cols[0]:
        st.image('./baslerstab.png')
    with cols[1]:
        st.header(APP_NAME)
    with st.expander("ℹ️ Info"):
        st.markdown(
            """Diese App zeigt dir verschiedene Informationen zu den Gemeinden im Kanton Basel-Landschaft 
([Datenquelle](https://data.bl.ch/explore/dataset/10650)). 
Zuerst wählst du eine Kennzahl aus, und danach klickst du auf eine Gemeinde. 
Neben der Karte siehst du anschliessend:
- eine Balkengrafik mit den Werten der Kennzahl aller Gemeinden, wobei die Gemeinde, die du ausgewählt hast rot markiert ist.
- Alle Werte für die Gemeinde als Tabelle.
- Einen Link auf die Webseite der Gemeinde.
        """
        )
    # Read the JSON file into a Python object
    df = pd.read_csv("./10650.csv", sep=";")
    if os.path.exists(gemeinden_json):
        with open(gemeinden_json, "r") as json_file:
            var_geojson = json.load(json_file)
    else:
        features_list = []
        for index, row in df.iterrows():
            features_list.append((get_feature(row)))
        var_geojson = geojson.FeatureCollection(features_list)

        with open(gemeinden_json, "w") as json_file:
            json.dump(var_geojson, json_file)

    options = get_options(df)
    selected_variable = st.selectbox("Wähle eine Kennzahl aus", options)
    settings = {
        "selected_variable": selected_variable,
        "var_geojson": var_geojson,
        "width": 700,
        "height": 400,
        "zoom": 10,
    }
    cols = st.columns([4, 3])
    with cols[0]:
        id = chloropleth_chart(df, settings)
    with cols[1]:
        if id > 0:
            gemeinde = df[df['BFS_Nummer'] == id]["Gemeinde"].iloc[0]
            tabs = st.tabs(["Rang", "Gemeinde Details", "Webseite"])
            with tabs[0]:
                df_bc = df[["BFS_Nummer", "Gemeinde", selected_variable]]
                settings = {
                    "y": "Gemeinde",
                    "x": f"{selected_variable}:Q",
                    "y_title": "",
                    "x_title": selected_variable,
                    "tooltip": ["Gemeinde", selected_variable],
                    "width": 400,
                    "height": 2000,
                    "title": f"{gemeinde} ({selected_variable})",
                    "sel_gemeinde": id,
                }
                barchart(df_bc, settings)
            with tabs[1]:
                df_pivot = df[df["BFS_Nummer"] == id]
                df_pivot = df_pivot.drop(['Webseite', 'Geometrie', 'Geometrisches_Zentrum'], axis=1)
                df_pivot = df_pivot.T
                df_pivot.columns = ['Wert']
                st.dataframe(df_pivot)
            with tabs[2]:
                website = df[df['BFS_Nummer'] == id]["Webseite"].iloc[0]
                st.markdown(f'<a href="https://{website}">Webseite der Gemeinde {gemeinde}</a>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
    cols = st.columns([1, 5])
    with cols[0]:
        st.markdown(get_app_info(), unsafe_allow_html=True)
