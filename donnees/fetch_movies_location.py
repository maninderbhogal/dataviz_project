"""Script qui extrait tous les films avec leurs lieux de production.
"""

import csv
import multiprocessing
from SPARQLWrapper import SPARQLWrapper, JSON, CSV

CQ_SPARQL_ENDPOINT = "http://data.cinematheque.qc.ca/sparql"
WIKIDATA_SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"

def fetch_movie_places():
    sparql = SPARQLWrapper(CQ_SPARQL_ENDPOINT)

    query = """
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX frbroo: <http://iflastandards.info/ns/fr/frbr/frbroo/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT DISTINCT ?film ?filmLabel ?placeWikidata ?placeLabel WHERE {
  ?film a frbroo:F1_Work .
  ?film rdfs:label ?filmLabel .
  ?recordingWork frbroo:R2_is_derivative_of ?film .
  ?recordingEvent frbroo:R22_created_a_realization_of ?recordingWork .
  ?recordingEvent crm:P7_took_place_at ?place .
  ?place owl:sameAs ?placeWikidata .
  ?place rdfs:label ?placeLabel .
}
"""
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()['results']['bindings']

    dict_data = [{ 'film': r['film']['value'],
                   'filmLabel': r['filmLabel']['value'],
                   'place': r['placeWikidata']['value'],
                   'placeLabel': r['placeLabel']['value']
                 } for r in results]

    return dict_data

def main():
    movies_places = fetch_movie_places()

    with open('movie_places.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['film', 'filmLabel', 'place', 'placeLabel'])
        writer.writeheader()
        for m in movies_places:
            writer.writerow(m)

if __name__ == '__main__':
    main()
