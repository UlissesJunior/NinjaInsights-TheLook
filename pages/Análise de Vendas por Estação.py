import os
from dotenv import load_dotenv
import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import matplotlib.pyplot as plt

load_dotenv()

credentials = service_account.Credentials.from_service_account_file('credentials.json')
project_id = os.getenv("PROJECT_ID")
client = bigquery.Client(credentials=credentials, project=project_id)

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

results = list(query_job.result())

def filter_results(selected_year, selected_months):
    return filter(
        lambda row: (row.year == selected_year and row.month in selected_months),
        results
    )
    
unique_years = sorted(set(row.year for row in results))

def print_results(filtered_results, season_name):
    total_vendas = 0
    st.write(f"{season_name}")
    for row in filtered_results:
        st.write(f"Ano: {row.year}, Mês: {row.month}, Número de Vendas: {row.num_sales}")
        total_vendas += row.num_sales
    st.write(f"Total de vendas na {season_name}: {total_vendas}")
    st.write("-------------------------")
    return total_vendas

selected_year = st.slider("Escolha o ano", min_value=min(unique_years), max_value=max(unique_years), value=min(unique_years))

summer_results = list(filter_results(selected_year - 1, [12])) + list(filter_results(selected_year, [1, 2]))
autumn_results = list(filter_results(selected_year, [3, 4, 5]))
winter_results = list(filter_results(selected_year, [6, 7, 8]))
spring_results = list(filter_results(selected_year, [9, 10, 11]))

total_summer = print_results(summer_results, "Verão")
total_autumn = print_results(autumn_results, "Outono")
total_winter = print_results(winter_results, "Inverno")
total_spring = print_results(spring_results, "Primavera")

total_geral = total_summer + total_autumn + total_winter + total_spring
st.write(f"Total Geral de Vendas: {total_geral}")

fig, ax = plt.subplots(2, 2, figsize=(12, 8))

if len(summer_results) >= 3 and summer_results[-3]:
    values_verao = [summer_results[-3].num_sales, summer_results[-2].num_sales, summer_results[-3].num_sales]
else:
    values_verao = [0, summer_results[-2].num_sales, summer_results[-1].num_sales]


ax[0, 0].bar(['Dez (Ano Anterior)', 'Jan', 'Fev'], values_verao)
ax[0, 0].set_title('Vendas no Verão')

ax[0, 1].bar(['Mar', 'Abr', 'Mai'], [autumn_results[-3].num_sales, autumn_results[-2].num_sales, autumn_results[-1].num_sales])
ax[0, 1].set_title('Vendas no Outono')

ax[1, 0].bar(['Jun', 'Jul', 'Ago'], [winter_results[-3].num_sales, winter_results[-2].num_sales, winter_results[-1].num_sales])
ax[1, 0].set_title('Vendas no Inverno')

ax[1, 1].bar(['Set', 'Out', 'Nov'], [spring_results[-3].num_sales, spring_results[-2].num_sales, spring_results[-1].num_sales])
ax[1, 1].set_title('Vendas na Primavera')

plt.tight_layout()
st.pyplot(fig)