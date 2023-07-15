import streamlit as st
import pandas as pd
import numpy as np
import module 

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
    # st.info(tarefas)
    return tarefas


def cria_dataframe_tarefas(tarefas) -> pd.DataFrame():
    df = pd.DataFrame(tarefas, columns = [0, 1]).rename(columns={0:'Custo',1: 'Período'})
    df.insert(loc=0, column='Tarefa', value=df.index+1)
    st.write(df)
    return df


def get_utilizacao_processador(df) -> bool:
    U = 0
    for ind in df.index:
        U = U + int(df['Custo'][ind]) / int(df['Período'][ind])
    return U


def get_prioridade() -> str:
    prioridade = st.selectbox(
        'Escolha a prioridade',
        options=["Prioridade Fixa", "Prioridade Dinâmica"]
    )
    # st.info(prioridade)
    return prioridade


def get_algoritmo(prioridade) -> str:
    if prioridade == "Prioridade Dinâmica":
        algoritmos=['EDF']
    else:
        algoritmos = ["Rate-Monotonic"]
    # st.info(algoritmos)
    return st.radio("Escolha o algoritmo",options=algoritmos)


def rate_monotonic_scheduling(df) -> pd.DataFrame:
    df = df.sort_values(by='Período')
    df['Prioridade'] = df.index + 1

    tempo_inicial = 0
    df['Início'] = 0
    df['Término'] = 0

    for i, row in df.iterrows():
        tempo_inicial = max(tempo_inicial, int(row['Período']))
        df.at[i, 'Início'] = tempo_inicial
        df.at[i, 'Término'] = tempo_inicial + int(row['Custo'])
        tempo_inicial = df.at[i, 'Término']

    st.write(df)
    return df


def earliest_deadline_first_scheduling(df) -> pd.DataFrame:
    df = df.sort_values(by='Período')
    df['Deadline'] = df['Período']

    tempo_inicial = 0
    df['Início'] = 0
    df['Término'] = 0

    for i, row in df.iterrows():
        tempo_inicial = max(tempo_inicial, int(row['Período']))
        df.at[i, 'Início'] = tempo_inicial
        df.at[i, 'Término'] = tempo_inicial + int(row['Custo'])
        tempo_inicial = df.at[i, 'Término']

    st.write(df)
    return df
 

def esta_plenamente_utilizado() -> bool:
    pass
 

def cria_gráfico(df) -> None:
    pass


def main():
    st.write('21:15')
    cria_cabecalho()
    tarefas = get_conjunto_tarefas()
    if tarefas[0][0]:
        df = cria_dataframe_tarefas(tarefas)
        u = get_utilizacao_processador(df)
        if not u < 1:
            st.warning(
                '''
                O Conjunto de tarefas não é Escalonável, 
                pois a utilização do processador é maior do que 100%.
                '''
            )
        else:
            st.success("Utilização: "+str(np.round(u,3)))
            prioridade = get_prioridade()
            algoritmos = get_algoritmo(prioridade)
            rate_monotonic_scheduling(df) if algoritmos == "Prioridade Fixa" else earliest_deadline_first_scheduling(df)
            return 1


if __name__ == "__main__":
    main()