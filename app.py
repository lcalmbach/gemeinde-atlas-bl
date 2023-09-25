import os
import streamlit as st
import geojson
import json
import pandas as pd

from plots import chloropleth_chart, barchart, radar_chart
import texts

__version__ = "0.0.4"
__author__ = "Lukas Calmbach"
__author_email__ = "lcalmbach@gmail.com"
VERSION_DATE = "2023-09-25"
APP_NAME = "GemeindeAtlas-BL"
GIT_REPO = "https://github.com/lcalmbach/gemeinde-atlas-bl"

gemeinden_json = "./gemeinden.json"


def init():
    st.set_page_config(
        page_title=APP_NAME,
        page_icon="🏠",
        layout="wide",
    )
    if "selected" not in st.session_state:
        st.session_state.selected = []


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


def get_radar_data(df):
    if len(df) > 0:
        vars = [
            "Landwirtschaftsfläche_Prozent",
            "Beschäftigte_2020",
            "Ausländeranteil_2022_Prozent",
            "Steuerertrag_2021_1000_CHF",
            "Steuerfuss_2023",
            "0_bis_14jährige_Prozent",
            "15_bis_64jährige_Prozent",
            "65jährige_und_älter_Prozent",
            "Arbeitsstätten_2020",
            "Einfamilienhäuser_Prozent",
            "Leerwohnungsziffer_2023_Prozent",
            "Bodenpreis_m2_Wohnbauland_2020_2022_CHF",
            "Bevölkerung_2022"
        ]
        vars_new_names = [
            "Landwirtschaftsfläche_Pzt",
            "Beschäftigte_pro_1000_Einw",
            "Ausländeranteil_Pzt",
            "Steuerertrag_CHF_pro_Einw",
            "Steuerfuss",
            "0_14_Jahre_Pzt",
            "15_64_Jahre_Pzt",
            "65_und_mehr_Jahre_Pzt",
            "Arbeitsstätten_pro_1000_Einw",
            "Einfamilienhäuser_Pzt",
            "Leerwohnungsziffer_Pzt",
            "Bodenpreis_1000_CHF_m2",
            "Bevölkerung"
        ]
        df_radar = df[["Gemeinde", "BFS_Nummer"] + vars]
        df_radar = df_radar.rename(columns=dict(zip(vars, vars_new_names)))
        vars_convert = ["Beschäftigte_pro_1000_Einw",
                        "Steuerertrag_CHF_pro_Einw",
                        "Arbeitsstätten_pro_1000_Einw",
        ]
        for var in vars_convert:
            df_radar[var] = df_radar[var] / df_radar["Bevölkerung"] * 1000

        ranges = {var: [df_radar[var].min(), df_radar[var].max()] for var in vars_new_names}

        for var in vars_new_names:
            max = df_radar[var].max()
            df_radar[var] = df_radar[var] / max * 5
        
        df_radar = df_radar[df_radar["BFS_Nummer"].isin(st.session_state.selected)]
        df_radar.drop(["BFS_Nummer"], axis=1, inplace=True)
        df_radar = df_radar.rename(columns={"Gemeinde": "name"})
        df_radar.drop(["Bevölkerung"], axis=1, inplace=True)
        return df_radar, ranges
    else:
        return None, None


def reset_gemeinde_selection():
    st.write(123)
    st.session_state.selected = []


def main():
    init()
    cols = st.columns([1, 20])
    with cols[0]:
        st.image("./liestal_tor.jpg")
    with cols[1]:
        st.header(APP_NAME)
    with st.expander("ℹ️ Info"):
        st.markdown(
            texts.intro
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
    # replace missing values: () by -1
    for col in df.columns:
        if not (col in ["Gemeinde", "Bezirk", "BFS_Nummer", "Webseite", "Geometrie", "Geometrisches_Zentrum"]):
            df[col] = df[col].replace('( )', -1)
            df[col] = df[col].astype('float64')
    options = get_options(df)
    selected_variable = st.selectbox("Wähle eine Kennzahl aus", options, on_change=reset_gemeinde_selection)
    settings = {
        "selected_variable": selected_variable,
        "var_geojson": var_geojson,
        "width": 700,
        "height": 500,
        "zoom": 10,
    }
    cols = st.columns([4, 3])
    with cols[0]:
        id = chloropleth_chart(df, settings)
        # add the id to the selected item is not already in the list
        # else remove it
        if id in st.session_state.selected:
            st.session_state.selected.remove(id)
        else:
            st.session_state.selected.append(id)
        if st.session_state.selected != []:
            data, ranges = get_radar_data(df)
            settings = {"title": "Rarar Chart", "range": [0, 5]}
            radar_chart(data, settings)
            text = texts.radar_chart
            st.markdown(text)
            df_ = pd.DataFrame(ranges).T
            df_.columns=["Min", "Max"]
            st.dataframe(df_)
            if st.button("Selektion zurücksetzen"):
                st.session_state.selected = []


    with cols[1]:
        if id > 0:
            gemeinde = df[df["BFS_Nummer"] == id]["Gemeinde"].iloc[0]
            tabs = st.tabs(["Rang", "Gemeinde Details", "Webseite"])
            with tabs[0]:
                df_bc = df[["BFS_Nummer", "Gemeinde", selected_variable]]
                df_bc['selected'] = df_bc["BFS_Nummer"].isin(st.session_state.selected)
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
                df_pivot = df_pivot.drop(
                    ["Webseite", "Geometrie", "Geometrisches_Zentrum"], axis=1
                )
                df_pivot = df_pivot.T
                df_pivot.columns = ["Wert"]
                st.dataframe(df_pivot)
            with tabs[2]:
                website = df[df["BFS_Nummer"] == id]["Webseite"].iloc[0]
                st.markdown(
                    f'<a href="https://{website}">Webseite der Gemeinde {gemeinde}</a>',
                    unsafe_allow_html=True,
                )


if __name__ == "__main__":
    main()
    cols = st.columns([1, 5])
    with cols[0]:
        st.markdown(get_app_info(), unsafe_allow_html=True)
