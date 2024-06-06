#------------------------------------------------------------------------------------
# Bibliotecas Necessarias
#------------------------------------------------------------------------------------

import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from PIL import Image
from matplotlib import pyplot as plt


st.set_page_config(
    page_title="Main Page",
    page_icon="💸",
    layout= 'wide'
)
#------------------------------------------------------------------------------------
# Importando Dados
#------------------------------------------------------------------------------------
df_elasticity = pd.read_csv('/home/tiagobarreto/DS/repos/elasticidade_preco/data/treated/df_elasticity.csv')
df_elasticity = df_elasticity.drop(columns = ['Unnamed: 0'])
df_elasticity.columns = ['Produto','Elasticidade', 'Preco Medio', 'Demanda Média', 'Intercept', 'Slope', 'R²', 'P-Valor', 'Ranking']


#------------------------------------------------------------------------------------
# Funções
#------------------------------------------------------------------------------------
# Essa função tem plotar o gráfico com as elasticidades
def plot_elasticity(df_elasticity):
    if len(df_elasticity) < 10:
        size = 10
    else:
        size = len(df_elasticity) / 2.4
    plt.figure(figsize=(20, size))
    plt.hlines(y=df_elasticity['Ranking'], xmin=0, xmax=df_elasticity['Elasticidade'], alpha=0.5, linewidth=3)

    for name, p in zip(df_elasticity['Produto'], df_elasticity['Ranking']):
        plt.text(4, p, name)

    # Add elasticity labels
    for x, y, s in zip(df_elasticity['Elasticidade'], df_elasticity['Ranking'], df_elasticity['Elasticidade']):
        vertical_adjustment = y + 0.15 if x > 0 else y
        plt.text(x, vertical_adjustment, round(s, 2), horizontalalignment='right' if x < 0 else 'left',
                 verticalalignment='bottom',
                 fontdict={'color': 'red' if x < 0 else 'green', 'size': 10})

    plt.gca().set(ylabel='Ranking Number', xlabel='Price Elasticity')
    plt.title('Price Elasticity', fontdict={'size': 13})
    plt.grid(linestyle='--')

    return plt


with st.sidebar:
    # carregando imagem
    st.image('/home/tiagobarreto/DS/repos/elasticidade_preco/streamlit/images/bestbuy.png')

    # título
    st.title('Bestbuy')  

    # criando filtro pelo tipo de elasticidade
    elasticity_type = ['Positiva', 'Negativa']
    elasticity_filter = st.multiselect("Selecione o Tipo da Elasticidade", options=elasticity_type, default=elasticity_type)  
    
    # criando filtro pelo tipo do produto
    min_price, max_price = st.slider(
        'Selecione o intervalo de Preço Médio do Produto',
        min_value=float(df_elasticity['Preco Medio'].min()),
        max_value=float(df_elasticity['Preco Medio'].max()),
        value=(float(df_elasticity['Preco Medio'].min()), float(df_elasticity['Preco Medio'].max()))
    )
    

# ---------------------------------------------- filtro e transformações ----------------------------------------------

# filtrando pelo preço
df_elasticity = df_elasticity.loc[(df_elasticity['Preco Medio'] >= min_price) & (df_elasticity['Preco Medio'] <= max_price), :]

# filtrando pelo tipo de elasticidade
if 'Positiva' in elasticity_filter and 'Negativa' not in elasticity_filter:
    df_elasticity = df_elasticity[df_elasticity['Elasticidade'] >= 0]
elif 'Negativa' in elasticity_filter and 'Positiva' not in elasticity_filter:
    df_elasticity = df_elasticity[df_elasticity['Elasticidade'] < 0]
else:
    df_elasticity = df_elasticity

# resetando o index
df_elasticity = df_elasticity.reset_index(drop = True)

# transformando o dataframe em csv
df_elasticity_csv = df_elasticity.to_csv(index=False, sep=';', encoding='latin1', decimal=',')

#---------------------------------------------------------------------------------
# Layout
#---------------------------------------------------------------------------------
st.title('Elasticidade de Preço - Bestbuy.com')

tab1, tab2 = st.tabs(['Gráfico', 'DataFrame'])

with tab1:
    # titulo
    st.header("Explicação Elasticidade Positiva e Negativa")

    # explicacao elasticidade
    st.markdown("""
                **Positiva:** A demanda pelo produto aumenta quando aumenta seu preço.
                - Exemplo: Elasticidade = 2 -> Um aumento de 2% no preço aumenta a demanda em 4%.\n
                **Negativa:** A demanda pelo produto aumenta quando diminui seu preço.
                - Exemplo: Elasticidade = 5 -> Uma diminuição de 2% no preço aumenta a demanda em 10%.
""")
    
    # titulo
    st.header("Explicações sobre os produtos selecionados:")

    # explicacao selecao produtos
    st.markdown("- Dos 600 produtos, foram escolhidos os 43 que a Elasticidade teve respaldo estatístico.")

    # usando a funcao para gerar o grafico
    fig = plot_elasticity(df_elasticity)

    # plotando o grafico
    st.pyplot(fig)

with tab2:
    # plotando o dataframe
    st.dataframe(df_elasticity)
    
    # adicionando botao de download dos dados
    st.download_button("Download CSV", df_elasticity_csv, "df_elasticity.csv","text/csv",key='download-csv')






    