#------------------------------------------------------------------------------------
# Bibliotecas Necessarias
#------------------------------------------------------------------------------------

import pandas as pd
import numpy as np
# import inflection
import plotly.express as px
import streamlit as st
from PIL import Image
from matplotlib import pyplot as plt
# import folium
# from streamlit_folium import folium_static
# from folium.plugins import MarkerCluster

st.set_page_config(
    page_title="Main Page",
    page_icon="💸",
    layout= 'wide'
)
#------------------------------------------------------------------------------------
# Importando Dados
#------------------------------------------------------------------------------------
df_business = pd.read_csv('../data/treated/business.csv')
df_business = df_business.drop(columns = ['Unnamed: 0'])


#------------------------------------------------------------------------------------
# Funções
#------------------------------------------------------------------------------------
# Essa função tem como objetivo gerar um mapa com pontos nos locais do restaurantes de acordo com sua latitude e longitude. Todos os pontos possuem: 
# 1. Clusterização através do comando MarkerCluster
# 2. Ícone de uma casa branca e em volta a cor é de acordo com a avaliação (quanto mais verde melhor avaliado é o restaurante), dentro desse ícone tem:
    # 1. Nome do Restaurante
    # 2. Preço médio para dois e a moeda
    # 3. Tipo de culinária
    # 4. Nota de avaliação

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

    
# data_inicial_default = pd.to_datetime('2014-06-30').date()
# data_final_default = pd.to_datetime('2014-06-30').date()
# df['timestamp'] = pd.to_datetime(df['timestamp']).dt.date

#--------------------------------------------------------------------------
# Limpeza
#-------------------------------------------------------------------------

# Criando um filtro de datas no sidebar

#----------------------------------------------------------------------------------
# Sidebar
#---------------------------------------------------------------------------------
with st.sidebar:
    st.image('images/bestbuy.png')
  
    st.title('Bestbuy')  

    desconto = st.slider('Selecione o Desconto', min_value = 0, max_value = 30, value = 20, step = 5)
    aumento = st.slider('Selecione o Aumento', min_value = 0, max_value = 30, value = 10, step = 5)
    growth_percentage1 = st.slider('Selecione a Porcentagem de Aumento', min_value = 0, max_value = 200, value = 30, step = 10)

# ---------------------------------------------- feature engineering ----------------------------------------------
# criando variável com gasto total
desconto = desconto/100
aumento = aumento/100


feature_engineering(df_business, desconto, aumento)

df_business = df_business[(df_business['growth_spent'] > growth_percentage1)]
# df_business['growth_spent'] = df_business['growth_spent'].apply(lambda x: f"{x}%")


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



df_business.columns = ['Produto','Quantidade','Preco','Elasticidade', 'Faturamento', 'Novo Preco', 'Nova Quantidade','Novo Faturamento', 'Crescimento']
# df_business['Crescimento'] = df_business['Crescimento'].apply(lambda x: f"{x}%")


df_business_csv = df_business.to_csv(index=False, sep=';', encoding='latin1', decimal=',')

with tab2:

    st.dataframe(df_business)
    st.download_button("Download CSV", df_business_csv, "df_business.csv","text/csv",key='download-csv')






    