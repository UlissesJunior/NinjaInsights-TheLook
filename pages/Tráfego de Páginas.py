import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from client.client import run_client

query = """
    SELECT
      event_type,
      COUNT(*) AS count
    FROM
      `bigquery-public-data.thelook_ecommerce.events`
    GROUP BY
      event_type
    ORDER BY
      count DESC
"""

results = run_client(query)
df = results.to_dataframe()

st.title("Tráfego de Páginas")

fig, ax = plt.subplots()
ax.scatter(df['event_type'], df['count'])
ax.set_title('Contagem de Eventos por Tipo')
ax.set_ylabel('Contagem')
ax.set_xlabel('Tipo de Evento')
st.pyplot(fig)

st.subheader("Dados detalhados")
st.table(df)
