import streamlit as st
import pandas as pd
import requests

api_key = "api_key=a30d5ffe068c4cb0aecfc349d42fd161"


def get_movies(page_number):
    query = f"&primary_release_date.gte=2020-01-01&primary_release_date.lte=2020-02-29&page={page_number}"
    url = "https://api.themoviedb.org/3/discover/movie?" + api_key + query
    return requests.get(url).json()


def main():
    st.title("Project 2 - Data Import")
    data = get_movies(1)

    st.selectbox("Change page", tuple(i + 1 for i in range(data["total_pages"])))



main()
