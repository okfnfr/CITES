# Definition of the OKFN France API
# https://blog.invivoo.com/designer-des-apis-rest-avec-flask-restplus/
from flask import Flask, request
from flask_restplus import Api, Resource
import mysql.connector
import json
from C_CONFIG import *

app = Flask(__name__)
api = Api(app=app, version='0.1', title='OKFN Species Api', description='', validate=True)

@api.route("/country/<string:iso>")
class Country(Resource):
    def get(self, iso):

        if len(iso) != 2:
            return {"response": 'Not a valid ISO country code'}, 200

        cnx = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
        cursor = cnx.cursor()
        sql_country = cursor.execute("SELECT * FROM COUNTRIES WHERE countrycode='" + iso + "'")
        cursor.execute(sql_country)
        record = cursor.fetchall()

        if len(record) != 1:
            return {"response": 'Not a valid ISO country code'}, 200

        c = { 'Name': record[0][1], 'ISO': record[0][2] }
        return {"response": json.dumps(c, sort_keys=True, indent=4)}, 200


@api.route("/countries/")
class CountryList(Resource):
    def get(self):
        cnx = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
        cursor = cnx.cursor()

        list = []
        try:
            sql_countries = cursor.execute("SELECT * FROM COUNTRIES")
            cursor.execute(sql_countries)
            records = cursor.fetchall()

            for record in records:
                c = { 'Name': record[1], 'ISO': record[2] }
                list.append(c)

        except:
            print("Erreur list countries")

        return {"response": json.dumps(list, sort_keys=True, indent=4)}, 200


@api.route("/itemWikidata/<string:wikidataid>")
class ItemByWikidata(Resource):
    def get(self, wikidataid):

        cnx = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
        cursor = cnx.cursor()

        sql_wikidataid = cursor.execute("SELECT * FROM MAINTABLE WHERE wikidataid='" + wikidataid + "'")
        cursor.execute(sql_wikidataid)
        record = cursor.fetchall()

        if len(record) != 1:
            return {"response": 'Not a valid wikidataid'}, 200

        # return value
        data = {}
        data_countries = {}

        # Iteration on description column & values
        row = record[0]
        ii = 0
        fields = [i[0] for i in cursor.description]
        for field in fields:
            if ii != 0:
                data[field] = row[ii] # not necessary to have the primary key ID
            ii = ii + 1

        sql_wikidataid = cursor.execute("SELECT COUNTRIES.countryname, CITES_DISTRIBUTION.countrystatus FROM COUNTRIES INNER JOIN CITES_DISTRIBUTION WHERE CITES_DISTRIBUTION.citesid='" + wikidataid + "' AND COUNTRIES.ID = CITES_DISTRIBUTION.countryid")
        cursor.execute(sql_wikidataid)
        record = cursor.fetchall()
        print (record)
        # Iteration on description column & values
        rows = record
        for row in rows:
            country = row[0]
            data_countries[country] = row[1]
        data['countries'] = data_countries

        return {'item': json.dumps(data, sort_keys=True, indent=4)}, 200


@api.route("/itemCites/<string:citesid>")
class ItemByCites(Resource):
    def get(self, citesid):

        cnx = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
        cursor = cnx.cursor()

        sql_citesid = cursor.execute("SELECT * FROM MAINTABLE WHERE citesid='" + citesid + "'")
        cursor.execute(sql_citesid)
        record = cursor.fetchall()

        if len(record) != 1:
            return {"response": 'Not a valid citesid'}, 200

        # return value
        data = {}
        data_countries = {}

        # Iteration on description column & values
        row = record[0]
        ii = 0
        fields = [i[0] for i in cursor.description]
        for field in fields:
            if ii != 0:
                data[field] = row[ii] # not necessary to have the primary key ID
            ii = ii + 1

        sql_citesid = cursor.execute("SELECT COUNTRIES.countryname, CITES_DISTRIBUTION.countrystatus FROM COUNTRIES INNER JOIN CITES_DISTRIBUTION WHERE CITES_DISTRIBUTION.citesid='" + citesid + "' AND COUNTRIES.ID = CITES_DISTRIBUTION.countryid")
        cursor.execute(sql_citesid)
        record = cursor.fetchall()
        print (record)
        # Iteration on description column & values
        rows = record
        for row in rows:
            country = row[0]
            data_countries[country] = row[1]
        data['countries'] = data_countries

        return {'item': json.dumps(data, sort_keys=True, indent=4)}, 200

@api.route("/ByCountryCode/<string:countrycode>")
class ItemByCites(Resource):
    def get(self, countrycode):

        cnx = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
        cursor = cnx.cursor()

        sql_countrycode = cursor.execute("SELECT * FROM MAINTABLE WHERE MAINTABLE.wikidataid IN ( SELECT CITES_DISTRIBUTION.wikidataid FROM CITES_DISTRIBUTION INNER JOIN COUNTRIES WHERE CITES_DISTRIBUTION.countryid=COUNTRIES.ID AND COUNTRIES.countrycode = '" + countrycode + "')")
        cursor.execute(sql_countrycode)
        rows = cursor.fetchall()

        # return value
        data = {}

        fields = [i[0] for i in cursor.description]
        r = 0
        for row in rows:

            datar = {}
            f = 0
            for field in fields:
                if f != 0:
                    datar[field] = row[f] # not necessary to have the primary key ID
                f = f + 1
            data['item' + str(r)] = datar
            r = r + 1

        return {'items': json.dumps(data, sort_keys=True, indent=4)}, 200


@api.route("/ByCountryName/<string:countryname>")
class ItemByCites(Resource):
    def get(self, countryname):

        cnx = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
        cursor = cnx.cursor()

        sql_countrycode = cursor.execute("SELECT * FROM MAINTABLE WHERE MAINTABLE.wikidataid IN ( SELECT CITES_DISTRIBUTION.wikidataid FROM CITES_DISTRIBUTION INNER JOIN COUNTRIES WHERE CITES_DISTRIBUTION.countryid=COUNTRIES.ID AND COUNTRIES.countryname = '" + countryname + "')")
        cursor.execute(sql_countrycode)
        rows = cursor.fetchall()

        # return value
        data = {}

        fields = [i[0] for i in cursor.description]
        r = 0
        for row in rows:

            datar = {}
            f = 0
            for field in fields:
                if f != 0:
                    datar[field] = row[f] # not necessary to have the primary key ID
                f = f + 1
            data['item' + str(r)] = datar
            r = r + 1

        return {'items': json.dumps(data, sort_keys=True, indent=4)}, 200

if __name__ == '__main__':
    app.run(debug=True)