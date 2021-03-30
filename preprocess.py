import pandas as pd
from functools import reduce
pd.set_option('display.max_columns', None)
#
# #create dataframes for all csv files
# film_role = pd.read_csv("data/film_personRole.csv")
# print(film_role)
# print(film_role.describe())
# film_role = film_role.groupby(['Role']).agg(['count'])
# print(film_role.describe())

# #Get indexes for which column anneeSortie has value less than 1894
# #indexNames = film_df[film_df['anneeSortie'].isna()].index
# # Delete these row indexes from dataFrame
# #film_df.drop(indexNames , inplace=True)
#
# film_df = pd.read_csv("donnees/film.csv")
# print(film_df.describe())
# description = film_df.describe()
# #print(description)
# #print("annee sortie: ")
# #print(film_df['anneeSortie'].isna().sum())

film_distinctions = pd.read_csv("donnees/distinctions_people.csv")
print(film_distinctions.describe())
#
# film_genre = pd.read_csv("donnees/movie_genres.csv")
# film_langue = pd.read_csv("donnees/movie_langues.csv")
# film_places = pd.read_csv("donnees/movie_places.csv")
# film_directors = pd.read_csv("donnees/movie_directors.csv")
#
# print(film_directors)
# print(film_directors.describe())
#
# # film_genre = film_genre.sort_values(by='titreOriginal')
# # print(genre_counts)
# # print(genre_counts.describe())
# # print("count of na genres: ")
# # print(film_genre['genreLabel'].isna().sum())
#
#
#
# #merging all dataframes, many films are repeated as some have many genres
# dfs = [film_genre, film_langue, film_places,film_df]
# df_final = reduce(lambda left, right: pd.merge(left, right, on='titreOriginal', how="inner"), dfs)
#
# film_data = df_final.drop(columns=["film_x", "film_y", "genre", "langue", "place", "film"])
#
# print(film_data)
#
# #describe to know the range of each column
# description = film_data.describe()
# print(description)
#
# #getting the datatype of each column
# print(film_data.dtypes)