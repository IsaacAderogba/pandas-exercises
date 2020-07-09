from io import StringIO
import streamlit as st
import pandas as pd
import numpy as np


def render_header():
    st.title("Project 3 - Data Cleaning")
    st.subheader("Tidying up messy datasets")


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
    st.text(info)
    st.table(datatypes)

    st.subheader("Summary statistics")
    st.table(content.describe(include="all").T)
    return info, datatypes


def main():
    # setup
    df = pd.read_csv("movies_metadata.csv", low_memory=False)

    # render header and overview info
    render_header()
    if st.sidebar.checkbox("View summary information"):
        render_summary_info(df)


main()
