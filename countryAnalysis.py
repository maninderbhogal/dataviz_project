import plotly.express as px
import pandas as pd


film_country = pd.read_csv("data/film_pays.csv")


#film_country_grouped = film_country.groupby(['pays'])['filmoId'].agg(MoviesCount="count")


film_country['count'] = film_country.groupby('pays')['pays'].transform('count')

print(film_country)

fig = px.scatter(film_country, color="pays",size="count")
fig.show()
