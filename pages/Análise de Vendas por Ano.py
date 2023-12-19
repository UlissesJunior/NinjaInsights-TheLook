import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from client.client import run_client

query= """
        SELECT EXTRACT(YEAR FROM created_at) AS year,
               EXTRACT(MONTH FROM created_at) AS month,
               COUNT(*) AS num_sales
        FROM `bigquery-public-data.thelook_ecommerce.orders`
        WHERE status = "Complete"
        GROUP BY year, month
        ORDER BY year, month
"""

results = run_client(query)

df = results.to_dataframe()

def plot_yearly_sales(df_year, selected_year):
    plt.figure(figsize=(10, 6))
    plt.bar(df_year['month'], df_year['num_sales'])
    plt.title(f'Vendas para o ano {selected_year}')
    plt.xlabel('Mês')
    plt.ylabel('Número de Vendas')
    st.pyplot(plt)

st.title("Análise de Vendas por Ano")

st.subheader("Vendas por ano")

selected_year = st.slider("Escolha o ano", min_value=min(df['year']), max_value=max(df['year']), value=min(df['year']))

df_year = df[df['year'] == selected_year]
df_year = df_year.sort_values(['year', 'month'])

plot_yearly_sales(df_year, selected_year)

sum_row = pd.DataFrame({
    'year': "",
    'month': "Total do Ano",
    'num_sales': [df_year['num_sales'].sum()]
})

df_year = pd.concat([df_year, sum_row]).reset_index(drop=True)

st.subheader("Dados detalhados")
st.table(df_year)