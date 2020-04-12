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
        cnx = mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
        cursor = cnx.cursor()
        sql_country = cursor.execute("SELECT * FROM COUNTRIES WHERE countrycode='" + iso + "'")
        cursor.execute(sql_country)
        record = cursor.fetchall()

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

if __name__ == '__main__':
    app.run(debug=True)