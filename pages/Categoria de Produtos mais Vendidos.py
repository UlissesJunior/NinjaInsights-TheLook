import streamlit as st
from client.client import run_client

query = """
SELECT
  products.category,
  COUNT(order_items.product_id) AS total_vendas
FROM
  `bigquery-public-data.thelook_ecommerce.order_items` AS order_items
JOIN
  `bigquery-public-data.thelook_ecommerce.products` AS products
ON
  order_items.product_id = products.id
WHERE
  order_items.status = "Complete"
GROUP BY
  products.category
ORDER BY
  total_vendas DESC
"""

results = run_client(query)
df = results.to_dataframe()

st.title("Categoria de Produtos mais Vendidos")

num_produtos = st.slider("Escolha o número das categorias mais vendidas a serem exibidos", min_value=1, max_value=len(df), value=10)

st.table(df.head(num_produtos))