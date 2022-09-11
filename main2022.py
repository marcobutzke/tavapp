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

st.dataframe(gs)
st.dataframe(cla_cli)
st.dataframe(reg_reg)
