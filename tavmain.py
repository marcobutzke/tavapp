import pandas as pd 
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objs as go
from plotly import tools
from plotly.offline import init_notebook_mode, plot, iplot
import plotly.express as px
from streamlit_folium import folium_static 
import folium
from folium.plugins import MarkerCluster

st.title('App - Tópicos Avançados')

@st.cache
def load_database():
    return pd.read_feather('tavbase/gs.feather'), \
        pd.read_feather('tavbase/classificacaoz_consumidor.feather'), \
        pd.read_feather('tavbase/clusterizacao_pais.feather'), \
        pd.read_feather('tavbase/regressao_mercado.feather'), \
        pd.read_feather('tavbase/regressao_regiao.feather'), \
        pd.read_feather('tavbase/knn_pais.feather'), \
        pd.read_feather('tavbase/knn_produto.feather'), \
        pd.read_feather('tavbase/knn_subcategoria.feather'), \
        pd.read_feather('tavbase/outliers_pais.feather'), \
        pd.read_feather('tavbase/probabilidade_pais.feather'), \
        pd.read_feather('tavbase/localizacao.feather')

gs, cla_con, clu_pai, reg_mer, reg_reg, \
    knn_pais, knn_pro, knn_sub, out_pai, prb_pai, coordenadas = load_database()
rg_mer = reg_mer.copy()
rg_mer['ano'] = rg_mer['ds'].dt.year
rg_reg = reg_reg.copy()
rg_reg['ano'] = rg_reg['ds'].dt.year

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
    with st.expander('Paises similares'):
        st.write(gs_con['Country'][0])
        st.dataframe(knn_pais[knn_pais['referencia'] == gs_con['Country'][0]] )
        st.write('Probabilidade:')
        st.dataframe(prb_pai[prb_pai['Country'] == gs_con['Country'][0]])
    cl1, cl2, cl3, cl4 = st.columns(4)
    cl1.metric('Score', round(cla_con_con['score'][0],4), "1")
    cl2.metric('Classe', round(cla_con_con['classe'][0],4), "1")
    cl3.metric('Rank', round(cla_con_con['rank'][0],4), "1")
    cl4.metric('Lucro', round(cla_con_con['lucro'][0],4), "1")
    cl1.metric('Valor Total Comprado', round(gs_con['Sales'].sum(),2), "1")
    cl2.metric('Valor Lucro', round(gs_con['Profit'].sum(),2), "1")
    cl3.metric('Valor Médio Comprado', round(gs_con['Sales'].mean(),2), "1")
    cl4.metric('Quantidade Comprada', round(gs_con['Quantity'].sum(),2), "1")
    clu_pai_cli = clu_pai[clu_pai['referencia'] == gs_con['Country'].values[0]]    
    st.dataframe(clu_pai_cli[
       ['referencia', 'm_entrega', 'm_lucro', 'm_vendas', 'm_qtde', \
        'f_vendas', 'f_lucro', 'r_dias']])    
    st.dataframe(clu_pai_cli[
       ['cluster', 'clm_entrega', 'clm_lucro', 'clm_vendas', 'clm_qtde', \
        'clf_vendas', 'cls_lucro', 'clr_dias']])    
    with st.expander('Pedidos:'):
        st.dataframe(gs_con[
                ['Order Date','Product Name','Quantity','Sales','Profit']
            ]
        )
    if st.checkbox('Mostrar Mapas de Localização dos Pedidos'):
        data = gs_con.merge(
            coordenadas.drop_duplicates(), 
            left_on=['City', 'Country'], 
            right_on=['cidade', 'pais'], 
            how='left'
        )
        data = data.fillna(0)
        m = folium.Map(location=[0, 0], tiles='openstreetmap', zoom_start=2)
        for id,row in data.iterrows():
            folium.Marker(location=[row['lat'],row['lng']], popup=row['Profit']).add_to(m)
        folium_static(m) 

        m2 = folium.Map(location=[0,0], tiles='cartodbpositron', zoom_start=2)
        mc = MarkerCluster()
        for idx, row in data.iterrows():
            mc.add_child(folium.Marker([row['lat'], row['lng']],popup=row['Country']))
        m2.add_child(mc)
        folium_static(m2) 

with tabbi:
    st.header('Dados do Business Intelligence')
    with st.expander('Mercado'):
        aggm = st.selectbox('Agregador Mercado, ', ['sum', 'mean'])
        st.dataframe(rg_mer.pivot_table(index='Market', columns='ano',
            values='yhat', aggfunc=aggm, fill_value=0))
        if st.checkbox('Detalhar mercado'):
            mercado = st.selectbox('Mercado', rg_mer['Market'].unique())
            gr_mer = rg_mer[rg_mer['Market'] == mercado].groupby('ano')['yhat'].sum().reset_index()
            proj = alt.Chart(gr_mer).mark_line(color='blue').encode(x='ano', y='yhat')
            gr_gs = gs[gs['Market'] == mercado].groupby('Year')['Sales'].sum().reset_index()
            real = alt.Chart(gr_gs).mark_line(color='red').encode(x='Year', y='Sales')
            st.altair_chart(proj + real)
            if st.checkbox('Mapa do mercado'):
                vendas = gs[gs['Market'] == mercado].groupby('Country')['Sales'].sum().reset_index()
                fig = px.choropleth(vendas,locations='Country',locationmode='country names',color='Sales')
                fig.update_layout(title='Vendas',template="plotly_white")  
                st.plotly_chart(fig)          
                lucros = gs[gs['Market'] == mercado].groupby('Country')['Profit'].sum().reset_index()            
                fig = px.choropleth(lucros,locations='Country',locationmode='country names',color='Profit')
                fig.update_layout(title='Vendas',template="plotly_white")  
                st.plotly_chart(fig)          
    with st.expander('Região'):
        aggr = st.selectbox('Agregador Região, ', ['sum', 'mean'])
        st.dataframe(rg_reg.pivot_table(index='Region', columns='ano',
            values='yhat', aggfunc=aggr, fill_value=0))
        if st.checkbox('Detalhar região'):
            regiao = st.selectbox('Região', rg_reg['Region'].unique())
            gr_reg = rg_reg[rg_reg['Region'] == regiao].groupby('ano')['yhat'].sum().reset_index()
            proj = alt.Chart(gr_reg).mark_line(color='blue').encode(x='ano', y='yhat')
            gr_gs = gs[gs['Region'] == regiao].groupby('Year')['Sales'].sum().reset_index()
            real = alt.Chart(gr_gs).mark_line(color='red').encode(x='Year', y='Sales')
            st.altair_chart(proj + real)
            if st.checkbox('Mapa da Região'):
                vendas = gs[gs['Region'] == regiao].groupby('Country')['Sales'].sum().reset_index()
                fig = px.choropleth(vendas,locations='Country',locationmode='country names',color='Sales')
                fig.update_layout(title='Vendas',template="plotly_white")  
                st.plotly_chart(fig)          
                lucros = gs[gs['Region'] == regiao].groupby('Country')['Profit'].sum().reset_index()            
                fig = px.choropleth(lucros,locations='Country',locationmode='country names',color='Profit')
                fig.update_layout(title='Vendas',template="plotly_white")  
                st.plotly_chart(fig)          
    with st.expander('Mapa de Vendas'):
        vendas = gs.groupby('Country')['Sales'].sum().reset_index()
        fig = px.choropleth(vendas,locations='Country',locationmode='country names',color='Sales')
        fig.update_layout(title='Vendas',template="plotly_white")  
        st.plotly_chart(fig)          
        lucros = gs.groupby('Country')['Profit'].sum().reset_index()            
        fig = px.choropleth(lucros,locations='Country',locationmode='country names',color='Profit')
        fig.update_layout(title='Lucro',template="plotly_white")  
        st.plotly_chart(fig)          
    with st.expander('RFM/Outliers'):    
        out_paises = st.multiselect('Paises:', gs_con['Country'].unique())
        st.dataframe(out_pai[out_pai['referencia'].isin(out_paises)])
with tabstore:
    st.header('Dados do Comércio Eletrônico')        
    consumidor = st.selectbox(
        'Selecione o consumidor: ',
        gs['Customer ID'].unique() 
    )
    gs_cli = gs[gs['Customer ID'] == consumidor][[
        'Product ID',
        'Product Name', 
        'Sub-Category']
    ].reset_index()
    for subcategoria in gs_cli['Sub-Category'].unique():
        st.info(subcategoria)
        st.warning('Similares')
        for idx, rw in knn_sub[knn_sub['referencia'] == subcategoria].iterrows():
            st.error(rw['vizinho'])
    for index, row in gs_cli.iterrows():
        st.info('{0}({1})'.format(row['Product Name'],row['Product ID']))
        st.write('Similares')
        for idx, rw in knn_pro[knn_pro['referencia'] == row['Product Name']].iterrows():
            st.success(rw['vizinho'])

    if st.checkbox('Não clique aqui'):
        st.balloons()        

