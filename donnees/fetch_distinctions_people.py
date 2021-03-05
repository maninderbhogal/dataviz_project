"""Script qui extrait les distinctions (avec la date) obtenues par les
personnes qui ont occupé une fonction dans une oeuvre réalisée au Québec.

Malheureusement, on ne connaît pas dans quelle oeuvre est associée la distinction.
"""

import csv
import multiprocessing
from SPARQLWrapper import SPARQLWrapper, JSON, CSV

CQ_SPARQL_ENDPOINT = "http://data.cinematheque.qc.ca/sparql"
WIKIDATA_SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"

def get_distinctions(person_result):
    try:
        sparql = SPARQLWrapper(WIKIDATA_SPARQL_ENDPOINT)
        person_wikidata = person_result['personWikidata']['value']
        query = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX p: <http://www.wikidata.org/prop/>
    PREFIX ps: <http://www.wikidata.org/prop/statement/>
    PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
    SELECT DISTINCT ?distinction ?date WHERE {{
        <{person_wikidata}> p:P166 [ ps:P166 ?distinction ; pq:P585 ?date ] .
    }}
    """
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        return [(r['distinction']['value'], r['date']['value']) for r in sparql.query().convert()['results']['bindings']]
    except:
        return []

def fetch_quebec_person_distinction():
    sparql = SPARQLWrapper(CQ_SPARQL_ENDPOINT)

    print('Extraction des personnes qui ont obtenus une distinction et qui ont travaillé dans une oeuvre produite au Québec...')
    query = """
PREFIX crm: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX frbroo: <http://iflastandards.info/ns/fr/frbr/frbroo/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT DISTINCT ?person ?personWikidata ?distinction WHERE {
  ?recordingEvent crm:P9_consists_of ?recordingActivity .
  ?recordingEvent crm:P7_took_place_at <http://data.cinematheque.qc.ca/resource/Place216> .
  ?recordingEventCarriedOutBy crm:P01_has_domain ?recordingActivity .
  ?recordingEventCarriedOutBy crm:P02_has_range ?person .
  ?person a crm:E21_Person .
  ?person owl:sameAs ?personWikidata .
}
"""
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    dict_data = []
    results = sparql.query().convert()

    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    results = sparql.query().convert()['results']['bindings']
    distinctions_people = zip(results, pool.map(get_distinctions, results))
    for person_result, distinctions in distinctions_people:
        for distinction in distinctions:
            dict_data.append({ 'person': person_result['person']['value'], 'distinction': distinction[0], 'date': distinction[1] })

    with open('distinctions_people.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['person', 'distinction', 'date'])
        writer.writeheader()
        for data in dict_data:
            writer.writerow(data)

def main():
    # fetch_movie_genres()
    fetch_quebec_person_distinction()

if __name__ == '__main__':
    main()
