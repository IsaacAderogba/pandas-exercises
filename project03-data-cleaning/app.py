from io import StringIO
import streamlit as st
import pandas as pd
import numpy as np


def render_header():
    st.title("Project 3 - Data Cleaning")


def render_summary_info(content: pd.DataFrame):
    content_info = StringIO()
    content.info(buf=content_info)
    str_ = content_info.getvalue()

    lines = str_.split("\n")
    table = StringIO("\n".join(lines[3:-3]))
    datatypes = pd.read_table(
        table, delim_whitespace=True, names=["column", "count", "null", "dtype"]
    )
    datatypes.set_index("column", inplace=True)

    info = "\n".join(lines[0:2] + lines[-2:-1])
    st.subheader("Dataframe info")
    st.table(datatypes)

    if st.sidebar.checkbox("View summary statistics"):
        st.subheader("Summary statistics")
        st.table(content.describe(include="all").T)

    return info, datatypes

def clean_data(df: pd.DataFrame):
    column_names = list(df.columns)
    column_name = st.sidebar.selectbox("Inspect column", column_names)

    st.subheader(f"{column_name} value counts")
    st.table(df[column_name].value_counts())

    columns_to_remove = st.sidebar.multiselect("Drop columns", column_names)
    return df.drop(columns=columns_to_remove)


def main():
    # setup
    df = pd.read_csv("movies_metadata.csv", low_memory=False)

    # render header
    render_header()

    # interactive data cleaning
    clean_df = clean_data(df)

    # render cleaned information
    render_summary_info(clean_df)

main()
