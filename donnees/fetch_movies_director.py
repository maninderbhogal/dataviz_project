"""Script qui extrait tous les films avec les directeurs.
"""

import csv
import multiprocessing
from SPARQLWrapper import SPARQLWrapper, JSON, CSV

CQ_SPARQL_ENDPOINT = "http://data.cinematheque.qc.ca/sparql"
WIKIDATA_SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"

def fetch_movie_directors():
    sparql = SPARQLWrapper(CQ_SPARQL_ENDPOINT)

    query = """
BASE <http://data.cinematheque.qc.ca>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX frbroo: <http://iflastandards.info/ns/fr/frbr/frbroo/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT DISTINCT ?personWikidata ?personLabel ?film ?titreOriginal WHERE {
  ?film rdf:type frbroo:F1_Work .
  ?film rdfs:label ?titreOriginal .
  ?recordingWork frbroo:R2_is_derivative_of ?film .
  ?recordingEvent frbroo:R22_created_a_realization_of ?recordingWork .
  ?recordingEvent crm:P9_consists_of ?recordingActivity .
  ?recordingActivityC crm:P01_has_domain ?recordingActivity .
  ?recordingActivityC crm:P02_has_range ?person .
  ?recordingActivityC crm:P14.1_in_the_role_of </resource/Role1> .
  ?person owl:sameAs ?personWikidata .
  ?person rdfs:label ?personLabel .
}
"""
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()['results']['bindings']

    dict_data = [{'film': r['film']['value'],
                 'titreOriginal': r['titreOriginal']['value'],
                  'person': r['personWikidata']['value'],
                  'personLabel': r['personLabel']['value']
                 } for r in results]

    return dict_data

def fetch_wikidata_directors():
    sparql = SPARQLWrapper(WIKIDATA_SPARQL_ENDPOINT)

    query = """
SELECT DISTINCT ?person
WHERE
{
  ?person wdt:P106 wd:Q2526255 .
  # SERVICE wikibase:label { bd:serviceParam wikibase:language "fr". }

}
"""

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()['results']['bindings']

    persons = []
    for r in results:
        persons.append(r['person']['value'])

    return persons

def main():
    movies_directors = fetch_movie_directors()
    wd_directors = fetch_wikidata_directors()
    filtered_movies_directors = filter(lambda m: m['person'] in wd_directors, movies_directors)

    with open('movie_directors.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['film', 'titreOriginal', 'person', 'personLabel'])
        writer.writeheader()
        for m in filtered_movies_directors:
            writer.writerow(m)

if __name__ == '__main__':
    main()
