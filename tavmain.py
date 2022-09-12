import pandas as pd 
import streamlit as st
import altair as alt

st.title('App - Tópicos Avançados')

@st.cache
def load_database():
    return pd.read_feather('tavbase/gs.feather'), \
        pd.read_feather('tavbase/classificacaoz_consumidor.feather')

gs, cla_con = load_database()

taberp, tabbi, tabstore = st.tabs(['Sistema Interno', 'Gestão', 'E-Commerce'])

with taberp:
    st.header('Dados do Sistema Interno')
    consumidor = st.selectbox(
        'Selecione o consumidor', 
        gs['Customer ID'].unique()
    )
    gs_con = gs[gs['Customer ID'] == consumidor]
    # st.dataframe(gs_con)
    cla_con_con = cla_con[cla_con['Customer ID'] == consumidor].reset_index() 
    # st.dataframe(cla_con_con)
    st.dataframe(gs_con[['Customer Name', 'Segment']].drop_duplicates())
    cl1, cl2, cl3, cl4 = st.columns(4)
    cl1.metric('Score', round(cla_con_con['score'][0],4), "1")
    cl2.metric('Classe', round(cla_con_con['classe'][0],4), "1")
    cl3.metric('Rank', round(cla_con_con['rank'][0],4), "1")
    cl4.metric('Lucro', round(cla_con_con['lucro'][0],4), "1")
    cl1.metric('Valor Total Comprado', round(gs_con['Sales'].sum(),2), "1")
    cl2.metric('Valor Lucro', round(gs_con['Profit'].sum(),2), "1")
    cl3.metric('Valor Médio Comprado', round(gs_con['Sales'].mean(),2), "1")
    cl4.metric('Quantidade Comprada', round(gs_con['Quantity'].sum(),2), "1")
    with st.expander('Pedidos:'):
        st.dataframe(gs_con[
                ['Order Date','Product Name','Quantity','Sales','Profit']
            ]
        )
with tabbi:
    st.header('Dados do Business Intelligence')
with tabstore:
    st.header('Dados do Comércio Eletrônico')        