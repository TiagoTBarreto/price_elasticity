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
df_cross_elasticity = pd.read_csv('../data/treated/cross_elasticity.csv')
df_cross_elasticity = df_cross_elasticity.drop(columns = ['Unnamed: 0'])


#------------------------------------------------------------------------------------
# Funções
#------------------------------------------------------------------------------------

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

    product_type = ['Substituto', 'Complementar']
    product_filter = st.multiselect("Selecione o Tipo do Produto", options=product_type, default=product_type)  

# ---------------------------------------------- feature engineering ----------------------------------------------

# df_cross_elasticity['growth_spent'] = df_cross_elasticity['growth_spent'].apply(lambda x: f"{x}%")


if 'Substituto' in product_filter and 'Complementar' not in product_filter:
    df_cross_elasticity = df_cross_elasticity[df_cross_elasticity['price_elasticity'] >= 0]
elif 'Complementar' in product_filter and 'Substituto' not in product_filter:
    df_cross_elasticity = df_cross_elasticity[df_cross_elasticity['price_elasticity'] < 0]
else:
    df_cross_elasticity = df_cross_elasticity

#---------------------------------------------------------------------------------
# Layout
#---------------------------------------------------------------------------------
st.title('Elasticidade de Preço - Bestbuy.com')

tab1, tab2 = st.tabs(['Insights', 'DataFrame'])

with tab1:
    with st.container():
        st.header("Produtos Complementares")
        st.markdown("- Diminuindo o preço do produto em destaque aumenta a demanda pelos produtos complementares.")
        st.markdown("- Realizar Cross-Sell, oferecendo os produtos listados junto do desconto.")
        st.subheader('Produto 1: YU2 Powered Desktop Speakers (Matte Black)')
        st.markdown("""
                    1. Kanto - sub6 6 80W Powered Subwoofer - Gloss Black"
                    2. SRS-ZR7 Wireless Speaker
                    3. sub6 100W 6 Active Subwoofer (Matte Gray)
                    4. SRS-XB40 Bluetooth Speaker (Black)
                    5. Samsung - 40 Class - LED - MU7000 Series - 2160p - Smart - 4K UHD TV with HDR"
                    """)

        st.subheader('Produto 2: Sony MDR-1A Headphone - Black (International Version U.S. warranty may not apply)')
        st.markdown("""
                    1. SanDisk - Ultra 500GB Internal SATA Solid State Drive for Laptops
                    2. Sandisk Extreme CompactFlash Memory Card - 64 GB (SDCFXS-064G-A46)
                    3. Samsung - 40 Class - LED - MU7000 Series - 2160p - Smart - 4K UHD TV with HDR"
                    4. Panasonic - Lumix G85 Mirrorless Camera with 12-60mm Lens - Black
                    5. SanDisk Extreme 500 480GB USB 3.0 Portable SSD (Solid State Drive) - SDSSDEXT-480G
                    """)

        st.subheader('Produto 3: Kanto - sub6 6 80W Powered Subwoofer - Gloss Black"')
        st.markdown("""
                    1. SRS-ZR7 Wireless Speaker
                    2. sub6 100W 6 Active Subwoofer (Matte Gray)
                    3. YU2 Powered Desktop Speakers (Matte Black)
                    4. SRS-XB40 Bluetooth Speaker (Black)
                    5. Samsung - 40 Class - LED - MU7000 Series - 2160p - Smart - 4K UHD TV with HDR"
                    """)

        st.header("Produtos Substitutos")
        st.markdown("- Aumentando o preço do produto em destaque aumenta a demanda pelos produtos substitutos.")
        st.markdown("- Se necessário desovar estoque, oferecer os produtos listados junto do aumento do produto em destaque.")

        st.subheader('Produto 1: SanDisk Extreme 500 480GB USB 3.0 Portable SSD (Solid State Drive) - SDSSDEXT-480G')
        st.markdown("""
                    1. Sandisk Extreme CompactFlash Memory Card - 64 GB (SDCFXS-064G-A46)
                    2. SanDisk - Ultra 500GB Internal SATA Solid State Drive for Laptops
                    """)

        st.subheader('Produto 2: WD - Blue 500GB Internal SATA Hard Drive')
        st.markdown("""
                    1. SanDisk Ultra II 1TB SATA III SSD - 2.5-Inch 7mm Height Solid State Drive - SDSSDHII-1T00-G25
                    """)


df_cross_elasticity_csv = df_cross_elasticity.to_csv(index=False, sep=';', encoding='latin1', decimal=',')

with tab2:

    st.dataframe(df_cross_elasticity)
    st.download_button("Download CSV", df_cross_elasticity_csv, "df_cross_elasticity.csv","text/csv",key='download-csv')
#     st.dataframe(df_cross_elasticity)
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






    