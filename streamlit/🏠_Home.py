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
df_elasticity = pd.read_csv('../data/treated/df_elasticity.csv')
df_elasticity = df_elasticity.drop(columns = ['Unnamed: 0'])
df_elasticity.columns = ['Produto','Elasticidade', 'Preco Medio', 'Demanda Média', 'Intercept', 'Slope', 'R²', 'P-Valor', 'Ranking']


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

    elasticity_type = ['Positiva', 'Negativa']
    elasticity_filter = st.multiselect("Selecione o Tipo da Elasticidade", options=elasticity_type, default=elasticity_type)  
    
    min_price, max_price = st.slider(
        'Selecione o intervalo de Preço Médio do Produto',
        min_value=float(df_elasticity['Preco Medio'].min()),
        max_value=float(df_elasticity['Preco Medio'].max()),
        value=(float(df_elasticity['Preco Medio'].min()), float(df_elasticity['Preco Medio'].max()))
    )
    # data_final = st.sidebar.date_input("Selecione a data final", value=data_final_default, min_value=min(df['timestamp']), max_value=max(df['timestamp']))
    
    # call_types = df['call_type'].unique()
    # call_type = st.multiselect("Selecione os Tipos de Corrida", options=call_types, default= call_types)

    # reactivation_trigger = st.sidebar.button('Reativar')



# ---------------------------------------------- filtro e transformações ----------------------------------------------

df_elasticity = df_elasticity.loc[(df_elasticity['Preco Medio'] >= min_price) & (df_elasticity['Preco Medio'] <= max_price), :]


if 'Positiva' in elasticity_filter and 'Negativa' not in elasticity_filter:
    df_elasticity = df_elasticity[df_elasticity['Elasticidade'] >= 0]
elif 'Negativa' in elasticity_filter and 'Positiva' not in elasticity_filter:
    df_elasticity = df_elasticity[df_elasticity['Elasticidade'] < 0]
else:
    df_elasticity = df_elasticity

df_elasticity = df_elasticity.reset_index(drop = True)

df_elasticity_csv = df_elasticity.to_csv(index=False, sep=';', encoding='latin1', decimal=',')
#---------------------------------------------------------------------------------
# Layout
#---------------------------------------------------------------------------------
st.title('Elasticidade de Preço - Bestbuy.com')

tab1, tab2 = st.tabs(['Gráfico', 'DataFrame'])

with tab1:
    st.header("Explicação Elasticidade Positiva e Negativa")

    st.markdown("""
                **Positiva:** A demanda pelo produto aumenta quando aumenta seu preço.
                - Exemplo: Elasticidade = 2 -> Um aumento de 2% no preço aumenta a demanda em 4%.\n
                **Negativa:** A demanda pelo produto aumenta quando diminui seu preço.
                - Exemplo: Elasticidade = 5 -> Uma diminuição de 2% no preço aumenta a demanda em 10%.
""")

    st.header("Explicações sobre os produtos selecionados:")
    st.markdown("- Dos 600 produtos, foram escolhidos os 43 que a Elasticidade teve respaldo estatístico.")

    fig = plot_elasticity(df_elasticity)
    st.pyplot(fig)

with tab2:
    st.dataframe(df_elasticity)
    
    st.download_button("Download CSV", df_elasticity_csv, "df_elasticity.csv","text/csv",key='download-csv')
#     col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
#     with col1:
#         motorista_unico_atual = df_atual['taxi_id'].nunique()
#         motorista_unico_past = df_passado['taxi_id'].nunique()
#         col1.metric('Motoristas Cadastrados', value =motorista_unico_atual, delta = (motorista_unico_atual - motorista_unico_past))
        
#     with col2:

#         pontos_unicos_atual = (df_atual['origin_stand'].nunique() - 1)
#         pontos_unicos_past = (df_passado['origin_stand'].nunique() - 1)
#         col2.metric('Pontos Cadastrados', value =pontos_unicos_atual, delta = (pontos_unicos_atual - pontos_unicos_past))
        
#     with col3:
#         numeros_unicos_atual = (df_atual['origin_call'].nunique() - 1)
#         numeros_unicos_past = (df_passado['origin_call'].nunique() - 1)
#         col3.metric('Números Cadastrados', value =numeros_unicos_atual, delta = (numeros_unicos_atual - numeros_unicos_past))

#     with col4:
#         total_corridas_essa = df1['trip_id'].nunique()
#         total_corridas_passada = df2['trip_id'].nunique()
    
#         aumento = (total_corridas_essa - total_corridas_passada)  
#         col4.metric("Corridas", value = total_corridas_essa, delta= aumento)

#     with col5:
#         motorista_ativa = df1['taxi_id'].nunique()
#         motorista_passada = df2['taxi_id'].nunique()
#         col5.metric('Motoristas Ativos',value = motorista_ativa, delta= (motorista_ativa - motorista_passada))
    
#     with col6:
#         corrida_motorista = np.round(total_corridas_essa/motorista_ativa, 2)
#         corrida_motorista_pass = np.round(total_corridas_passada/motorista_passada, 2)
#         delta6 = np.round(corrida_motorista - corrida_motorista_pass,2)
#         col6.metric('Relação Corridas/Motorista',value = corrida_motorista, delta= delta6)
    
#     with col7:
#         tempo_medio_atual = np.round(df1['time_spent'].mean(), 2) 
#         tempo_medio_past = np.round(df2['time_spent'].mean(), 2) 
#         mudanca = np.round((tempo_medio_atual - tempo_medio_past), 2)  
#         col7.metric("Tempo Médio", value = tempo_medio_atual, delta= mudanca)

# with st.container():
#     col1, col2= st.columns (2)
#     with col1:
#         st.title('Mapa Inicial')   
#         country_maps_inicial(df1)
#     with col2:
#         st.title('Mapa Final')   
#         country_maps_final(df1)






    