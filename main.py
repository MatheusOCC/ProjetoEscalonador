import streamlit as st


def main():
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


if __name__ == "__main__":
    main()