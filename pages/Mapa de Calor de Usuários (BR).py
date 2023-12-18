import streamlit as st
import folium
from folium.plugins import HeatMap
import pandas as pd
import ast

csv_path = 'database/coordenadas.csv' 

df = pd.read_csv(csv_path)
df['coordinates'] = df['coordinates'].apply(ast.literal_eval)

heat_data = [[row['coordinates'][0], row['coordinates'][1]] for index, row in df.iterrows() if pd.notnull(row['coordinates'])]

mean_latitude = df['coordinates'].apply(lambda x: x[0]).mean()
mean_longitude = df['coordinates'].apply(lambda x: x[1]).mean()
mymap = folium.Map(location=[mean_latitude, mean_longitude], zoom_start=2)

st.title("Mapa de Calor de Usuários")

HeatMap(heat_data).add_to(mymap)
map_html = mymap._repr_html_()
st.components.v1.html(map_html, width=700, height=500, scrolling=True)

st.title("Dados Detalhados")
st.dataframe(df) 