import streamlit as st
import pandas as pd


def render_header():
    st.title("Project 4 - Data Merging")


def render_data_to_merge(df, credits_df):
    st.subheader("Movies for which we don't have cast or crew info")
    st.dataframe(df[~df.id.isin(credits_df.id)])

    st.subheader("Credits for which we don't have movie info")
    st.dataframe(credits_df[~credits_df.id.isin(df.id)])


def render_and_return_merged_data(df, credits_df):
    st.subheader("Merged data (just 50 to avoid runtime errors)")

    df = df.merge(credits_df, how="left", left_on="id", right_on="id")
    st.dataframe(df.head(50))

    return df


def main():
    df = pd.read_csv("movies_clean.csv", parse_dates=["release_date"])

    credits_df = pd.read_csv("credits.csv")
    credits_df.drop_duplicates(subset="id", inplace=True)

    render_header()
    render_data_to_merge(df, credits_df)

    merged_df = render_and_return_merged_data(df, credits_df)


main()
