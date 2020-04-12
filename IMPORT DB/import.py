from SPARQLWrapper import SPARQLWrapper, JSON
from C_WIKIDATA import WIKIDATA_REQUEST1
from C_CONFIG import *
from C_CITES import CITES1, CITES2, CITES_KEY, CITES2_LEGISLATION
from import_cites import *
from urllib.error import HTTPError
from tables import *
from database import *
import requests
import json
import time

# MySQL
cnx = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
cursor = cnx.cursor()
db = Database(cursor)
db.remove_database(DATABASE)
db.create_database(DATABASE)
db.use_database(DATABASE)
print("create_tables")
db.create_tables(TABLES, cnx)

##############################################

FeedDbCountries()
FeedDbStatus()

##############################################

# Wikidata request
endpoint_url = "https://query.wikidata.org/sparql"
def get_results(endpoint_url, query):
    print(query)
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    try:
        result = sparql.query().convert()
        print (result)
        return result
    except HTTPError as err:
        print(err.code)

wikidata_request_send = WIKIDATA_REQUEST1
results = get_results(endpoint_url, wikidata_request_send)

listIdsSPECIES = []
listResults = []
results = get_results(endpoint_url, wikidata_request_send)
results = results["results"]["bindings"]
print("results")
for result in results:

    id = result["citesid"]["value"]
    print(id)
    if id not in listIdsSPECIES:
        listIdsSPECIES.append(id)
        listResults.append(result)

ligne = 0
for res in listResults:

    name = ''
    wikidataid = ''
    image = ''
    scientific_name = ''
    taxinomic_rank = ''
    upper_taxon = ''
    citesid = ''

    try:
        name = res['itemLabel']['value']
        print (name)
    except:
        name = ''
        print("Error - name")

    try:
        wikidataid = res['item']['value']
        print (wikidataid)
        wikidataid = wikidataid.replace('http://www.wikidata.org/entity/', '')
    except:
        wikidataid = ''
        print("Error - wikidataid")

    try:
        image = res['image']['value']
        print (image)
    except:
        image = ''
        print("Error - image")

    try:
        scientific_name = res['scientific_name']['value']
        print (scientific_name)
    except:
        scientific_name = ''
        print("Error - scientific_name")

    try:
        taxinomic_rank = res['taxinomic_rankLabel']['value']
        print (taxinomic_rank)
    except:
        taxinomic_rank = ''
        print("Error - taxinomic_rank")

    try:
        citesid = res['citesid']['value']
        print (citesid)
    except:
        citesid = ''
        print("Error - citesid")

    try:
        cursor.execute("INSERT INTO MAINTABLE (nom, wikidataid, image, scientific_name, taxinomic_rank, upper_taxon, citesid) VALUES (%s, %s, %s, %s, %s, %s, %s)", (name, wikidataid, image, scientific_name, taxinomic_rank, upper_taxon, citesid))
        cnx.commit()
        ligne = ligne + 1
        print("Row " + str(ligne))
    except:
        print("Error MAINTABLE - INSERT")

##############################################

sql_main_table = "SELECT ID, wikidataid, citesid FROM MAINTABLE"
cursor.execute(sql_main_table)
records = cursor.fetchall()
print("sql_main_table number - ", cursor.rowcount)

##############################################

FeedDbFromCitesDistribution()

##############################################

#for row in records:
#    time.sleep(3)

#    citesidx = row[2]

    # CITES distribution
#    req = CITES1 + str(citesidx) + CITES2
#    print (req)
#    result = requests.get(req, headers={'X-Authentication-Token': CITES_KEY})

#    if result.status_code == '200':
#        print("citesid - ", citesidx, "\n")
#        wjdata = json.loads(result.text)

#        ligne = 0
#        for val in wjdata:
#            print(str(val))
#            countryname = str(val['name'])
#            countrycode = str(val['iso_code2'])
#            countrytype = str(val['type'])
#            countrytags = str(val['tags'])

#            try:
#                cursor.execute(
#                    "INSERT INTO CITES_DISTRIBUTION (citesid, countryname, countrycode, countrytype, countrytags) VALUES (%s, %s, %s, %s, %s, %s, %s)",
#                    (citesid, countryname, countrycode, countrytype, countrytags))
#                cnx.commit()
#                ligne = ligne + 1
#                print("Row " + str(ligne))
#            except:
#                print("Error CITES_DISTRIBUTION - INSERT")
#    else:
#        print("citesid - erreur 404", citesidx, "\n")
