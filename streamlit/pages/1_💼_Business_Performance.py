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
df_business = pd.read_csv('/home/tiagobarreto/DS/repos/elasticidade_preco/data/treated/business.csv')
df_business = df_business.drop(columns = ['Unnamed: 0'])


#------------------------------------------------------------------------------------
# Funções
#------------------------------------------------------------------------------------
# Essa função tem como criar novas colunas e calcular os novos preços e novas quantidades a partir do desconto e aumento fornecido
def feature_engineering(df8, desconto , aumento):
    df8.loc[:, 'total_spent'] = df8['date_imp'] * df8['price']

    # criando o novo preço
    # - se a elasticidade for negativa vai ter um desconto de 25% nos produtos
    # - se a elasticidade for positiva vai ter um aumento de 10% nos produtos
    df8['new_price'] = df8.apply(lambda x: x['price'] * (1- desconto)
                                if (x['price_elasticity'] < 0) 
                                else x['price'] * (1 + aumento), 
                                axis = 1)


    # criando a nova quantidade
    # - se a elasticidade for negativa vai ter um aumento na demanda de 1 + 0.25 x elasticidade 
    # - se a elasticidade for positiva vai ter um aumento na demanda de 1 + 0.10 x elasticidade 
    df8['new_quantity'] = df8.apply(lambda x: x['date_imp'] * (1 + desconto * abs(x['price_elasticity']))
                                    if (x['price_elasticity'] < 0) 
                                    else x['date_imp'] * (1 + aumento * abs(x['price_elasticity'])), 
                                    axis=1)

    # arredonando a quantidade                     
    df8['new_quantity'] = np.round(df8['new_quantity'], 0)

    # calculando novo gasto total
    df8['new_spent'] = abs(df8['new_price'] * df8['new_quantity'])

    # calculando crescimento de lucro por produto
    df8['growth_spent'] = np.round(100 *(df8['new_spent'] - df8['total_spent']) / df8['total_spent'], 2)

    return df8
#-----------------------------------------------------------------

# Sidebar
#---------------------------------------------------------------------------------
with st.sidebar:
    # carregando imagem
    st.image('/home/tiagobarreto/DS/repos/elasticidade_preco/streamlit/images/bestbuy.png')
    
    # título
    st.title('Bestbuy')  

    # filtro desconto
    desconto = st.slider('Selecione o Desconto', min_value = 0, max_value = 30, value = 20, step = 5)

    # filtro desconto
    aumento = st.slider('Selecione o Aumento', min_value = 0, max_value = 30, value = 10, step = 5)

    # filtro crescimento
    growth_percentage1 = st.slider('Selecione a Porcentagem de Aumento', min_value = 0, max_value = 200, value = 30, step = 10)

# ---------------------------------------------- feature engineering ----------------------------------------------
# dividindo o desconto por 100 para poder realizar cálculos
desconto = desconto/100
aumento = aumento/100

# função transforma o dataframe e cria novas colunas
feature_engineering(df_business, desconto, aumento)

# filtragem pelo percentual de crescimento
df_business = df_business[(df_business['growth_spent'] > growth_percentage1)]

# variaveis para o resultado da simulação
faturamento_dez = np.round(df_business['total_spent'].sum(), 2)
faturamento_exp = np.round(df_business['new_spent'].sum(), 2)
growth = np.round(100* (faturamento_exp - faturamento_dez) / faturamento_dez, 2)

#---------------------------------------------------------------------------------
# Layout
#---------------------------------------------------------------------------------
st.title('Elasticidade de Preço - Bestbuy.com')

tab1, tab2 = st.tabs(['Resultado', 'DataFrame'])

with tab1:
    with st.container():
        st.header("Explicação da Simulação:")
        st.markdown("- Dos 42 produtos selecionados anteriormente realizei uma filtragem pelos que tiveram vendas em Dezembro de 2017 para a simulação, resultando em 24 produtos.")
        
        st.header("Resultado da Simulação:")
        st.markdown(f'- Faturamento Dezembro 2017 sem otimização de preços: ${faturamento_dez}')
        st.markdown(f'- Expectativa faturamento Janeiro 2018 com otimização de preços: ${faturamento_exp}')
        st.markdown(f'- Crescimento no Faturamento: {growth}%')


# trocando nome das colunas
df_business.columns = ['Produto','Quantidade','Preco','Elasticidade', 'Faturamento', 'Novo Preco', 'Nova Quantidade','Novo Faturamento', 'Crescimento']

# exportando o dataframe como csv
df_business_csv = df_business.to_csv(index=False, sep=';', encoding='latin1', decimal=',')

with tab2:
    st.dataframe(df_business)
    st.download_button("Download CSV", df_business_csv, "df_business.csv","text/csv",key='download-csv')






    