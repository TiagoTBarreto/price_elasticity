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
df_cross_elasticity = pd.read_csv('/home/tiagobarreto/DS/repos/elasticidade_preco/data/treated/cross_elasticity.csv')
df_cross_elasticity = df_cross_elasticity.drop(columns = ['Unnamed: 0'])


#----------------------------------------------------------------------------------
# Sidebar
#---------------------------------------------------------------------------------
with st.sidebar:
    # carregando imagem
    st.image('/home/tiagobarreto/DS/repos/elasticidade_preco/streamlit/images/bestbuy.png')

    # criando título
    st.title('Bestbuy')  

    # criando filtro por tipo do produto
    product_type = ['Substituto', 'Complementar']
    product_filter = st.multiselect("Selecione o Tipo do Produto", options=product_type, default=product_type)  

# ---------------------------------------------- filtragem ----------------------------------------------

# filtrando por tipo do produto
if 'Substituto' in product_filter and 'Complementar' not in product_filter:
    df_cross_elasticity = df_cross_elasticity[df_cross_elasticity['price_elasticity'] >= 0]
elif 'Complementar' in product_filter and 'Substituto' not in product_filter:
    df_cross_elasticity = df_cross_elasticity[df_cross_elasticity['price_elasticity'] < 0]
else:
    df_cross_elasticity = df_cross_elasticity
# ------------------------------------------- renomeando colunas ----------------------------------------
df_cross_elasticity.columns = ['Produto A (Preço)', 'Produto B (Demanda)', 'Elasticidade']

# ------------------------------------------- feature engineering ----------------------------------------
df_cross_elasticity['Tipo do Produto'] = df_cross_elasticity.apply(lambda x: 'Complementar' if x['Elasticidade'] < 0 else 'Substituto', axis = 1)  


# salvando dataframe como csv
df_cross_elasticity_csv = df_cross_elasticity.to_csv(index=False, sep=';', encoding='latin1', decimal=',')


#---------------------------------------------------------------------------------
# Layout
#---------------------------------------------------------------------------------
st.title('Elasticidade de Preço - Bestbuy.com')

tab1, tab2 = st.tabs(['Insights', 'DataFrame'])


with tab1:
    with st.container():
        # produtos complementares
        st.header("Produtos Complementares")

        # explicacao
        st.markdown("- Diminuindo o preço do produto em destaque aumenta a demanda pelos produtos complementares.")
        st.markdown("- Realizar Cross-Sell, oferecendo os produtos listados junto do desconto.")

        # produto 1
        st.subheader('Produto 1: YU2 Powered Desktop Speakers (Matte Black)')
        # recomendações complementares
        st.markdown("""
                    1. Kanto - sub6 6 80W Powered Subwoofer - Gloss Black"
                    2. SRS-ZR7 Wireless Speaker
                    3. sub6 100W 6 Active Subwoofer (Matte Gray)
                    4. SRS-XB40 Bluetooth Speaker (Black)
                    5. Samsung - 40 Class - LED - MU7000 Series - 2160p - Smart - 4K UHD TV with HDR"
                    """)

        # produto 2
        st.subheader('Produto 2: Sony MDR-1A Headphone - Black (International Version U.S. warranty may not apply)')
        # recomendações complementares
        st.markdown("""
                    1. SanDisk - Ultra 500GB Internal SATA Solid State Drive for Laptops
                    2. Sandisk Extreme CompactFlash Memory Card - 64 GB (SDCFXS-064G-A46)
                    3. Samsung - 40 Class - LED - MU7000 Series - 2160p - Smart - 4K UHD TV with HDR"
                    4. Panasonic - Lumix G85 Mirrorless Camera with 12-60mm Lens - Black
                    5. SanDisk Extreme 500 480GB USB 3.0 Portable SSD (Solid State Drive) - SDSSDEXT-480G
                    """)

        # produto 3
        st.subheader('Produto 3: Kanto - sub6 6 80W Powered Subwoofer - Gloss Black"')

        # recomendações complementares
        st.markdown("""
                    1. SRS-ZR7 Wireless Speaker
                    2. sub6 100W 6 Active Subwoofer (Matte Gray)
                    3. YU2 Powered Desktop Speakers (Matte Black)
                    4. SRS-XB40 Bluetooth Speaker (Black)
                    5. Samsung - 40 Class - LED - MU7000 Series - 2160p - Smart - 4K UHD TV with HDR"
                    """)

        # produtos substitutos
        st.header("Produtos Substitutos")

        # explicacao
        st.markdown("- Aumentando o preço do produto em destaque aumenta a demanda pelos produtos substitutos.")
        st.markdown("- Se necessário desovar estoque, oferecer os produtos listados junto do aumento do produto em destaque.")

        # produto 1
        st.subheader('Produto 1: SanDisk Extreme 500 480GB USB 3.0 Portable SSD (Solid State Drive) - SDSSDEXT-480G')

        # substitutos
        st.markdown("""
                    1. Sandisk Extreme CompactFlash Memory Card - 64 GB (SDCFXS-064G-A46)
                    2. SanDisk - Ultra 500GB Internal SATA Solid State Drive for Laptops
                    """)

        # produto 2
        st.subheader('Produto 2: WD - Blue 500GB Internal SATA Hard Drive')

        # substitutos
        st.markdown("""
                    1. SanDisk Ultra II 1TB SATA III SSD - 2.5-Inch 7mm Height Solid State Drive - SDSSDHII-1T00-G25
                    """)


with tab2:
    # titulo
    st.header("Explicação Produto Complementar e Substituto")

    # explicacao
    st.markdown("""
                **Complementar:** São os produtos que tem Elasticidade Negativa: Então uma diminuição no preço do produto A aumenta a demanda pelo produto B.
                - Exemplo: Elasticidade = 2 -> Uma diminuição de 2% no preço do produto A aumenta a demanda em 4% do produto B.\n
                **Substituto:** São os produtos que tem Elasticidade Positiva: Então um aumento no preço do produto A aumenta a demanda pelo produto B.
                - Exemplo: Elasticidade = 5 -> Um aumento de 2% no preço do Produto A aumenta a demanda em 10% do produto B.
                """)

    # plotando dataframe
    st.dataframe(df_cross_elasticity)

    # adicionando botao de download dos dados
    st.download_button("Download CSV", df_cross_elasticity_csv, "df_cross_elasticity.csv","text/csv",key='download-csv')



    