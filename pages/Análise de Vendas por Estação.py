import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from client.client import run_client

query = """
    SELECT EXTRACT(YEAR FROM created_at) AS year,
           EXTRACT(MONTH FROM created_at) AS month,
           COUNT(*) AS num_sales
    FROM `bigquery-public-data.thelook_ecommerce.orders`
    WHERE status = "Complete"
    GROUP BY year, month
    ORDER BY year, month
"""

results = list(run_client(query))

def filter_results(selected_year, selected_months):
    return filter(
        lambda row: (row.year == selected_year and row.month in selected_months),
        results
    )
    
unique_years = sorted(set(row.year for row in results))

def get_table_data(filtered_results):
    total_vendas = 0
    table_data = []
    for row in filtered_results:
        table_data.append([row.year, row.month, row.num_sales])
        total_vendas += row.num_sales
    table_data.append(["", "Total", total_vendas])
    return table_data

st.title("Análise de Vendas por Estação")

selected_year = st.slider("Escolha o ano", min_value=min(unique_years), max_value=max(unique_years), value=min(unique_years))

summer_results = list(filter_results(selected_year - 1, [12])) + list(filter_results(selected_year, [1, 2]))
autumn_results = list(filter_results(selected_year, [3, 4, 5]))
winter_results = list(filter_results(selected_year, [6, 7, 8]))
spring_results = list(filter_results(selected_year, [9, 10, 11]))

total_summer = sum(row.num_sales for row in summer_results)
total_autumn = sum(row.num_sales for row in autumn_results)
total_winter = sum(row.num_sales for row in winter_results)
total_spring = sum(row.num_sales for row in spring_results)

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

st.subheader("Tabela de Vendas no Verão")
st.table(pd.DataFrame(get_table_data(summer_results), columns=["Ano", "Mês", "Número de Vendas"]))

st.subheader("Tabela de Vendas no Outono")
st.table(pd.DataFrame(get_table_data(autumn_results), columns=["Ano", "Mês", "Número de Vendas"]))

st.subheader("Tabela de Vendas no Inverno")
st.table(pd.DataFrame(get_table_data(winter_results), columns=["Ano", "Mês", "Número de Vendas"]))

st.subheader("Tabela de Vendas na Primavera")
st.table(pd.DataFrame(get_table_data(spring_results), columns=["Ano", "Mês", "Número de Vendas"]))

total_geral = total_summer + total_autumn + total_winter + total_spring
st.subheader(f"Total Geral de Vendas: {total_geral}")