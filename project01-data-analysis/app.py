import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import HTML


def main():
    st.title("Project 1 - Data Analysis")

    df = pd.read_csv("movies_complete.csv", parse_dates=["release_date"])
    df["Franchise"] = df.belongs_to_collection.notna()

    def best_worst(
        by, n=5, ascending=False, min_budget=0, min_votes=0, custom_column=False
    ):
        df2 = df.copy()

        if custom_column:
            df2[by] = custom_column(df2)

        df2 = (
            df2.loc[
                (df["budget_musd"] >= min_budget) & (df["vote_count"] >= min_votes),
                ["title", "poster_path", by],
            ]
            .sort_values(by, ascending=ascending)
            .head(5)
        )

        df2.set_index("title", inplace=True)
        return df2.to_html(escape=False)

    if st.sidebar.checkbox("View column data"):
        st.write(
            """
      * **id:** The ID of the movie (clear/unique identifier).
  * **title:** The Official Title of the movie.
  * **tagline:** The tagline of the movie.
  * **release_date:** Theatrical Release Date of the movie.
  * **genres:** Genres associated with the movie.
  * **belongs_to_collection:** Gives information on the movie series/franchise the particular film belongs to.
  * **original_language:** The language in which the movie was originally shot in.
  * **budget_musd:** The budget of the movie in million dollars.
  * **revenue_musd:** The total revenue of the movie in million dollars.
  * **production_companies:** Production companies involved with the making of the movie.
  * **production_countries:** Countries where the movie was shot/produced in.
  * **vote_count:** The number of votes by users, as counted by TMDB.
  * **vote_average:** The average rating of the movie.
  * **popularity:** The Popularity Score assigned by TMDB.
  * **runtime:** The runtime of the movie in minutes.
  * **overview:** A brief blurb of the movie.
  * **spoken_languages:** Spoken languages in the film.
  * **poster_path:** The URL of the poster image.
  * **cast:** (Main) Actors appearing in the movie.
  * **cast_size:** number of Actors appearing in the movie.
  * **director:** Director of the movie.
  * **crew_size:** Size of the film crew (incl. director, excl. actors).
      """
        )
    # st.dataframe(df)

    best_worst_value = st.sidebar.selectbox(
        "Select Best/Worst Column",
        ("budget_musd", "revenue_musd", "vote_count", "vote_average", "popularity"),
    )
    radio = st.sidebar.radio("Select Best or Worst", ("Best", "Worst"))

    if radio == "Best":
        st.subheader(f"Best ({best_worst_value})")
        st.markdown(best_worst(best_worst_value), unsafe_allow_html=True)
    else:
        st.subheader(f"Worst ({best_worst_value})")
        st.markdown(
            best_worst(best_worst_value, ascending=True), unsafe_allow_html=True
        )

    franchise_counts = df["Franchise"].value_counts()
    avg_revenue = df.groupby("Franchise").revenue_musd.mean()

    df["ROI"] = df.revenue_musd.div(df.budget_musd)
    roi = df.groupby("Franchise").ROI.median()

    franchise_df = pd.DataFrame(
        {"counts": franchise_counts, "avg_revenue": avg_revenue, "roi": roi}
    )
    franchise_df.rename(index={False: "Not a Franchise", True: "Is a Franchise"}, inplace=True)

    st.text("")
    st.subheader("Are Franchises more successful?")
    st.text("")
    st.dataframe(franchise_df)


main()
