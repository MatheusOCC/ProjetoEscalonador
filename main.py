import streamlit as st


def cria_cabecalho():
    st.title('Projeto Escalonador')
    col1,col2 = st.columns(2)
    with col1:
        st.caption(
            '''
            Autores:
            \n* John Bryan
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


def main():
    cria_cabecalho()
    tarefas = get_conjunto_tarefas()


if __name__ == "__main__":
    main()