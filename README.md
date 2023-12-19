<h1 align="center">
🥷🖥️<br>Tech4Humans - Projeto de Análise de Dados do The Look Ecommerce 
</h1>

Bem-vindo ao repositório do projeto de análise de dados desenvolvido para a Tech4Humans em parceria com a Ninja Startup Job e o CEU UNIFEI. 
Este projeto utiliza a biblioteca Streamlit e outras ferramentas Python para fornecer análises detalhadas do banco de dados The Look Ecommerce. 

<p align="center">
<img src="images/banner.png">
<p>

<h4 align="center"><a href="https://ninjainsights-thelook-deploy.streamlit.app/">Clique para visitar o projeto</a></h4>

---

## Sumário  
1. [Introdução](#introdução)
 2. [Instalação](#instalação)
 3. [Configuração](#configuração)
 4. [Como Executar](#como-executar)
 5. [Páginas do Aplicativo](#páginas-do-aplicativo) 
 6. [Bibliotecas Utilizadas](#bibliotecas-utilizadas) 
 7. [Licença](#licença) 
## Introdução 

Este projeto foi desenvolvido como parte da posição de Analista de Dados na Tech4Humans, em colaboração com a Ninja Startup Job. O objetivo principal é analisar dados do The Look Ecommerce e apresentar insights de maneira interativa através de uma aplicação web construída com Streamlit. 

## Instalação 

Certifique-se de ter o Python e o pip instalados em seu ambiente. Em seguida, execute o seguinte comando para instalar as dependências: 

```pip install -r requirements.txt```

## Configuração

Antes de executar o aplicativo, você precisa configurar suas credenciais para acessar o banco de dados BigQuery. 

Siga as instruções deixadas pelos membros do CEU para conseguir suas credencias e ID de projeto: [INSTRUÇÕES](https://colab.research.google.com/drive/111psZJNkil95u3uAUmY56cAdO4R3GG7j?usp=sharing)

Crie um arquivo `.env` na raiz do projeto e adicione as seguintes variáveis:

```
PROJECT_ID=12345
GOOGLE_APPLICATION_CREDENTIALS=/caminho/para/sua/credencial.json
``` 

Substitua "12345" pelo seu project id e  "/caminho/para/sua/credencial.json" pelo caminho real para suas credenciais do Google Cloud.

## Como Executar

Para iniciar a aplicação, execute o seguinte comando:

`streamlit run Home.py` 

Isso iniciará um servidor local e abrirá o aplicativo em seu navegador padrão.

## Páginas do Aplicativo

### Home

Página inicial com uma visão geral do projeto.

### Análise de Vendas por Ano

Análise das vendas anuais por gráficos e tabelas.

### Análise de Vendas por Estação

Análise das vendas distribuídas ao longo das estações do ano por gráficos e tabelas.

### Análise de Vendas por Mês

Análise das vendas mensais por gráficos e tabelas.

### Categoria de Produtos mais Vendidos

Tabela das categorias de produtos mais vendidos.

### Mapa de Calor de Usuários (BR)

Mapa de calor destacando a distribuição geográfica dos usuários no Brasil*.
</br>
(*): A big query do the look ecommerce atualiza a cada dia, durante a execução desse código, precisei converter os códigos postais da tabela users para latitude e longitude com geopy, fiz a conversão apenas com os dados do Brasil, mas ainda assim, alguns dados tinham na coluna country "Brasil" e código postal de outros países.
Query utilizado para filtragem no google collab: 
```
SELECT *

FROM `bigquery-public-data.thelook_ecommerce.users`

WHERE postal_code IS NOT NULL AND country = 'Brasil'
```  

### Mapa dos Centros de Distribuição

Mapa interativo mostrando a localização dos centros de distribuição do ecommerce.

### Produtos mais Vendidos

Tabela e gráficos dos produtos mais vendidos.

### Tráfego de Páginas

Análise do tráfego nas páginas do The Look Ecommerce com tabela e gráfico de dispersão.

## Bibliotecas Utilizadas

-   Streamlit
-   Pandas
-   Plotly
-   Google Cloud BigQuery
-   Folium
-   Python-dotenv
-   Matplotlib
-   DB-Dtypes

## Licença

Este projeto é licenciado sob a [MIT License](https://github.com/UlissesJunior/NinjaInsights-TheLook/blob/main/LICENSE).