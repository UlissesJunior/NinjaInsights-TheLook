import streamlit as st
import folium
import pandas as pd
from client.client import run_client

query = """
    SELECT name, latitude, longitude
    FROM `bigquery-public-data.thelook_ecommerce.distribution_centers`
"""

results = run_client(query)
df = results.to_dataframe()

mymap = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=3)

for index, row in df.iterrows():
    if pd.notnull(row['latitude']) and pd.notnull(row['longitude']):
        folium.Marker(location=[row['latitude'], row['longitude']], popup=row['name']).add_to(mymap)

st.title("Mapa dos Centros de Distribuição")

st.components.v1.html(mymap._repr_html_(), height=430)

st.table(df)