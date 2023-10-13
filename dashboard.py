import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
import datetime
import streamlit as st
import plotly as px

st.set_page_config(layout="wide")

yf.pdr_override()

anos_ini = [2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
ticker = ['VIIA3.SA', 'MGLU3.SA', 'CIEL3.SA']

nomes_empresas = pd.read_csv('empresas.csv')

ano_ini = st.sidebar.selectbox("Inicio", anos_ini)
ano_fim = st.sidebar.selectbox("Fim", anos_ini)
empresa = st.sidebar.selectbox("Código da empresa", nomes_empresas)

def dados_fin(empresa):
    nome = yf.Ticker(empresa)
    teste = nome.income_stmt
    teste = teste.T
    #print(teste)
    ver_ebitda = 'EBITDA'
    ver_despesa_total = 'Total Expenses'
    ver_lucro_op = 'Operating Income'
    ver_depesa_op = 'Operating Expense'
    ver_receita_op = 'Operating Revenue'

    resultado_ebitda = verifica(ver_ebitda, teste)
    resultado_despesa_total = verifica(ver_despesa_total, teste)
    resultado_lucro_op = verifica(ver_lucro_op, teste)
    resultado_depesa_op = verifica(ver_depesa_op, teste)
    resultado_receita_op = verifica(ver_receita_op, teste)

    return(resultado_ebitda, resultado_despesa_total, resultado_lucro_op, resultado_depesa_op, resultado_receita_op)

def verifica(nome_coluna, df):
    if nome_coluna in df.columns:
        df = df.iloc[0]
        valor = 'R${:,.2f}'.format(df[nome_coluna]).replace('.', 'X').replace(',', '.').replace('X', ',')
        return valor
    else:
        return f'Indisponivel'

#times = st.sidebar.selectbox("Times", brasileirao["Nome"].unique())
#dados = brasileirao[brasileirao["Nome"] == times]

start = datetime.datetime(ano_ini, 1, 1)
end = datetime.datetime(ano_fim, 12, 31)

via = pdr.data.get_data_yahoo(empresa,start,end)
via.drop(columns=['Open','High','Low','Adj Close','Volume'],inplace=True)
via.head()

st.markdown("<h1 style='text-align: center; color: white;'>"+(f'Análise da ação - {empresa}')+"</h1>",unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("<h3 style='text-align: center; color: white;'>"'Preço da ação ao longo do tempo'"</h3>",unsafe_allow_html=True)
    imagem = px.express.line(via, y="Close")
    st.plotly_chart(imagem, use_container_width=True)

with col2:
    infos = dados_fin(empresa)
    st.subheader(f'Ebitda: \n{infos[0]}')
    st.subheader(f'Lucro operacional: \n{infos[1]}')
    st.subheader(f'Depesa operacional: \n{infos[2]}')
    st.subheader(f'Receita operacional: \n{infos[3]}')
    st.subheader(f'Despesa operacional: \n{infos[4]}')

