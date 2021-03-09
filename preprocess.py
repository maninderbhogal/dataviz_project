import pandas as pd
from functools import reduce
pd.set_option('display.max_columns', None)

#create dataframes for all csv files
film_df = pd.read_csv("donnees/film.csv")

print(film_df)
description = film_df.describe()
print(description)

film_genre = pd.read_csv("donnees/movie_genres.csv")
film_langue = pd.read_csv("donnees/movie_langues.csv")
film_places = pd.read_csv("donnees/movie_places.csv")

film_genre = film_genre.sort_values(by='titreOriginal')
genre_counts = film_genre.groupby(['genreLabel']).agg(['count'])
print(genre_counts.describe())


#merging all dataframes, many films are repeated as some have many genres
dfs = [film_genre, film_langue, film_places,film_df]
df_final = reduce(lambda left, right: pd.merge(left, right, on='titreOriginal', how="inner"), dfs)

film_data = df_final.drop(columns=["film_x", "film_y", "genre", "langue", "place", "film"])

print(film_data)

#describe to know the range of each column
description = film_data.describe()
print(description)

#getting the datatype of each column
print(film_data.dtypes)