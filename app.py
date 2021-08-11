import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from time import sleep

@st.cache
def carrega_dados(caminho):
    dados = pd.read_csv(caminho)
    sleep(3)
    return dados


def grafico_comparativo(dados_2019, dados_2020, causa, estado = 'BRASIL'):

    if estado == 'BRASIL':
        total_2019 = dados_2019.groupby('tipo_doenca').sum()
        total_2020 = dados_2020.groupby('tipo_doenca').sum()
        lista = [int(total_2019.loc[causa]), int(total_2020.loc[causa])]

    else:
        total_2019 = dados_2019.groupby(['uf', 'tipo_doenca']).sum()
        total_2020 = dados_2020.groupby(['uf', 'tipo_doenca']).sum()
        lista = [int(total_2019.loc[estado, causa]), int(total_2020.loc[estado, causa])]

    dados = pd.DataFrame({'Total': lista, 'Ano': [2019, 2020]})

    fig, ax = plt.subplots()
    ax = sns.barplot(x = 'Ano', y = 'Total', data = dados)
    ax.set_title(f'Óbitos por {causa} - {estado}')

    return fig


obitos_2019 = carrega_dados('dados/obitos-2019.csv')
obitos_2020 = carrega_dados('dados/obitos-2020.csv')
estados = np.append(obitos_2019.uf.unique(), 'BRASIL')
doencas = obitos_2019.tipo_doenca.unique()

st.title('Análise de óbitos')
st.dataframe(obitos_2019)
st.markdown('Este trabalho analisa dados dos óbitos por doenças respiratórias* nos anos de 2019 e 2020')

opcao_1 = st.sidebar.selectbox('Selecione a doença', options = doencas)
opcao_2 = st.sidebar.selectbox('Selecione o estado', options = estados)

figura = grafico_comparativo(obitos_2019, obitos_2020, 
                                opcao_1, opcao_2)
st.pyplot(figura)


