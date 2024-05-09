import streamlit as st
import pandas as pd
import altair as alt
from utils import clean_convert_column
import numpy as np

def run():
    # init_session_state()
    st.set_page_config(
        page_title="Empenhos IFC Araquari | Empenhos Pagos", 
        page_icon="📃", 
        layout="wide", 
        initial_sidebar_state="expanded", 
        menu_items={
            'Get Help': 'https://www.extremelycoolapp.com/help',
            'Report a bug': "https://www.extremelycoolapp.com/bug",
            'About': """
                Este projeto de pesquisa tem como objetivo apresentar dados financeiros sobre o IFC Campus Araquari, no que respeita aos empenhos pagos e à liquidar..
                \\
                \\
                Professor Responsavel: [Fábio Longo de Moura](www.github.com/ldmfabio) 
                \\
                Aluno Responsavel: [Mateus Lopes Albano](www.github.com/mateus-lopes)
                \
                \

            """
        }
    )
    st.markdown(
        """
        ## 📃 Empenhos IFC Araquari | Empenhos A Liquidar
        #####
        """
    )

    df = pd.read_csv('./assets/csv/a_liquidar.csv', sep=';', decimal=',')
    colunas_visiveis = ['Natureza Despesa', 'Natureza Despesa Detalhada', 'Nome Favorecido', 'Mês', 'Saldo']
    filtered_df = df[colunas_visiveis]

    tab1, tab2 = st.tabs(["Dados", "Gráficos"])

    with tab1:
        st.write(filtered_df)

    with tab2:

        tab3, tab4, tab5 = st.tabs(
            [
                "Por Mês",
                "Por Natureza de Despesa",
                "Por Mês e Natureza de Despesa",
            ]
        )

        with tab3:
            clean_df = clean_convert_column(filtered_df.copy(), 'Saldo')
            df_grouped = clean_df.groupby("Mês").sum().reset_index()
            # st.write(df_grouped)

            chart = (
                alt.Chart(df_grouped)
                .mark_bar()
                .encode(x="Mês", y="Saldo", color="Mês")
                .properties(width=800, height=400)
            )
            st.altair_chart(chart, use_container_width=True)

        with tab4:
            grouped_df = clean_df.groupby(['Natureza Despesa', 'Mês'])

            # Calcular a soma do "Saldo" para cada grupo
            aggregated_df = grouped_df['Saldo'].sum().reset_index()

            # Combinar as informações em um único DataFrame
            combined_df = pd.merge(clean_df, aggregated_df, on=['Natureza Despesa', 'Mês'])

            # Renomear e descartar colunas desnecessárias
            combined_df.rename(columns={'Saldo_y': 'Saldo'}, inplace=True)
            combined_df.drop(['Saldo_x'], axis=1, inplace=True)

            df_para_grafico = combined_df.groupby(['Natureza Despesa', 'Mês']).sum().reset_index()

            # st.write(df_para_grafico)
            chart1 = alt.Chart(df_para_grafico).mark_bar().encode(
                x=alt.X('Mês', axis=alt.Axis(title='Mês')),
                y=alt.Y('Saldo', axis=alt.Axis(title='Saldo')),
                color='Natureza Despesa',
                tooltip=['Mês', 'Natureza Despesa', alt.Tooltip('Saldo', title='Saldo')]
            ).properties(
                width=800,
                height=400
            )
            st.altair_chart(chart1, use_container_width=True)

        with tab5:
            def filtrar_dados(filtered_df, mes, naturezas_selecionadas):
                if mes == 'Todos' and naturezas_selecionadas == ['Todas']:
                    return filtered_df
                elif naturezas_selecionadas != ['Todas']:
                    return filtered_df[filtered_df['Natureza Despesa'].isin(naturezas_selecionadas)]
                elif mes != 'Todos':
                    return filtered_df[filtered_df['Mês'] == mes]
                else:
                    return filtered_df[(filtered_df['Mês'] == mes) & (filtered_df['Natureza Despesa'].isin(naturezas_selecionadas))]

            meses_unicos = ['Todos'] + filtered_df['Mês'].unique().tolist()
            naturezas_unicas = filtered_df['Natureza Despesa'].unique().tolist()

            mes_selecionado = st.selectbox('Selecione o mês', meses_unicos)
            naturezas_unicas = ['Todas'] + filtered_df['Natureza Despesa'].unique().tolist()
            naturezas_selecionadas = st.multiselect('Selecione a natureza de despesa', naturezas_unicas, 'Todas')
            
            df_filtrado = filtrar_dados(filtered_df, mes_selecionado, naturezas_selecionadas)

            clean_df = clean_convert_column(df_filtrado.copy(), 'Saldo')
            df_grouped = clean_df.groupby(['Natureza Despesa', 'Mês']).sum().reset_index()

            chart2 = alt.Chart(df_grouped).mark_bar().encode(
                x='Mês',
                y='Saldo',
                color='Natureza Despesa',
                tooltip=['Mês', 'Natureza Despesa', alt.Tooltip('Saldo', title='Saldo')]
            ).properties(
                width=800,
                height=400
            ).interactive()

            st.altair_chart(chart2, use_container_width=True)


if __name__ == "__main__":
    run()