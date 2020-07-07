import streamlit as st
import pandas as pd
import requests

api_key = "api_key=a30d5ffe068c4cb0aecfc349d42fd161"


def get_movies(page_number):
    query = f"&primary_release_date.gte=2020-01-01&primary_release_date.lte=2020-02-29&page={page_number}"
    url = "https://api.themoviedb.org/3/discover/movie?" + api_key + query
    return requests.get(url).json()


def get_movie(movie_id):
    query = f"https://api.themoviedb.org/3/movie/{movie_id}?{api_key}"
    return requests.get(query).json()


def main():
    st.title("Project 2 - Data Import")
    data = get_movies(1)

    page_num = st.sidebar.selectbox(
        "Change page", tuple(i + 1 for i in range(data["total_pages"]))
    )
    data = get_movies(page_num)

    df = pd.DataFrame(data["results"])
    df.set_index("id", inplace=True)
    st.dataframe(df)

    movie_name = st.sidebar.selectbox("Change movie", tuple(df["title"].values))

    st.subheader(movie_name)
    movie_data = get_movie(df[df["title"] == movie_name].index.values.astype(int)[0])
    normalized_data = pd.json_normalize(movie_data, sep="_").T
    st.table(normalized_data)

    if st.button("Download movie data"):
        movie_data.to_json(f"{movie_name}.json", orient="records")


main()
