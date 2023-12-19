import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from client.client import run_client

query = """
        SELECT EXTRACT(YEAR FROM created_at) AS year,
               EXTRACT(MONTH FROM created_at) AS month,
               EXTRACT(DAY FROM created_at) AS day,
               COUNT(*) AS num_sales
        FROM `bigquery-public-data.thelook_ecommerce.orders`
        WHERE status = "Complete"
        GROUP BY year, month, day
        ORDER BY year, month, day
"""

results = run_client(query)
df = results.to_dataframe()

def plot_monthly_sales(df_month):
    plt.figure(figsize=(10, 6))
    plt.bar(df_month['day'], df_month['num_sales'])
    plt.title(f'Vendas para o mês {df_month["month"].iloc[0]}/{df_month["year"].iloc[0]}')
    plt.xlabel('Dia do mês')
    plt.ylabel('Número de Vendas')
    st.pyplot(plt)

st.title("Análise de Vendas por Mês")
st.subheader("Vendas por mês")

year = st.slider("Escolha o ano", min_value=min(df['year']), max_value=max(df['year']), value=min(df['year']))
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