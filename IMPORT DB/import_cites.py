import csv
from tables import *
from database import *
from C_CONFIG import *

def FeedDbCountries():
    cnx = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cursor = cnx.cursor()
    db = Database(cursor)

    with open('csv/COUNTRIES.csv', newline='') as csvfile:

        reader = csv.DictReader(csvfile, delimiter=',')

        for row in reader:

            name = row['name']
            iso = row['alpha-2']
            print(name + " " + iso)
            try:
                cursor.execute(
                    "INSERT INTO COUNTRIES (countryname, countrycode) VALUES (%s, %s)",
                    (name, iso))
                cnx.commit()
                print("Row " + str(lignes_compteur))
            except:
                print("Erreur COUNTRIES - INSERT")

def FeedDbStatus():
    cnx = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cursor = cnx.cursor()
    db = Database(cursor)
    try:
        cursor.execute("INSERT INTO STATUS (status, statusfr) VALUES (%s, %s)", ("Native", "Native"))
        cnx.commit()
        cursor.execute("INSERT INTO STATUS (status, statusfr) VALUES (%s, %s)", ("Introduced", "Introduite"))
        cnx.commit()
        cursor.execute("INSERT INTO STATUS (status, statusfr) VALUES (%s, %s)", ("Reintroduced", "Reintroduite"))
        cnx.commit()
        cursor.execute("INSERT INTO STATUS (status, statusfr) VALUES (%s, %s)", ("Extinct", "Éteinte"))
        cnx.commit()
        cursor.execute("INSERT INTO STATUS (status, statusfr) VALUES (%s, %s)", ("Uncertain", "Incertain"))
        cnx.commit()
        cursor.execute("INSERT INTO STATUS (status, statusfr) VALUES (%s, %s)", ("Extinct?", "Éteinte ?"))
        cnx.commit()
    except:
        print("Erreur STATUS - INSERT")

def FeedDbFromCitesDistribution():
    print("FeedDbFromCitesDistribution")
    cnx = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cursor = cnx.cursor()
    db = Database(cursor)

    with open('csv/cites_listings_2020-04-12 12_12_comma_separated.csv', newline='') as csvfile:

        reader = csv.DictReader(csvfile)
        lignes_compteur = 0

        for row in reader:

            print(row)
            if lignes_compteur > 0:

                citesid = row['Id']
                sql_main_table = "SELECT wikidataid FROM MAINTABLE WHERE citesid='" + citesid + "'"
                cursor.execute(sql_main_table)
                records = cursor.fetchall()

                if len(records) > 0:

                    wikidataid = records[0][0]

                    kingdom = row['Kingdom']
                    phylum = row['Phylum']
                    class_c = row['Class']
                    order_c = row['Order']
                    family = row['Family']
                    genus = row['Genus']
                    species = row['Species']
                    subspecies = row['Subspecies']
                    listing_cites = row['Listing']

                    query = """ UPDATE MAINTABLE
                                    SET kingdom = %s,
                                        phylum = %s,
                                        class_c = %s,
                                        order_c = %s,
                                        family = %s,
                                        genus = %s,
                                        species = %s,
                                        subspecies = %s,                                       
                                        listing_cites = %s
                                    WHERE wikidataid = %s """

                    data = (kingdom, phylum, class_c, order_c, family, genus, species, subspecies, listing_cites, wikidataid)
                    cursor.execute(query, data)
                    cnx.commit()

                    # Cleaning "Province of China", "SAR"
                    distrib_full_name = row['All_DistributionFullNames']
                    distrib_full_name = distrib_full_name.replace("Province of China", "")
                    distrib_full_name = distrib_full_name.replace("SAR", "")
                    distrib_full_name = distrib_full_name.replace("Bonaire", "")

                    full_names = distrib_full_name.split(",")
                    while '' in full_names:
                        full_names.remove('')
                    while ' ' in full_names:
                        full_names.remove(' ')

                    distrib_ISO_code = row['All_DistributionISOCodes']
                    distrib_ISO_code = distrib_ISO_code.replace(", ,", ",")
                    distrib_ISO_code = distrib_ISO_code.replace(",,", ",")
                    iso_codes = distrib_ISO_code.split(",")

                    # Here we define a dictionary
                    thisdict = {}
                    ii = 0
                    for f in full_names:
                        f = full_names[ii].replace("'", "")

                        if f != "":

                            try:
                                thisdict[f] = iso_codes[ii]
                                ii = ii + 1
                            except:
                                print("ERROR DICTIONARY CITES")
                                print(f)
                                print(len(full_names))
                                print(len(iso_codes))
                                print(iso_codes)
                                print(full_names)

                    ################ NATIVE ################
                    native = row['NativeDistributionFullNames']
                    if len(native) > 0:

                        native = native.replace("Province of China", "")
                        native = native.replace("SAR", "")
                        native = native.replace("Bonaire", "")
                        native = native.replace("1- Africa", "")
                        countries = native.split(",")

                        for country in countries:
                            country = country.replace("'", "")

                            if country != "" and  country != " ":

                                try:
                                    sql_main_table = "SELECT ID FROM COUNTRIES WHERE countrycode='" + thisdict[country] + "'"
                                    cursor.execute(sql_main_table)
                                    countries_sql_id = cursor.fetchall()

                                    try:
                                        countryid = countries_sql_id[0][0]
                                        cursor.execute(
                                            "INSERT INTO CITES_DISTRIBUTION (wikidataid, citesid, countryid, countrystatus) VALUES (%s, %s, %s, %s)",
                                            (wikidataid, citesid, countryid, "NATIVE"))
                                        cnx.commit()
                                    except:
                                        print("Error NATIVE: " + country + " " + countryid)

                                except:
                                    print("Error NATIVE (SELECTION): " + country + " : " + thisdict[country])

                    ################ END NATIVE ################


                    ################ INTRODUCED ################
                    native = row['Introduced_Distribution']
                    if len(native) > 0:

                        native = native.replace("Province of China", "")
                        native = native.replace("SAR", "")
                        native = native.replace("Bonaire", "")
                        native = native.replace("1- Africa", "")
                        countries = native.split(",")

                        for country in countries:
                            country = country.replace("'", "")

                            if country != "" and  country != " ":

                                try:
                                    sql_main_table = "SELECT ID FROM COUNTRIES WHERE countrycode='" + thisdict[country] + "'"
                                    cursor.execute(sql_main_table)
                                    countries_sql_id = cursor.fetchall()

                                    try:
                                        countryid = countries_sql_id[0][0]
                                        cursor.execute(
                                            "INSERT INTO CITES_DISTRIBUTION (wikidataid, citesid, countryid, countrystatus) VALUES (%s, %s, %s, %s)",
                                            (wikidataid, citesid, countryid, "INTRODUCED"))
                                        cnx.commit()
                                    except:
                                        print("Error INTRODUCED: " + country + " " + countryid)

                                except:
                                    print("Error INTRODUCED (SELECTION): " + country + " : " + thisdict[country])

                    ################ END INTRODUCED ################

                    ################ REINTRODUCED ################
                    native = row['Reintroduced_Distribution']
                    if len(native) > 0:

                        native = native.replace("Province of China", "")
                        native = native.replace("SAR", "")
                        native = native.replace("Bonaire", "")
                        native = native.replace("1- Africa", "")
                        countries = native.split(",")

                        for country in countries:
                            country = country.replace("'", "")

                            if country != "" and  country != " ":

                                try:
                                    sql_main_table = "SELECT ID FROM COUNTRIES WHERE countrycode='" + thisdict[country] + "'"
                                    cursor.execute(sql_main_table)
                                    countries_sql_id = cursor.fetchall()

                                    try:
                                        countryid = countries_sql_id[0][0]
                                        cursor.execute(
                                            "INSERT INTO CITES_DISTRIBUTION (wikidataid, citesid, countryid, countrystatus) VALUES (%s, %s, %s, %s)",
                                            (wikidataid, citesid, countryid, "REINTRODUCED"))
                                        cnx.commit()
                                    except:
                                        print("Error REINTRODUCED: " + country + " " + countryid)

                                except:
                                    print("Error REINTRODUCED (SELECTION): " + country + " : " + thisdict[country])

                    ################ END REINTRODUCED ################

                    ################ EXTINCT ################
                    native = row['Extinct_Distribution']
                    if len(native) > 0:

                        native = native.replace("Province of China", "")
                        native = native.replace("SAR", "")
                        native = native.replace("Bonaire", "")
                        native = native.replace("1- Africa", "")
                        countries = native.split(",")

                        for country in countries:
                            country = country.replace("'", "")

                            if country != "" and  country != " ":

                                try:
                                    sql_main_table = "SELECT ID FROM COUNTRIES WHERE countrycode='" + thisdict[country] + "'"
                                    cursor.execute(sql_main_table)
                                    countries_sql_id = cursor.fetchall()

                                    try:
                                        countryid = countries_sql_id[0][0]
                                        cursor.execute(
                                            "INSERT INTO CITES_DISTRIBUTION (wikidataid, citesid, countryid, countrystatus) VALUES (%s, %s, %s, %s)",
                                            (wikidataid, citesid, countryid, "EXTINCT"))
                                        cnx.commit()
                                    except:
                                        print("Error EXTINCT: " + country + " " + countryid)

                                except:
                                    print("Error EXTINCT (SELECTION): " + country + " : " + thisdict[country])

                    ################ END EXTINCT ################

                    ################ EXTINCT_QUESTION ################
                    native = row['Extinct(?)_Distribution']
                    if len(native) > 0:

                        native = native.replace("Province of China", "")
                        native = native.replace("SAR", "")
                        native = native.replace("Bonaire", "")
                        native = native.replace("1- Africa", "")
                        countries = native.split(",")

                        for country in countries:
                            country = country.replace("'", "")

                            if country != "" and  country != " ":

                                try:
                                    sql_main_table = "SELECT ID FROM COUNTRIES WHERE countrycode='" + thisdict[country] + "'"
                                    cursor.execute(sql_main_table)
                                    countries_sql_id = cursor.fetchall()

                                    try:
                                        countryid = countries_sql_id[0][0]
                                        cursor.execute(
                                            "INSERT INTO CITES_DISTRIBUTION (wikidataid, citesid, countryid, countrystatus) VALUES (%s, %s, %s, %s)",
                                            (wikidataid, citesid, countryid, "EXTINCT_QUESTION"))
                                        cnx.commit()
                                    except:
                                        print("Error EXTINCT_QUESTION: " + country + " " + countryid)

                                except:
                                    print("Error EXTINCT_QUESTION (SELECTION): " + country + " : " + thisdict[country])

                    ################ END EXTINCT_QUESTION ################

                    ################ UNCERTAIN ################
                    native = row['Distribution_Uncertain']
                    if len(native) > 0:

                        native = native.replace("Province of China", "")
                        native = native.replace("SAR", "")
                        native = native.replace("Bonaire", "")
                        native = native.replace("1- Africa", "")
                        countries = native.split(",")

                        for country in countries:
                            country = country.replace("'", "")

                            if country != "" and  country != " ":

                                try:
                                    sql_main_table = "SELECT ID FROM COUNTRIES WHERE countrycode='" + thisdict[country] + "'"
                                    cursor.execute(sql_main_table)
                                    countries_sql_id = cursor.fetchall()

                                    try:
                                        countryid = countries_sql_id[0][0]
                                        cursor.execute(
                                            "INSERT INTO CITES_DISTRIBUTION (wikidataid, citesid, countryid, countrystatus) VALUES (%s, %s, %s, %s)",
                                            (wikidataid, citesid, countryid, "UNCERTAIN"))
                                        cnx.commit()
                                    except:
                                        print("Error UNCERTAIN: " + country + " " + countryid)

                                except:
                                    print("Error UNCERTAIN (SELECTION): " + country + " : " + thisdict[country])

                    ################ END UNCERTAIN ################

            lignes_compteur = lignes_compteur + 1
