"""Script qui extrait tous les films avec leurs genres cinématographiques.

Le genre cinématographique extrait correspond à une entité Wikidata. Dans ce script,
on combine les données de la CQ et ceux de Wikidata.
"""

import csv
import multiprocessing
from SPARQLWrapper import SPARQLWrapper, JSON, CSV

CQ_SPARQL_ENDPOINT = "http://data.cinematheque.qc.ca/sparql"
WIKIDATA_SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"

def fetch_movie_genres():
    sparql = SPARQLWrapper(CQ_SPARQL_ENDPOINT)

    query = """
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX frbroo: <http://iflastandards.info/ns/fr/frbr/frbroo/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT DISTINCT ?film ?titreOriginal ?genreWikidata ?genreLabel WHERE {
  ?film a frbroo:F1_Work .
  ?film rdfs:label ?titreOriginal .
  ?film crm:P2_has_type ?genre .
  ?genre owl:sameAs ?genreWikidata .
  ?genre rdfs:label ?genreLabel .
}
"""
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()['results']['bindings']

    dict_data = [{ 'film': r['film']['value'],
                   'titreOriginal': r['titreOriginal']['value'],
                   'genre': r['genreWikidata']['value'],
                   'genreLabel': r['genreLabel']['value']
                 } for r in results]

    return dict_data

def fetch_wikidata_genres():
    sparql = SPARQLWrapper(WIKIDATA_SPARQL_ENDPOINT)

    query = """
SELECT DISTINCT ?genre
WHERE
{
  ?genre wdt:P31/wdt:279* wd:Q201658 .
  # SERVICE wikibase:label { bd:serviceParam wikibase:language "fr". }
}
"""

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()['results']['bindings']

    genres = []
    for r in results:
        genres.append(r['genre']['value'])

    return genres

def main():
    movies_genres = fetch_movie_genres()
    wd_genres = fetch_wikidata_genres()
    filtered_movies_genres = filter(lambda m: m['genre'] in wd_genres, movies_genres)

    with open('movie_genres.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['film', 'titreOriginal', 'genre', 'genreLabel'])
        writer.writeheader()
        for m in filtered_movies_genres:
            writer.writerow(m)

if __name__ == '__main__':
    main()
