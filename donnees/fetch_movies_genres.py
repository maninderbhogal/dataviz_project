"""Script qui extrait tous les films avec leurs genres cinématographiques et
leur année de sortie.

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
SELECT DISTINCT ?film ?genreWikidata ?releaseDate WHERE {
  ?film a frbroo:F1_Work .

  {
    ?film crm:P2_has_type ?genre .
    ?genre owl:sameAs ?genreWikidata .
  } UNION {
    ?film owl:sameAs ?filmWikidata .
    SERVICE <https://query.wikidata.org/sparql> {
      ?filmWikidata wdt:P136 ?genreWikidata .
    }
  }
}
"""
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()['results']['bindings']

    dict_data = [{ 'film': r['film']['value'], 'genreWikidata': r['genreWikidata']['value'] } for r in results]
    with open('movie_genres.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['film', 'genreWikidata'])
        writer.writeheader()
        for data in dict_data:
            writer.writerow(data)

def main():
    fetch_movie_genres()

if __name__ == '__main__':
    main()


