import pandas as pd
import altair as alt
import streamlit as st
import random

def clean_convert_column(df, column_name):
    # Replace thousand separators with decimals (assuming '.' is decimal separator)
    df[column_name] = df[column_name].str.replace(',', '.')

    # Handle potential decimal separators other than '.' (e.g., ',')
    df[column_name] = df[column_name].str.replace(r"[^\d\-+\.]", "", regex=True)

    # Try converting to float, replacing errors with NaN (or a specified value)
    df[column_name] = pd.to_numeric(df[column_name], errors='coerce')

    return df

def create_simple_chart():
    df = pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [10, 20, 30, 40, 50]
    })

    chart = (
        alt.Chart(df)
        .mark_line(point=True)
        .encode(x='x', y='y')
    )

    return chart

def get_campus_option():
    id = random.randint(1, 1000)
    campus_option = st.selectbox(
        f"Selecione o Campus {id}",
        ["Araquari", "Camboriú", "Sombrio", "Videira"],
    )

    return campus_option

def create_card_chart(title='Titulo do Grafico', desciption='pequena descrição sobre o grafico', border=False):
    container_col = st.container(border=border)
    container_col.write(f"### {title}")
    container_col.caption(f"{desciption}")
    layout_cols = st.columns((1, 1, 2))

    with layout_cols[0]:
        option1 = get_campus_option()

    with layout_cols[1]:
        option2 = get_campus_option()

    st.altair_chart(create_simple_chart(), use_container_width=True)