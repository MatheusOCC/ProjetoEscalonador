import streamlit as st
import pandas as pd

def cria_cabecalho():
    st.title('Projeto Escalonador')
    col1,col2 = st.columns(2)
    with col1:
        st.caption(
            '''
            Autores:
            \n* John Bryan Lemos
            \n* Matheus Oliver de Carvalho Cerqueira
            '''
        )
    with col2:
        st.caption(
            '''
            UNIVERSIDADE FEDERAL DA BAHIA
            \nSemestre: 2023.1
            \n MATA82 - Sistemas de Tempo Real
            '''
        )
    st.divider()


def get_conjunto_tarefas() -> list:
    conjunto_tarefas = st.text_input(
        'Escreva o Conjunto de Tarefas a ser escalonado',
        help='''
        Exemplo: (1,2);(1,4);(1,6);(2,5). 
        Parênteses e espaços são desconsiderados.
        '''
    )
    try:
        conjunto_tarefas = conjunto_tarefas.split(';')
    except:
        st.warning(
            'Por favor, adeque o conjunto de tarefas ao formato esperado.'
        )
    tarefas = []
    for tarefa in conjunto_tarefas:
        tarefas.append(
            tarefa.replace('(','').replace(')','').replace(' ','').split(',')
        )
    st.info(tarefas)
    return tarefas


def cria_dataframe_tarefas(tarefas) -> pd.DataFrame():
    if tarefas[0][0]:
        df = pd.DataFrame(tarefas, columns = [0, 1]).rename(columns={0:'Custo',1: 'Período'})
        df.insert(loc=0, column='Tarefa', value=df.index+1)
        st.write(df)
        return df


def get_utilizacao_processador(df) -> bool:
    U = 0
    for ind in df.index:
        U = U + int(df['Custo'][ind]) / int(df['Período'][ind])
    return (U <= 1)


def get_prioridade() -> str:
    prioridade = st.selectbox(
        'Escolha a prioridade',
        options=["Prioridade Fixa", "Prioridade Dinâmica"]
    )
    st.info(prioridade)
    return prioridade


def get_algoritmo(prioridade) -> str:
    if prioridade == "Prioridade Dinâmica":
        algoritmos=['EDF']
    else:
        algoritmos = ["Rate-Monotonic"]
    st.info(algoritmos)
    return st.radio("Escolha o algoritmo",options=algoritmos)


def rate_monotonic_scheduling(df) -> pd.DataFrame():
    pass


def earliest_deadline_first_scheduling(df) -> pd.DataFrame():
    pass
 

def esta_plenamente_utilizado() -> bool:
    pass
 

def cria_gráfico(df) -> None:
    pass


def main():
    cria_cabecalho()
    tarefas = get_conjunto_tarefas()
    df = cria_dataframe_tarefas(tarefas)
    if not get_utilizacao_processador(df):
        st.warning(
            '''
            O Conjunto de tarefas não é Escalonável, 
            pois a utilização do processador é maior do que 100%.
            '''
        )
    else:
        prioridade = get_prioridade()
        algoritmos = get_algoritmo(prioridade)


if __name__ == "__main__":
    main()