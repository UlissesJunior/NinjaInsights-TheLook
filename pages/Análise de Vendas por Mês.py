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
               EXTRACT(DAY FROM created_at) AS day,
               COUNT(*) AS num_sales
        FROM `bigquery-public-data.thelook_ecommerce.orders`
        WHERE status = "Complete"
        GROUP BY year, month, day
        ORDER BY year, month, day
    """
    query_job = client.query(query_string)
    results = query_job.result()
    df = results.to_dataframe()
    return df

def plot_monthly_sales(df_month):
    plt.figure(figsize=(10, 6))
    plt.bar(df_month['day'], df_month['num_sales'])
    plt.title(f'Vendas para o mês {df_month["month"].iloc[0]}/{df_month["year"].iloc[0]}')
    plt.xlabel('Dia do mês')
    plt.ylabel('Número de Vendas')
    st.pyplot(plt)

st.title("Análise de Vendas por Mês")
st.subheader("Vendas por mês")

df = query_bigquery()

year = st.slider("Escolha o ano", min_value=2019, max_value=2023, value=2019)
month = st.slider("Escolha o mês", min_value=1, max_value=12, value=1)

df_month = df[(df['year'] == year) & (df['month'] == month)]
df_month = df_month.sort_values('day')

plot_monthly_sales(df_month)

sum_row = pd.DataFrame({
    'year': "",
    'month': "",
    'day': ['Total do mês'],
    'num_sales': [df_month['num_sales'].sum()]
})
df_month = pd.concat([df_month, sum_row]).reset_index(drop=True)

st.subheader("Dados detalhados")
st.table(df_month)