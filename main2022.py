import pandas as pd

import streamlit as st
import altair as alt

st.title('Projeto da Disciplina de Tópicos Avançados')

@st.cache
def load_databases():
    return pd.read_feather('base2022/gs.feather'), \
    pd.read_feather('base2022/classificaoz_consumidor.feather'), \
    pd.read_feather('base2022/clustericacao_pais.feather'), \
    pd.read_feather('base2022/knn_pais.feather'), \
    pd.read_feather('base2022/knn_produto.feather'), \
    pd.read_feather('base2022/knn_subcategoria.feather'), \
    pd.read_feather('base2022/probabilidade_pais.feather'), \
    pd.read_feather('base2022/regressao_mercado.feather'), \
    pd.read_feather('base2022/regressao_regiao.feather')

gs, cla_cli, clu_pai, knn_pai, knn_pro, knn_sub, prb_pai, reg_mer, reg_reg = load_databases()

taberp, tabbi, tabestore = st.tabs(["ERP", "BI", "eStore"])

with taberp:
    st.header('Dados para ERP')
    consumidor = st.selectbox(
        'Selecione o consumidor: ',
        gs['Customer ID'].unique() 
    )
    gs_cli = gs[gs['Customer ID'] == consumidor].reset_index()
    cla_con = gs_cli[gs_cli['Customer ID'] == consumidor].reset_index()
    cli_con = cla_cli[cla_cli['Customer ID'] == consumidor].reset_index()
    prb_con = prb_pai[prb_pai['Country'] == cla_con['Country'][0]].reset_index()
    clu_con = clu_pai[clu_pai['referencia'] == cla_con['Country'][0]].reset_index()
    gs_cli_pais_nome = gs_cli['Country'][0]
    knn_con = knn_pai[knn_pai['referencia'] == gs_cli_pais_nome].reset_index()
    st.dataframe(gs_cli[['Customer ID','Customer Name','Segment']].drop_duplicates())
    cl1, cl2, cl3, cl4, cl5, cl6 = st.columns(6)
    cl1.metric('Score', round(cli_con['score'][0],4), "1")
    cl2.metric('Classe', int(cli_con['classe'][0]), "1")
    cl3.metric('Rank', int(cli_con['rank'][0]), "1")
    cl4.metric('Lucro', int(cli_con['Profit'][0]), "1")
    cl5.metric('Probabilidade de Lucro', round(prb_con['lucro_1'][0],4), "1")
    cl6.metric('Cluster', int(clu_con['cluster'][0]), "1")
    with st.expander('Pedidos'): 
        st.dataframe(gs_cli[['Order ID','Order Date','Product Name','Sub-Category','Category','Quantity','Sales','Profit']])               
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric('Lucro Total', round(gs_cli['Profit'].sum(),2), "1")
    col2.metric('Vendas Total', round(gs_cli['Profit'].sum(),2), "1")
    col3.metric('Média Lucro', round(gs_cli['Profit'].mean(),2), "1")
    col4.metric('Média Itens', round(gs_cli['Profit'].mean(),2), "1")
    col5.metric('Quantidade', int(gs_cli['Profit'].count()), "1")
    col6.metric('Média Desconto', round(gs_cli['Discount'].mean(),2), "1")
    with st.expander('dados de mercado'):
        st.dataframe(gs_cli[['City','State','Country','Region','Market']].drop_duplicates())
        st.dataframe(cli_con[['zProfit','zSales','zQuantity']])
with tabbi:
    st.header('Dados para BI')
with tabestore:
    st.header('Dados para E-commerce') 

