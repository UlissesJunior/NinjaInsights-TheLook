import os
from dotenv import load_dotenv
import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import matplotlib.pyplot as plt

credentials = service_account.Credentials.from_service_account_file('credentials.json')
project_id = os.getenv("PROJECT_ID")
client = bigquery.Client(credentials=credentials, project=project_id)

def query_bigquery():
    query_string = """
        SELECT EXTRACT(YEAR FROM created_at) AS year,
               EXTRACT(MONTH FROM created_at) AS month,
               COUNT(*) AS num_sales
        FROM `bigquery-public-data.thelook_ecommerce.orders`
        WHERE status = "Complete"
        GROUP BY year, month
        ORDER BY year, month
    """
    query_job = client.query(query_string)
    results = query_job.result()
    df = results.to_dataframe()
    return df

def plot_yearly_sales(df_year, selected_year):
    plt.figure(figsize=(10, 6))
    plt.bar(df_year['month'], df_year['num_sales'])
    plt.title(f'Vendas para o ano {selected_year}')
    plt.xlabel('Mês')
    plt.ylabel('Número de Vendas')
    st.pyplot(plt)

st.title("Análise de Vendas por Ano")

st.subheader("Vendas por ano")

df = query_bigquery()

selected_year = st.slider("Escolha o ano", min_value=2019, max_value=2023, value=2019)

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