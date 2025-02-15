import requests

import pandas as pd

import folium

import streamlit as st

from streamlit_folium import st_folium

import folium.plugins



tectonic_plates = pd.read_csv('all.csv')

def get_color(value):
    if value < 3:
        return 'green'
    elif 3 < value < 5:
        return 'yellow'
    elif 5 < value < 7:
        return 'orange'
    elif 7 < value < 8:
        return 'red'
    else:
        return 'black'
def get_popup(row):
    return f"Location: {row['location']}<br>Magnitude: {row['magnitude']}"

complete_map = folium.Map()

plate_layer = folium.FeatureGroup(name='Tectonic Plates')

plates = list(tectonic_plates['plate'].unique())
for plate in plates:
    plate_vals = tectonic_plates[tectonic_plates['plate'] == plate]
    lats = plate_vals['lat'].values
    lons = plate_vals['lon'].values
    points = list(zip(lats, lons))
    indexes = [None] + [i + 1 for i, x in enumerate(points) if i < len(points) - 1 and abs(x[1] - points[i + 1][1]) > 300] + [None]

    for i in range(len(indexes) - 1):
        folium.vector_layers.PolyLine(points[indexes[i]:indexes[i+1]], popup=plate, color='red', fill=False).add_to(plate_layer)
plate_layer.add_to(complete_map)

all_quakes = folium.FeatureGroup(name='All earthquakes')
tsunami_quakes = folium.FeatureGroup(name='Tsunami earthquakes')
mag_2_3 = folium.FeatureGroup(name='Magnitude 2-3')
mag_3_5 = folium.FeatureGroup(name='Magnitude 3-5')
mag_5_7 = folium.FeatureGroup(name='Magnitude 5-7')
mag_7_8 = folium.FeatureGroup(name='Magnitude 7-8')
mag_8 = folium.FeatureGroup(name='Magnitude >8')

for index, row in df.iterrows():
    popup_str = get_popup(row)
    color = get_color(row['magnitude'])
    
    marker = folium.Marker(location=[row['latitude'], row['longitude']],
                           popup=popup_str,
                           icon=folium.Icon(color=color))
    if row['magnitude'] < 3:
        mag_2_3.add_child(marker)
    elif 3 <= row['magnitude'] < 5:
        mag_3_5.add_child(marker)
    elif 5 <= row['magnitude'] < 7:
        mag_5_7.add_child(marker)
    elif 7 <= row['magnitude'] < 8:
        mag_7_8.add_child(marker)
    else:
        mag_8.add_child(marker)
        
    all_quakes.add_child(marker)
    
    if row['tsunami'] == 1:
        tsunami_marker = folium.Marker(location=[row['latitude'], row['longitude']],
                                       popup=popup_str,
                                      icon=folium.Icon(color=color))
        tsunami_quakes.add_child(tsunami_marker)
           

complete_map.add_child(all_quakes)
complete_map.add_child(tsunami_quakes)
complete_map.add_child(mag_2_3)
complete_map.add_child(mag_3_5)
complete_map.add_child(mag_5_7)
complete_map.add_child(mag_7_8)
complete_map.add_child(mag_8)
    
folium.LayerControl(position='bottomleft', collapsed=False).add_to(complete_map)
    
folium.LayerControl().add_to(complete_map)

complete_map
